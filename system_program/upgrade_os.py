#!/usr/bin/python
import os, re, subprocess, sys, urllib, string, Tac, EntityManager
sys.stdout

if len(sys.argv) != 2:
 print sys.argv[0]+" requres [os image name]"
 sys.exit()

osimage_name=sys.argv[1]
configUrl = "http://20.0.2.224/os/%s"
parsedUrl = configUrl % ( osimage_name )

# Look at the boot-config file and get the currently set EOS version
fd = open("/etc/swi-version", "r")
for item in fd:
   if "SWI_VERSION=" in item:
      swiversion = item.strip('SWI_VERSION=|\n')
fd.close()

#This allows output to the console during boot time
def printLog( logmsg ):
    print logmsg
    os.system( '/usr/bin/logger -p local4.crit -t ZeroTouch %s' % logmsg )


ret = urllib.urlopen(parsedUrl)
updateBootConfig = False

if int(ret.info()['content-length']) < 2048:
 printLog('there is no os images or permission to download')
 sys.exit()
else:
 if ret.info()['content-type'] == 'application/vnd.aristanetworks.swi':
  if not os.path.isfile('/mnt/flash/%s' % osimage_name):
   download = True
  else:
   download = False
   updateBootConfig = True
   printLog(osimage_name+' already existed in /mnt/flash')
  # download processing
  if download == True:
   swiSize = ret.info()['content-length']
   urllib.urlretrieve(parsedUrl, '/mnt/flash/%s' % osimage_name)
   printLog('download url = %s' % parsedUrl)
   localFileSize = str(os.stat('/mnt/flash/%s' % osimage_name).st_size)
   if swiSize == localFileSize:
    printLog ('Downloaded %s' % osimage_name)
    updateBootConfig = True
   else:
    printLog ('Download failed, exiting')
    updateBootConfig = False
 else:
  printLog('this image is not os image, content-type is wrong')
  sys.exit()
 
ret.close()

# Change the boot-config file to new version
if updateBootConfig:
    fd = open("/mnt/flash/boot-config", "w")
    fd.write("SWI=flash:%s\n\n" % osimage_name)
    fd.close()

sys.exit()
