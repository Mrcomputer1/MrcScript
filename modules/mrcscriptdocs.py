import socket

def _module_(args):
    s = socket.socket()
    s.bind(("0.0.0.0", 8080))
    FOLDER = "docs/"
    s.listen(5)
    while True:
        c, addr = s.accept()
        httprequest = c.recv(1024).decode("utf-8")
        httprequestparts = httprequest.split(" ")
        try:
            #print(str(httprequestparts))
            if httprequestparts[1][1:] == "":
                f = open(FOLDER + "index.html", "r")
                t = "text/html"
            elif httprequestparts[1][1:] == "style.css":
                f = open(FOLDER + "style.css", "r")
                t = "text/css"
            else:
                f = open(FOLDER + httprequestparts[1][1:], "r")
                t = "text/html"
            fc = f.read()
            f.close()
            l = len(bytes(fc, "utf-8"))
            l = str(l+1)
            co = fc
            httpres = """HTTP/1.1 200 OK
Content-Type: """ + t + """; charset=UTF-8
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
        except IndexError:
            print("")
