import json, sys, importlib
import modules.builtin as builtin

VERSION = "1.1"
ERRORS = { #Still working on error system
    "UNKNOWN": "Something went wrong!",
    "BAD_IMPORT": "You are attemping to importing a module that does not exist",
    "NO_PROGRAM": "Please include a program!",
    "MODULE_DOES_NOT_SUPPORT": "Module does not support running with -m"
}
MODULES = {}
GLOBALS = {}
VARIABLES = {}
FUNCTIONS = {}

if len(sys.argv) == 1:
    print("MrcScript v" + VERSION )
    print()
    print("MrcScript.py (script file).mrcscript")
    print("\t     (script file).json")
    print()
    print("MrcScript.py -m (module)")
else:
    if sys.argv[1] == "-m":
        m = importlib.import_module("modules." + sys.argv[2])
        argv = sys.argv[3:]
        args = {}
        for arg in argv:
            argsp = arg.split("=")
            args[argsp[0][1:]] = argsp[1]
        try:
            m._module_(args)
        except AttributeError:
            print(ERRORS["MODULE_DOES_NOT_SUPPORT"])
        sys.exit(0)
    f = open(sys.argv[1], "r")
    fc = f.read()
    f.close()

    j = json.loads(fc)

    if 'imports' in j:
        for i in j['imports']:
            try:
                MODULES[i] = importlib.import_module("modules." + i)
            except ImportError:
                print(ERRORS['BAD_IMPORT'])
                sys.exit(1)

    if 'globals' in j:
        for g in j['globals']:
            GLOBALS[g[0]] = g[1]

    if 'functions' in j:
        for f in j['functions']:
            FUNCTIONS[f[0]] = f[1]

    if not 'program' in j:
        print(ERRORS["NO_PROGRAM"])
        sys.exit(1)
    def runCommand(c, var=None):
      global VARIABLES
      global FUNCTIONS
      global GLOBALS
      global ERRORS
      global VERSION
      if not var == None:
          VARIABLES = var
      if isinstance(c[0], str):
         return
      if len(c[0]) == 1:
         args = c[1:]
         argi = 0
         for a in args:
            if isinstance(a, list):
               if a[0] == "var":
                  args[argi] = VARIABLES[a[1]]
               elif a[0] == "global":
                  args[argi] = GLOBALS[a[1]]
            argi = argi + 1
         if c[0][0] == "if":
             if args[0] == args[1]:
                 for anarg in args[2]:
                     runCommand(anarg)
             else:
                 for anarg in args[3]:
                     runCommand(anarg)
             return
         elif c[0][0] == "+":
             VARIABLES[args[0]] = args[1] + args[2]
             return
         elif c[0][0] == "-":
             VARIABLES[args[0]] = args[1] - args[2]
             return
         elif c[0][0] == "/":
             VARIABLES[args[0]] = args[1] / args[2]
             return
         elif c[0][0] == "*":
             VARIABLES[args[0]] = args[1] * args[2]
             return
         varlist = eval("builtin." + c[0][0] + "(args, VARIABLES, GLOBALS, runCommand)")
         VARIABLES = varlist
      else:
         if c[0][0] == ":":
             for f in FUNCTIONS[c[0][1]]:
                 runCommand(f)
         args = c[1:]
         argi = 0
         for a in args:
            if isinstance(a, list):
               if a[0] == "var":
                  args[argi] = VARIABLES[a[1]]
               elif a[0] == "global":
                  args[argi] = VARIABLES[a[1]]
            argi = argi + 1
         varlist = eval("MODULES[c[0][0]]." + c[0][1] + "(args, VARIABLES, GLOBALS, runCommand)")
         VARIABLES = varlist
    for c in j['program']:
        runCommand(c)
