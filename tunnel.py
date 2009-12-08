#!/bin/sh -
"exec" "python" "-O" "$0" "$@"

__doc__ = """tunnel.

This module implements GET, HEAD, POST, PUT and DELETE methods
on BaseHTTPServer, and behaves as an HTTP proxy.  The CONNECT
method is also implemented experimentally, but has not been
tested yet.

Any help will be greatly appreciated.		SUZUKI Hisao
"""

__version__ = "0.0.1"

import BaseHTTPServer, select, socket, SocketServer, urlparse, urllib2

class ProxyHandler (BaseHTTPServer.BaseHTTPRequestHandler):
    __base = BaseHTTPServer.BaseHTTPRequestHandler
    __base_handle = __base.handle

    server_version = "tunnel/" + __version__
    rbufsize = 0                        # self.rfile Be unbuffered

    def do_GET(self):
            headers = {"Proxy-Connection" : "", }
            req = urllib2.Request(self.path, headers=headers) 
            
            try:
            	data = urllib2.urlopen(req)
                self.send_response(200)
                self.end_headers()
                self.wfile.write(data.read())

            except IOError:
                self.send_response(500)
                self.end_headers()
            
    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT  = do_GET
    do_DELETE=do_GET

class ThreadingHTTPServer (SocketServer.ThreadingMixIn,
                           BaseHTTPServer.HTTPServer): pass

if __name__ == '__main__':
    from sys import argv
    if argv[1:] and argv[1] in ('-h', '--help'):
        print argv[0], "[port [allowed_client_name ...]]"
    else:
        if argv[2:]:
            allowed = []
            for name in argv[2:]:
                client = socket.gethostbyname(name)
                allowed.append(client)
                print "Accept: %s (%s)" % (client, name)
            ProxyHandler.allowed_clients = allowed
            del argv[2:]
        else:
            print "Any clients will be served..."
        BaseHTTPServer.test(ProxyHandler, ThreadingHTTPServer)
