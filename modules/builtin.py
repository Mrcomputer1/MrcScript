def log(args, varlist, globallist, runCommand):
    print(args[0])
    return varlist

def read(args, varlist, globallist, runCommand):
    if len(args) == 1:
        varlist[args[0]] = input()
    else:
        varlist[args[1]] = input(args[0])
    return varlist

def var(args, varlist, globallist, runCommand):
    varlist[args[0]] = args[1]
    return varlist

def end(args, varlist, globallist, runCommand):
    raise SystemExit
