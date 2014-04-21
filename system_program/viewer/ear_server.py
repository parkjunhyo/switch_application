#! /usr/bin/python

import os, sys, json, time
from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

class Server_ear:

 def application(self,environ,start_response):

  ## POST method
  if environ['REQUEST_METHOD'] == 'POST':
   try:
    request_body_size = int(environ.get('CONTENT_LENGTH',0))
   except:
    request_body_size = int(0)
   request_body = environ['wsgi.input'].read(request_body_size)
   input_dict = json.loads(request_body)
   return_result = json.dumps(input_dict)

  ## GET method
  elif environ['REQUEST_METHOD'] == 'GET':
   input_dict = parse_qs(environ['QUERY_STRING'])
   return_result = json.dumps(input_dict)

  ## PUT method
  elif environ['REQUEST_METHOD'] == 'PUT':
   pass

  ## Other method
  else:
   pass

  ## add the header information
  status = '200 OK'
  response_headers = [('Content-Type', 'text/html'),
                     ('Access-Control-Allow-Origin','*'),
                     ('Access-Control-Allow-Credentials','true'),
                     ('Access-Control-Allow-Methods', 'POST, GET, PUT, OPTIONS'),
                     ('Access-Control-Allow-Headers', 'Access-Control-Allow-Origin, X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version, Access-Control-Allow-Credentials'),
                     ('Access-Control-Expose-Headers','Content-Length'),
                     ('Content-Length', str(len(return_result)))]

  ## return the response
  start_response(status, response_headers)
  return [return_result]

 
 def run_server(self):

  process_id = os.fork()

  if not process_id:

   os.setpgrp()
   os.umask(0)

   ## file open to save process id
   f=open("./ear_server.pid",'w')
   f.write(str(os.getpid())+"\n")
   f.close()
   
   ## runing the child process to create daemon
   self.makeserver = make_server('',8088,self.application)
   while 1:
    # self.makeserver.serve_forever()
    try:
     self.makeserver.handle_request()
    except:
     time.sleep(0.1)


  

if __name__ == '__main__':

 srv = Server_ear()
 srv.run_server()
