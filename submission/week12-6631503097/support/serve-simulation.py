"""Serve instructor simulation assets unchanged on loopback for manual browser evidence."""
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
class Handler(BaseHTTPRequestHandler):
 def do_GET(self):
  route=self.path.split('?')[0]
  files={'/sim/resolver-confusion':('labs/live-quiz/templates/sim_resolver_confusion.html','text/html'),'/static/sim/sim.css':('labs/live-quiz/static/sim/sim.css','text/css'),'/static/sim/resolver-confusion.js':('labs/live-quiz/static/sim/resolver-confusion.js','text/javascript')}
  if route not in files:self.send_error(404);return
  file,mime=files[route];data=(ROOT/file).read_bytes()
  if mime=='text/html':data=data.replace(b'{{ title }}',b'Week 12 - Dependency Confusion').replace(b'{{ asset_v }}',b'local')
  self.send_response(200);self.send_header('Content-Type',mime);self.end_headers();self.wfile.write(data)
print('Open http://127.0.0.1:8765/sim/resolver-confusion ; Ctrl-C stops the server',flush=True)
HTTPServer(('127.0.0.1',8765),Handler).serve_forever()
