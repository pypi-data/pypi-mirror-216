import fnmatch, traceback, sys, time, os.path, stat, pprint, re, signal, importlib, platform, os

from socket import *
from pythreader import PyThread, synchronized, Task, TaskQueue, Primitive
from webpie import Response
from .uid import uid
from .WPApp import WPApp
from .logs import Logged, Logger

from .py3 import PY2, PY3, to_str, to_bytes

import pythreader

macos = sys.platform.lower().startswith("darwin")

class BodyFile(object):
    
    def __init__(self, buf, sock, length):
        #print("BodyFile: buf:", buf)
        self.Buffer = buf
        self.Sock = sock
        self.Remaining = length
        
    def get_chunk(self, n):
        #print("get_chunk: Buffer:", self.Buffer)
        if self.Buffer:
            out = self.Buffer[:n]
            self.Buffer = self.Buffer[n:]
        elif self.Sock is not None:
            out = self.Sock.recv(n)
            if not out: self.Sock = None
        return out
        
    MAXMSG = 8192
    
    def read(self, N = None):
        #print ("read({})".format(N))
        #print ("Buffer:", self.Buffer)
        if N is None:   N = self.Remaining
        out = []
        n = 0
        eof = False
        while not eof and (N is None or n < N):
            ntoread = self.MAXMSG if N is None else N - n
            chunk = self.get_chunk(ntoread)
            if not chunk:
                eof = True
            else:
                n += len(chunk)
                out.append(chunk)
        out = b''.join(out)
        if self.Remaining is not None:
            self.Remaining -= len(out)
        #print ("returning:[{}]".format(out))
        return out

class HTTPHeader(object):

    def __init__(self):
        self.Headline = None
        self.StatusCode = None
        self.StatusMessage = ""
        self.Method = None
        self.Protocol = None
        self.URI = None
        self.OriginalURI = None
        self.Headers = {}
        self.Raw = b""
        self.Buffer = b""
        self.Complete = False
        self.Error = None
        
    def __str__(self):
        return "HTTPHeader(headline='%s', status=%s)" % (self.Headline, self.StatusCode)
        
    __repr__ = __str__

    def recv(self, sock):
        tmo = sock.gettimeout()
        sock.settimeout(15.0)
        received = eof = False
        self.Error = None
        try:
            body = b''
            while not received and not self.Error and not eof:       # shutdown() will set it to None
                try:    
                    data = sock.recv(1024)
                except Exception as e:
                    self.Error = "Error in recv(): %s" % (e,)
                    data = b''
                if data:
                    received, error, body = self.consume(data)
                else:
                    eof = True
        finally:
            sock.settimeout(tmo)
        return received, body
        
    def replaceURI(self, uri):
        self.URI = uri

    def is_server(self):
        return self.StatusCode is not None

    def is_client(self):
        return self.Method is not None
        
    def is_valid(self):
        return self.Error is None and self.Protocol and self.Protocol.upper().startswith("HTTP/")

    def is_final(self):
        return self.is_server() and self.StatusCode//100 != 1 or self.is_client()

    EOH_RE = re.compile(b"\r?\n\r?\n")
    MAXREAD = 100000

    def consume(self, inp):
        #print(self, ".consume(): inp:", inp)
        header_buffer = self.Buffer + inp
        match = self.EOH_RE.search(header_buffer)
        if not match:   
            self.Buffer = header_buffer
            error = False
            if len(header_buffer) > self.MAXREAD:
                self.Error = "Request is too long: %d" % (len(header_buffer),)
                error = True
            return False, error, b''
        i1, i2 = match.span()            
        self.Complete = True
        self.Raw = header = header_buffer[:i1]
        rest = header_buffer[i2:]
        headers = {}
        header = to_str(header)
        lines = [l.strip() for l in header.split("\n")]
        if lines:
            self.Headline = headline = lines[0]
            
            words = headline.split(" ", 2)
            #print ("HTTPHeader: headline:", headline, "    words:", words)
            if len(words) != 3:
                self.Error = "Can not parse headline. len(words)=%d" % (len(words),)
                return True, True, b''      # malformed headline
            if words[0].lower().startswith("http/"):
                self.StatusCode = int(words[1])
                self.StatusMessage = words[2]
                self.Protocol = words[0].upper()
            else:
                self.Method = words[0].upper()
                self.Protocol = words[2].upper()
                self.URI = self.OriginalURI = words[1]
                    
            for l in lines[1:]:
                if not l:   continue
                try:   
                    h, b = tuple(l.split(':', 1))
                    headers[h.strip()] = b.strip()
                except: pass
            self.Headers = headers
        self.Buffer = b""
        return True, False, rest

    def path(self):
        return self.URI.split("?",1)[0]

    def query(self):
        if '?' in self.URI:
             return self.URI.split("?",1)[1]
        else:
             return ""

    def removeKeepAlive(self):
        if "Connection" in self.Headers:
            self.Headers["Connection"] = "close"

    def forceConnectionClose(self):
        self.Headers["Connection"] = "close"

    def headersAsText(self):
        headers = []
        for k, v in self.Headers.items():
            if isinstance(v, list):
                for vv in v:
                    headers.append("%s: %s" % (k, vv))
            else:
                headers.append("%s: %s" % (k, v))
        return "\r\n".join(headers) + "\r\n"

    def headline(self, original=False):
        if self.is_client():
            return "%s %s %s" % (self.Method, self.OriginalURI if original else self.URI, self.Protocol)
        else:
            return "%s %s %s" % (self.Protocol, self.StatusCode, self.StatusMessage)

    def as_text(self, original=False):
        return "%s\r\n%s" % (self.headline(original), self.headersAsText())

    def as_bytes(self, original=False):
        return to_bytes(self.as_text(original))

class RequestProcessor(Task):
    
    def __init__(self, wsgi_app, request):
        Task.__init__(self, name=f"[RequestProcessor {request.Id}]")
        #print("RequestTask: wsgi_app:", wsgi_app)
        self.WSGIApp = wsgi_app
        self.Request = request
        self.OutBuffer = ""
        self.StatusCode = None
        self.ByteCount = 0
        self.Error = None

    def run(self):       
        request = self.Request
        #print("Task: request:", request)
        try:
            env = request.wsgi_env() 
            header = request.HTTPHeader
            csock = request.CSock

            if env["WebPie.headers"].get("Expect") == "100-continue":
                csock.sendall(b'HTTP/1.1 100 Continue\n\n')
                    
            out = []
            
            try:
                #print("env:")
                #for k, v in env.items():
                #    print(k,":",v)
                out = self.WSGIApp(env, self.start_response)
                #print("HTTPServer: out:", out)
            except:
                error = "error in wsgi_app: %s" % (traceback.format_exc(),)
                csock.sendall(b"HTTP/1.1 500 Error\nContent-Type: text/plain\n\n"+to_bytes(error))
                return self.error(error)
            

            #print("RequestProcessor.run: out:", out)
            if self.OutBuffer:      # from start_response
                #print("RequestProcessor.run: OutBuffer:", self.OutBuffer)
                csock.sendall(to_bytes(self.OutBuffer))
                
            self.ByteCount = 0

            for line in out:
                line = to_bytes(line)
                try:
                    #print("sending line:", line)    
                    csock.sendall(line)
                    #print("HTTPServer: sent:", line)
                except Exception as e:
                    return self.error("error sending body: %s" % (e,))
                self.ByteCount += len(line)
        finally:
            #print("HTTPServer: closing request...")
            request.close()
            self.OutBuffer = None
            self.WSGIApp = None

    def error(self, error):
        self.Error = error

    def start_response(self, status, headers):
        self.StatusCode = int(status.split(None, 1)[0])
        out = ["HTTP/1.1 " + status]
        for h,v in headers:
            if h != "Connection":
                out.append("%s: %s" % (h, v))
        out.append("Connection: close")     # can not handle keep-alive
        out.append(f"X-WebPie-Request-Id: {self.Request.Id}")
        self.OutBuffer = "\r\n".join(out) + "\r\n\r\n"

class Service(Logged):
    
    def __init__(self, app, capacity=100, logger=None):
        Logged.__init__(self, f"[{app.__class__.__name__}]", logger=logger)
        self.Name = app.__class__.__name__
        self.WPApp = app
        self.ProcessorQueue = TaskQueue(5, capacity=capacity, delegate=self)

    def accept(self, request):
        if not self.WPApp.match(request.HTTPHeader.URI):
            return False, "no match"
        p = RequestProcessor(self.WPApp, request)
        request.AppName = self.Name
        try:
            self.ProcessorQueue.add(p, timeout=0)
        except RuntimeError:
            return True, "service unavailable"
        else:
            return True, "accepted"

    def taskFailed(self, queue, task, exc_type, exc_value, tb):
        self.error("request failed:", "".join(traceback.format_exception(exc_type, exc_value, tb)))
        try:
            task.Request.close()
        except:
            pass

    def taskEnded(self, queue, task, _):
        request = task.Request
        header = request.HTTPHeader
        log_line = '%s %s:%s :%s %s %s -> %s %s %s %s' % (   
                        request.Id, request.CAddr[0], request.CAddr[1], request.ServerPort, 
                        header.Method, header.OriginalURI, 
                        request.AppName, header.path(),
                        task.StatusCode, task.ByteCount
                    )
        self.log(log_line)

class Request(object):
    
    def __init__(self, port, csock, caddr):
        self.Id = uid()
        self.ServerPort = port
        self.CSock = csock
        self.CAddr = caddr
        self.HTTPHeader = None
        self.Body = b''
        self.SSLInfo = None     
        self.AppName = None
        self.Environ = {}
        
    def close(self):
        if self.CSock is not None:
            try:
                if macos:
                    # this seems to be necessary on MacOS to make sure all buffered data is sent before closing the socket
                    os.fsync(self.CSock.fileno())
                self.CSock.close()
            except: 
                pass
            self.CSock = None
        self.SSLInfo = None

    def wsgi_env(self):
        header = self.HTTPHeader
        ssl_info = self.SSLInfo
        csock = self.CSock

        env = dict(
            REQUEST_METHOD = header.Method.upper(),
            PATH_INFO = header.path(),
            SCRIPT_NAME = "",
            SCRIPT_FILENAME = "",
            SERVER_PROTOCOL = header.Protocol,
            QUERY_STRING = header.query(),
        )
        env.update(self.Environ)
        env["REQUEST_SCHEME"] = env["wsgi.url_scheme"] = "http"
        env["WebPie.request_id"] = self.Id
        env["WebPie.headers"] = header.Headers

        if ssl_info != None:
            subject, issuer = self.x509_names(ssl_info)
            env["SSL_CLIENT_S_DN"] = subject
            env["SSL_CLIENT_I_DN"] = issuer
            env["REQUEST_SCHEME"] = env["wsgi.url_scheme"] = "https"
        
        env["query_dict"] = self.parseQuery(header.query())
        
        #print ("processRequest: env={}".format(env))
        body_length = None
        for h, v in header.Headers.items():
            h = h.lower()
            if h == "content-type": env["CONTENT_TYPE"] = v
            elif h == "host":
                words = v.split(":",1)
                words.append("")    # default port number
                env["HTTP_HOST"] = v
                env["SERVER_NAME"] = words[0]
                env["SERVER_PORT"] = words[1]
            elif h == "content-length": 
                env["CONTENT_LENGTH"] = body_length = int(v)
            else:
                env["HTTP_%s" % (h.upper().replace("-","_"),)] = v

        env["wsgi.input"] = BodyFile(self.Body, csock, body_length)
        return env

    def parseQuery(self, query):
        out = {}
        for w in query.split("&"):
            if w:
                words = w.split("=", 1)
                k = words[0]
                if k:
                    v = None
                    if len(words) > 1:  v = words[1]
                    if k in out:
                        old = out[k]
                        if type(old) != type([]):
                            old = [old]
                            out[k] = old
                        out[k].append(v)
                    else:
                        out[k] = v
        return out
        
    def format_x509_name(self, x509_name):
        components = [(to_str(k), to_str(v)) for k, v in x509_name.get_components()]
        return ",".join(f"{k}={v}" for k, v in components)
        
    def x509_names(self, ssl_info):
        import OpenSSL.crypto as crypto
        subject, issuer = None, None
        if ssl_info is not None:
            cert_bin = ssl_info.getpeercert(True)
            if cert_bin is not None:
                x509 = crypto.load_certificate(crypto.FILETYPE_ASN1,cert_bin)
                if x509 is not None:
                    subject = self.format_x509_name(x509.get_subject())
                    issuer = self.format_x509_name(x509.get_issuer())
        return subject, issuer

    def send_response(self, status, headline):
        response = f"HTTP/1.1 {status} {headline}\n\n"
        self.CSock.sendall(to_bytes(response))

class RequestReader(Task, Logged):

    MAXMSG = 100000

    def __init__(self, dispatcher, request, socket_wrapper, timeout, logger):
        Task.__init__(self)
        self.Request = request       
        Logged.__init__(self, f"[RequestReader {request.Id} client:%s:%s]" % request.CAddr, logger=logger, debug=True)
        self.SocketWrapper = socket_wrapper
        self.Dispatcher = dispatcher
        self.Timeout = timeout
        self.debug("created")

    def __str__(self):
        return "[reader %s]" % (self.Request.Id, )
        
    #def addToBody(self, data):
    #    if PY3:   data = to_bytes(data)
    #    #print ("addToBody:", data)
    #    self.Body.append(data)

    def run(self):
        header = None
        body = b''
        request = self.Request
        csock = request.CSock
        saved_timeout = csock.gettimeout() 
        dispatched = False
        dispatch_status = None
        try:
            #self.debug("started")
            self.Started = time.time()
            csock.settimeout(self.Timeout) 
            error = False       
            if self.SocketWrapper is not None:
                try:
                    csock, ssl_info = self.SocketWrapper.wrap(self.Request.CSock)
                    self.Request.CSock = csock
                    self.Request.SSLInfo = ssl_info
                    self.debug("socket wrapped")
                except Exception as e:
                    self.debug("Error wrapping socket: %s" % (e,))
                    error = True
            #self.debug("wrapped:", csock)
            if not error:
                #print("no error")
                header = HTTPHeader()
                request_received, body = header.recv(csock)
                csock.settimeout(saved_timeout) 
                
                if not request_received or not header.is_valid() or not header.is_client():
                    # header not received - end
                    #print("request invalid header.Error=", header.Error)
                    #print("   request_received:", request_received)
                    #print("   header.is_valid():", header.is_valid())
                    #print("   header.is_client():", header.is_client())
                    #print("   header.Protocol:", header.Protocol)
                        
                    self.debug("request not received or invalid or not client request: %s" % (request,))
                    if header.Error:
                        self.debug("request read error: %s" % (header.Error,))
                    dispatch_status = "invalid request"
                    return None
                else:
                    request.HTTPHeader = header
                    request.Body = body
                    self.debug("request received")
                    dispatched, service, dispatch_status = self.Dispatcher.dispatch(self.Request)
        finally:
            if not dispatched:
                if header is not None and header.Complete:
                    #print("dispatch status:", dispatch_status)
                    if dispatch_status == "no match":
                        request.send_response(404, "Service not found")
                    elif dispatch_status == "service unavailable":
                        request.send_response(503, "Service unavailable")
                    elif dispatch_status == "invalid request":
                        request.send_response(400, "Invalid request")
                    else:
                        request.send_response(500, "Request dispatch error " + dispatch_status)
                    self.log('%s %s:%s :%s %s %s -> (%s)' % 
                        (   request.Id, request.CAddr[0], request.CAddr[1], request.ServerPort, 
                            header.Method, header.OriginalURI, dispatch_status
                        )
                    )
                else:
                    self.log('%s:%s :%s (request reading error)' % 
                        (   request.CAddr[0], request.CAddr[1], request.ServerPort)
                    )
                request.close()
                    
            self.SocketWrapper = self.Dispatcher = self.Logger = None

class SSLSocketWrapper(object):
     
    def __init__(self, certfile, keyfile, verify, ca_file, password, allow_proxies=False):
        import ssl
        
        self.SSLContext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.SSLContext.load_cert_chain(certfile, keyfile, password=password)
        if ca_file is not None:
            self.SSLContext.load_verify_locations(cafile=ca_file)
        verify_flags = {
                "none":ssl.CERT_NONE,
                "optional":ssl.CERT_OPTIONAL,
                "required":ssl.CERT_REQUIRED
            }
        try:    self.SSLContext.verify_mode = verify_flags[verify]
        except KeyError:
            raise ValueError(f"Unrecognized verify mode: {verify}")

        flags = 0
        try:
            if allow_proxies:
                flags |= ssl.VERIFY_ALLOW_PROXY_CERTS    
        except AttributeError:
            raise ValueError("X.509 proxies are not supported by the ssl module")
        self.SSLContext.verify_flags = flags
        
        self.SSLContext.load_default_certs()
            
    def wrap(self, sock):
        ssl_socket = self.SSLContext.wrap_socket(sock, server_side=True)
        return ssl_socket, ssl_socket

class HTTPServer(PyThread, Logged):

    def __init__(self, port, app=None, services=[], sock=None, logger=None, max_connections = 100,
                timeout = 20.0,
                enabled = True, max_queued = 100,
                logging = False, log_file = "-", debug=False,
                certfile=None, keyfile=None, verify="none", ca_file=None, password=None, allow_proxies=False, **pythread_kv
                ):
        PyThread.__init__(self, **pythread_kv)
        self.Port = port
        self.Sock = sock
        assert self.Port is not None, "Port must be specified"
        if logger is None and logging:
            logger = Logger(log_file)
            #print("logs sent to:", f)
        Logged.__init__(self, f"[server {self.Port}]", logger=logger, debug=debug)
        self.Logger = logger
        self.Timeout = timeout
        max_connections =  max_connections
        queue_capacity = max_queued
        self.RequestReaderQueue = TaskQueue(max_connections, capacity=max_queued, delegate=self)
        self.SocketWrapper = SSLSocketWrapper(certfile, keyfile, verify, ca_file, password,
                allow_proxies=allow_proxies) if keyfile else None
        
        if app is not None:
            services = [Service(app, logger=logger)]
            
        self.Services = services
        self.Stop = False

    def close(self):
        self.RequestReaderQueue.hold()
        self.Stop = True
        try:    
            self.Sock.close()
        except Exception as e:
            pass
        self.Sock = None

    @staticmethod
    def from_config(config, services, logger=None, logging=False, log_file=None, debug=None):
        port = config["port"]
        
        timeout = config.get("timeout", 20.0)
        max_connections = config.get("max_connections", 100)
        queue_capacity = config.get("queue_capacity", 100)

        # TLS
        certfile = config.get("cert")
        keyfile = config.get("key")
        verify = config.get("verify", "none")
        ca_file = config.get("ca_file")
        password = config.get("password")
        
        #print("HTTPServer.from_config: services:", services)
        
        return HTTPServer(port, services=services, logger=logger, max_connections=max_connections,
                timeout = timeout, max_queued = queue_capacity, 
                logging = logging, log_file=log_file, debug=debug,
                certfile=certfile, keyfile=keyfile, verify=verify, ca_file=ca_file, password=password
        )
    
    @synchronized
    def setServices(self, services):
        self.Services = services
        
    def connectionCount(self):
        return len(self.Connections)    

    def run(self):
        if self.Sock is None:
            # therwise use the socket supplied to the constructior
            self.Sock = socket(AF_INET, SOCK_STREAM)
            self.Sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            self.Sock.bind(('', self.Port))
            self.Sock.listen(10)
        while not self.Stop:
            self.debug("--- accept loop port=%d start" % (self.Port,))
            csock = None
            caddr = ('-','-')
            try:
                csock, caddr = self.Sock.accept()
                self.connection_accepted(csock, caddr)
            except Exception as exc:
                #traceback.print_exc()
                if not self.Stop:
                    self.debug("connection processing error: %s" % (traceback.format_exc(),))
                    self.error(caddr, "Error processing connection: %s" % (exc,))
                    if csock is not None:
                        try:    csock.close()
                        except: pass
                self.debug("--- accept loop port=%d end" % (self.Port,))
        if self.Stop:   self.debug("stopped")
        try:    self.Sock.close()
        except: pass
        self.Sock = None
        self.RequestReaderQueue.join()

    def connection_accepted(self, csock, caddr):        # called externally by multiserver
        request = Request(self.Port, csock, caddr)
        self.debug("connection %s accepted from %s:%s" % (request.Id, caddr[0], caddr[1]))
        reader = RequestReader(self, request, self.SocketWrapper, self.Timeout, self)
        self.RequestReaderQueue << reader
        
    @synchronized
    def stop(self):
        self.Stop = True
        try:    self.Sock.close()
        except: pass

    def dispatch(self, request):
        with self:
            services = self.Services[:]
        for service in services:
            match, status = service.accept(request)
            if match:
                return status == "accepted", service, status
        else:
            return False, None, "no match"

    def taskFailed(self, queue, task, exc_type, exc, tb):
        traceback.print_exception(exc_type, exc, tb)
            
def run_server(port, app, **args):
    assert isinstance(port, int), "Port must be integer"
    assert isinstance(app, WPApp), "Application must be a WPApp"
    srv = HTTPServer(port, app, **args)
    srv.start()
    srv.join()
    

