#!/usr/bin/python
import os, re, subprocess, sys, urllib, string, Tac, EntityManager
sys.stdout

# This points to the ZTP server, change the IP address to match the server

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


def mountEntity( sysdb, *args, **kwargs ):
   mg = sysdb.mountGroup()
   entity = mg.mount( *args, **kwargs )
   mg.close( blocking=True )
   return entity

# Mount lldpStatus from sysdb
def mountSysdb():
   global lldpStatus
   sysname = os.environ.get( "SYSNAME", "ar" )
   sysdb = EntityManager.Sysdb( sysname=sysname )
   try:
      swiVersionSplit = map(int, swiversion.split( '.' ))
      #Added this check to account for Sysdb change in 4.12.0
      if swiVersionSplit[0] == 4 and swiVersionSplit[1] > 11:
         lldpStatus = mountEntity( sysdb, 
					   "l2discovery/lldp/status/all",
					   "Lldp::AllStatus", "r" )
      elif swiVersionSplit[0] == 4 and swiVersionSplit[1] < 12:
          lldpStatus = mountEntity( sysdb, 
					   "l2discovery/lldp/status",
					   "Lldp::Status", "r" )
   except e:
		printLog ('Failed to mount lldpStatus, Sysdb may have changed structure')
		sys.exit( 1 )

   if not lldpStatus:
         printLog( 'Failed to mount lldpStatus' )
         sys.exit( 1 )

def escapedString( origString ):
   """Return the origString with all non-printable characters escaped
   with the exception of a null byte terminator, which is stripped"""
   # we strip terminating NUL characters because some buggy 
   # D-Link switches transmit them
   s = []
   for char in origString.rstrip( '\0' ):
      if char in string.printable:
         s.append( char )
      else:
         s.append( "\\x%02x" % ord( char ) )
   return ''.join( s )

def getNeighPortDescription( intf ):   
   portStatus = lldpStatus.portStatus.get( intf )
   if not portStatus:
      return None
   remoteSystems = portStatus.remoteSystem.items()
   for (rs, obj) in remoteSystems:
      if obj.portId:
         return escapedString( obj.portId )
   return None


def getNeighPortName( intf ):
   portStatus = lldpStatus.portStatus.get( intf )
   if not portStatus:
      return None
   remoteSystems = portStatus.remoteSystem.items()
   for (rs, obj) in remoteSystems:
      if obj.portDesc:
         return escapedString( obj.portDesc )
   return None

   
def getNeighDeviceDescription( intf ):   
   portStatus = lldpStatus.portStatus.get( intf )
   if not portStatus:
      return None
   remoteSystems = portStatus.remoteSystem.items()
   for (rs, obj) in remoteSystems:
      if obj.sysName:
         return escapedString( obj.sysName )
   return None
   
mountSysdb()

# Get neighbor device and portid for Ma1
neighDevice = getNeighDeviceDescription('Management1')
neighPort = getNeighPortDescription('Management1')
neighPortifname = getNeighPortName('Management1')

## printLog( "-------------- variable status log -------------" )
## printLog( neighDevice )
## printLog( neighPort )
## printLog( neighPortifname )
## printLog( "------------------------------------------------" )

def regen_name(in_string):
 m = []
 r_list = in_string.split('-')
 for element in r_list:
  m = m+element.split('_')
 re_name = '-'.join(m)
 location_pattern='[QqRr]*\d+[QqRr]\d+[QqRr]*'
 if re.search(location_pattern,re_name):
  match_item=re.search(location_pattern,re_name).group()
  re_name=re_name.split(match_item)[0]+match_item
 return re_name


# redifine the information for download the configuration
mgmt_hostname = regen_name(neighDevice.split(r".")[0])
tor_hostname = regen_name(neighPort)
tor_mgmt_desc=mgmt_hostname+"-G"+neighPortifname.split(r"t")[-1]


tor_config_name=neighPort.split()[0]
configUrl = "http://20.0.2.224/config/%s/%s"
parsedUrl = configUrl % ( mgmt_hostname, tor_config_name )

# Download the config to flash
# Check if the switch is in the database.
if not urllib.urlopen( parsedUrl ).read() == "Device not found":
	urllib.urlretrieve(parsedUrl, '/mnt/flash/pre-startup-config')
else:
	printLog( "Device not in the database, exiting" ) 
	sys.exit( 1 )

# change the TOR MGMT Description
# change the TOR Host NAME CHANGE_HOSTNAME
startup_conf="/mnt/flash/startup-config"
pre_startup_conf="/mnt/flash/pre-startup-config"

pattern_string1=re.compile("CHANGE_MGMT_DESC")
pattern_string2=re.compile("CHANGE_HOSTNAME")

startup_f=open(startup_conf,'w')
prestartup_f=open(pre_startup_conf,'r')
r_msg=prestartup_f.readline()
while r_msg:
 if re.search('CHANGE_MGMT_DESC',r_msg):
  r_msg=pattern_string1.sub(tor_mgmt_desc,r_msg)

 if re.search('CHANGE_HOSTNAME',r_msg):
  r_msg=pattern_string2.sub(tor_hostname,r_msg)

 startup_f.write(r_msg)
 r_msg=prestartup_f.readline()
prestartup_f.close()
startup_f.close()
os.remove(pre_startup_conf)


# download upgrade_os.py
configUrl = "http://20.0.2.224/%s"
parsedUrl = configUrl % ( 'upgrade_os.py' )
# Check if the switch is in the database.
if not urllib.urlopen( parsedUrl ).read() == "Device not found":
        urllib.urlretrieve(parsedUrl, '/mnt/flash/upgrade_os.py')
else:
        printLog( "Device not in the database, exiting" )
        sys.exit( 1 )

sys.exit()


