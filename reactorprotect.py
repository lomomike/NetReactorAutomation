import sys
import os
import re

reactorPath = '"C:\Program Files (x86)\Eziriz\.NET Reactor\dotNET_Reactor.Console.exe"'

def usage():
    filename = os.path.split(sys.argv[0])[-1]
    print filename + " <directory>"

def findexe(files):
    for file in files:
        if(file.endswith('.exe')):
            return file
    return None;

def filter(filename):
    patterns = [
        r'^.*udl$',
        r'^.*config$',
        r'.*HaspProtect.*',
        r'log4net.dll',
        r'^DevExpress',
    ]

    for pattern in patterns:
        if(re.findall(pattern, filename, re.IGNORECASE)):
            return False
    return True


def formfileslist(path):
    filetoprocess = []
    for (this, inDirs, files) in os.walk(path):
        for filename in files:
            if filter(filename):
                filetoprocess.append(filename)
    return filetoprocess


def addtargetfile(path, exefile):
    exepath = '"' + os.path.join(path, exefile) + '"'
    return "-file %s -targetfile %s" % (exepath, exepath)


def addsatelites(path, satelites):
    return ""


def addaditionalparams():
    return ""

def formcommandline(path, exefile, satelites):
    commandline = reactorPath + " " + \
    addtargetfile(path, exefile) + " " + \
    addsatelites(path, satelites) + " " +\
    addaditionalparams()

    return commandline



def main(path):
    filelist = formfileslist(path)
  
    exefile = findexe(filelist)
    if not exefile:
        return 1
    else:
        filelist.remove(exefile)

    for filename in filelist:
        print filename
    print

    print formcommandline(path, exefile, filelist)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
    else:
        main(sys.argv[1])

  