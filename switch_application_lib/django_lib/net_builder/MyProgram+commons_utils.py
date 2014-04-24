#! /bin/env python

import os,re,copy,MySQLdb
from netaddr import *
from switch_application.settings import DATABASES as DB_CONNECT_INFO

django_database_name = DB_CONNECT_INFO['default']['NAME']
django_database_user = DB_CONNECT_INFO['default']['USER']
django_database_pass = DB_CONNECT_INFO['default']['PASSWORD']
django_database_host = DB_CONNECT_INFO['default']['HOST']

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
    re_IPaddress = "%s/%s" % (str(IPaddress).strip(),IP_subnet)
    IP_address_pool.append(re_IPaddress)
  return IP_address_pool

 def database_connect(self):
  try:
   open_db = MySQLdb.connect(django_database_host,django_database_user,django_database_pass)
   try:
    open_cursor = open_db.cursor()
   except:
    open_db.close()
    return False, False
  except:
   return False, False
  return open_db,open_cursor

 def database_disconnect(self, open_db, open_cursor):
  open_cursor.close()
  open_db.close()


 def ip_address_usage_confirm_from_database(self,application_name,database_model_name,ip_address_pool):
  database_name_to_access = "%s.%s_%s" % (django_database_name,application_name,database_model_name)
  query_msg = "select allocated_ip_address from %s" % (database_name_to_access)
  open_db, open_cursor = self.database_connect()
  ######################################
  # if database connection fail        #
  ######################################
  if not open_cursor:
   return False
  ######################################
  # send the query message to database #
  ######################################
  open_cursor.execute(query_msg)
  result_from_database = open_cursor.fetchall()
  self.database_disconnect(open_db, open_cursor)

  re_arrange_result_from_database = []
  for result_tupletype in result_from_database:
   item_value = result_tupletype[0].strip()
   if item_value not in re_arrange_result_from_database: 
    re_arrange_result_from_database.append(item_value)
  
  ######################################
  # ip usage confirm                   #
  ###################################### 
  for ip_addr_element in ip_address_pool:
   if ip_addr_element in re_arrange_result_from_database:
    return False
  ######################################
  # return                             #
  ######################################
  return True

 def mgmt_swname_usage_confirm_from_database(self,application_name,database_model_name,requested_swname):
  database_name_to_access = "%s.%s_%s" % (django_database_name,application_name,database_model_name)
  query_msg = "select mgmt_swname from %s" % (database_name_to_access)
  open_db, open_cursor = self.database_connect()
  if not open_cursor:
   return False
  open_cursor.execute(query_msg)
  result_from_database = open_cursor.fetchall()
  self.database_disconnect(open_db, open_cursor)

  re_arrange_result_from_database = []
  for result_tupletype in result_from_database:
   item_value = result_tupletype[0].strip() 
   if item_value not in re_arrange_result_from_database:
    re_arrange_result_from_database.append(item_value)
  ######################################
  # mgmt_name usage confirm            #
  ######################################
  if requested_swname in re_arrange_result_from_database:
   return False
  return True


 def shell_command_exec(self, shell_command):
  run_result = os.popen(shell_command)
  complete_status = ''
  result_msg = run_result.readline()
  while result_msg:
   complete_status = result_msg.strip()
   result_msg = run_result.readline()
  return complete_status


 def select_viewer_items(self,input_datas_list,selective_viewer):
  local_values = copy.copy(input_datas_list)
  for local_value in local_values:
   for key_name in local_value.keys():
    if key_name not in selective_viewer:
     del local_value[key_name]
  return local_values
