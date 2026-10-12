import os, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

# Ayarlar script'in yanindaki patchserver.json'dan okunur (setup.ps1 uretir).
_cfg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patchserver.json")
if os.path.isfile(_cfg):
    _d = json.load(open(_cfg))
    ROOT_UPDATE = _d["patch_dir"]
    ROOT_PATCHER = _d["patcher_dir"]
else:
    ROOT_UPDATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patch")
    ROOT_PATCHER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "patcher")

class H(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_GET(self):
        url = self.path.split("?")[0]
        if url.startswith("/update/"):
            base, rel = ROOT_UPDATE, url[8:]
        elif url.startswith("/patcher/"):
            base, rel = ROOT_PATCHER, url[9:]
        else:
            self.send_error(404); return
        rel = rel.lstrip("/")
        if not rel or ".." in rel.split("/"):
            self.send_error(404); return
        p = os.path.normpath(os.path.join(base, rel.replace("/", os.sep)))
        if not p.startswith(os.path.abspath(base) + os.sep) or not os.path.isfile(p):
            self.send_error(404); return
        size = os.path.getsize(p)
        ext = os.path.splitext(p)[1].lower()
        ctype = "application/octet-stream"
        if ext == ".json": ctype = "application/json"
        elif ext == ".exe": ctype = "application/x-msdownload"
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(size))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        with open(p, "rb") as f:
            while True:
                chunk = f.read(1 << 20)
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return

    def do_POST(self):
        self.send_error(405)
    do_PUT = do_POST
    do_DELETE = do_POST
    do_HEAD = do_GET

ThreadingHTTPServer(("127.0.0.1", 8091), H).serve_forever()
