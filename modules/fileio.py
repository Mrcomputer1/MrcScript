def read(args, varlist, globallist, runCommand):
    f = open(args[0], "r")
    varlist[args[1]] = f.read()
    f.close()
    return varlist

def write(args, varlist, globallist, runCommand):
    f = open(args[0], "w")
    f.write(args[1])
    f.close()
    return varlist

def append(args, varlist, globallist, runCommand):
    f = open(args[0], "a")
    f.write(args[1])
    f.close()
    return varlist
