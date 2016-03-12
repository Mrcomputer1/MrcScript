import socket

def _module_(args):
    s = socket.socket()
    if '-port' in args:
        s.bind(("0.0.0.0", int(args['-port'])))
    else:
        s.bind(("0.0.0.0", 80))
    if '-folder' in args:
        FOLDER = args['-folder']
    else:
        FOLDER = ""
    s.listen(5)
    while True:
        c, addr = s.accept()
        httprequest = c.recv(1024).decode("utf-8")
        httprequestparts = httprequest.split(" ")
        try:
            f = open(FOLDER + httprequestparts[1][1:], "r")
            fc = f.read()
            f.close()
            l = len(bytes(fc, "utf-8"))
            l = str(l+1)
            co = fc
            httpres = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: """ + l + """
Server: Mrcomputer1 MrcScript Web Server (HTTP Module)
Connection: close
\r\n
""" + co
            c.send(httpres.encode("utf-8"))
            c.close()
        except IOError:
            try:
                f = open(FOLDER + "__404__.html", "r")
                fc = f.read()
                f.close()
                l = len(bytes(fc, "utf-8"))
                l = str(l+1)
                co = fc
                httpres = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: """ + l + """
Server: Mrcomputer1 MrcScript Web Server (HTTP Module)
Connection: close
\r\n
""" + co
                c.send(httpres.encode("utf-8"))
                c.close()
            except IOError:
                fc = "<h1>404 Not Found</h1>The requested file was not found!"
                l = len(bytes(fc, "utf-8"))
                l = str(l+1)
                co = fc
                httpres = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: """ + l + """
Server: Mrcomputer1 MrcScript Web Server (HTTP Module)
Connection: close
\r\n
""" + co
                c.send(httpres.encode("utf-8"))
                c.close()

def init(args, varlist, globallist):
    varlist["_modules_http"] = {
        "socket": socket.socket(),
        "pages": {},
        "errors": {
            "404": """
<h1>404 Not Found</h1>
The requested file was not found!"""
        }
    }
    varlist["_modules_http"]["socket"].bind(("0.0.0.0", args[0]))
    return varlist

def addPage(args, varlist, globallist):
    varlist["_modules_http"]["pages"][args[0]] = args[1]
    return varlist

def run(args, varlist, globallist):
    varlist["_modules_http"]["socket"].listen(5)
    while True:
        c, addr = varlist["_modules_http"]["socket"].accept()
        httprequest = c.recv(1024).decode("utf-8")
        httprequestparts = httprequest.split(" ")
        if httprequestparts[1] in varlist["_modules_http"]["pages"]:
            l = len(bytes(varlist["_modules_http"]["pages"][httprequestparts[1]], "utf-8"))
            l = str(l+1)
            co = varlist["_modules_http"]["pages"][httprequestparts[1]]
            httpres = """HTTP/1.1 200 OK
Content-Type: text/html; charset=UTF-8
Content-Length: """ + l + """
Server: Mrcomputer1 MrcScript Web Server (HTTP Module)
Connection: close
\r\n
""" + co
            c.send(httpres.encode("utf-8"))
        else:
            l = len(bytes(varlist["_modules_http"]["errors"]["404"], "utf-8"))
            l = str(l+1)
            co = varlist["_modules_http"]["errors"]["404"]
            httpres = """HTTP/1.1 404 Not Found
Content-Type: text/html; charset=UTF-8
Content-Length: """ + l + """
Server: Mrcomputer1 MrcScript Web Server (HTTP Module)
Connection: close
\r\n
""" + co
            c.send(httpres.encode("utf-8"))
        c.close()
