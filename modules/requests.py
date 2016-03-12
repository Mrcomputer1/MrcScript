try:
    import requests
    USING_REQUESTS = True
except ImportError:
    import urllib.request
    USING_REQUESTS = False

def get(args, varlist, globallist):
    if USING_REQUESTS:
        r = requests.get(args[0])
        varlist[args[1]] = r.text
    else:
        varlist[args[1]] = urllib.request.urlopen(args[0]).read()
    return varlist

def post(args, varlist, globallist):
    if USING_REQUESTS:
        r = requests.post(args[0], data=args[1])
        varlist[args[2]] = r.text
    else:
        print("Please install python requests (pip install requests)!")
        raise SystemExit
