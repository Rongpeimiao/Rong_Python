#!/usr/bin/python
# vim: set fileencoding=utf-8 :

'''
Created on 2017-2-23

@author: Administrator
'''
import urllib
import io
import shutil
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    def _writeheaders(self):
        print "path==========",self.path,
        print "headers========",self.headers
#        self.send_response(200);
        self.send_header('Content-type','text/html');
        self.end_headers()
    def do_Head(self):
        self._writeheaders()
    def do_GET(self):
        content=""
#        self._writeheaders()
        if '?' in self.path:#如果带有参数  
#            http://ip:8765/?test=data
            query = urllib.splitquery(self.path)
            action=query[0]
            print "action====",action
            if query[1]:
                queryParams={}
                for qp in query[1].split('&'):
                    kv=qp.split('=')
                    queryParams[kv[0]]=urllib.unquote(kv[1]).decode("utf-8",'ignore')
                    content+=kv[0]+':'+queryParams[kv[0]]+"\r\n"
            enc="UTF-8"
            content=content.encode(enc)
            f=io.BytesIO()
            f.write(content)
            print "content=====",content
            f.seek(0)
            self.send_response(200)
            self.send_header("Content-type","text/html;charset=%s"% enc)
            self.send_header("Content-Length",str(len(content)))
            self.end_headers()
            shutil.copyfileobj(f,self.wfile)
            self.wfile.write(200)
    def do_POST(self):
        print "POST"
        self._writeheaders()
        length = self.headers.getheader('content-length');
        nbytes = int(length)  
        data = self.rfile.read(nbytes)
        print "data==========",data
        self.wfile.write(200)
        
addr = ('',8080)
server = HTTPServer(addr,RequestHandler)
server.serve_forever()

            
            
