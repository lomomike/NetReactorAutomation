import sys
import os
import re
import subprocess
from datetime import datetime


reactorPath = '"C:\Program Files (x86)\Eziriz\.NET Reactor\dotNET_Reactor.exe"'


def usage():
   filename = os.path.split(sys.argv[0])[-1]
   print filename + " <directory>"
   

def findexe(files):
   for file in files:
       if(file.endswith('.exe')):
           return file
   return None


def filter(filename):
   patterns = [
       r'^.*txt$',
       r'^.*udl$',
       r'^.*config$',
       r'.*HaspProtect.*',
       r'log4net.dll',
       r'^DevExpress',
       r'^FastReport',
       r'^System',
       r'IconsLib.dll',
       r'Transnavi.RemotingDll.dll',
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


def deletehash(path):
   for (this, inDirs, files) in os.walk(path):
       for filename in files:
           if filename.endswith('.hash') : os.remove(os.path.join(path, filename))


def addtargetfile(path, exefile):
   return '-file "' + os.path.join(path, exefile) + '"'


def addsatelites(path, satelites):
   line = '-satellite_assemblies "'
   for dll in satelites:
       libpath = os.path.join(path, dll)
       line += libpath + "/"
   return line[:-1] + '"'


def addaditionalparams():
   return '-suppressildasm 0 -obfuscation 0 -necrobit 1 -stringencryption 1 -targetfile "<AssemblyLocation>\<AssemblyFileName>"'


def formcommandline(path, exefile, satelites):
   commandline = reactorPath + " " + \
   addtargetfile(path, exefile) + " " + \
   addsatelites(path, satelites) + " " +\
   addaditionalparams()

   return commandline


def main(path):
   print "Protection started..."
   print datetime.now()
   
   filelist = formfileslist(path)
 
   exefile = findexe(filelist)
   
   if not exefile:
       return 1
   else:
       filelist.remove(exefile)

   command = formcommandline(path, exefile, filelist)
   
   #print command
   subprocess.call(command)

   deletehash(path)
   
   print "Protection completed."
   print datetime.now()   

if __name__ == "__main__":
   if len(sys.argv) < 2:
       usage()
   else:
       main(sys.argv[1])
