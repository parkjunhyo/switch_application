#! /bin/env python

import os,re,copy
from netaddr import *
from switch_application.settings import DATABASES as DB_CONNECT_INFO

django_database_name = DB_CONNECT_INFO['default']['NAME']
django_database_user = DB_CONNECT_INFO['default']['USER']
django_database_pass = DB_CONNECT_INFO['default']['PASSWORD']

class commons_utils:

 def get_ipaddress_list_from_network(self,requested_network):
  IP_address_pool = []
  try:
   IP_network = IPNetwork(requested_network)
   IP_subnet = str(IP_network.prefixlen)
  except:
   ######################################
   # IP network is not collect format   #
   ######################################
   return IP_address_pool
  #######################################
  # IP address list generation          #
  #######################################
  for IPaddress in list(IP_network):
   if str(IPaddress) not in IP_address_pool:
    IP_address_pool.append(str(IPaddress).strip())
  return IP_address_pool

 def ip_address_usage_confirm_from_database(self,application_name,database_model_name,ip_address_pool):
  database_name_to_access = "%s.%s_%s" % (django_database_name,application_name,database_model_name)
  print database_name_to_access
