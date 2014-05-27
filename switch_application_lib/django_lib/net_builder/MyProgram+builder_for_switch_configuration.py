#! /bin/env python

import os,re,copy
from net_builder.MyProgram.commons_utils import commons_utils as COMMONS_UTILS
from ip_manager.models import switch_configuration_urls, switch_network_usages, mgmt_network_ip_pools_for_cstack, mgmt_network_ip_pools_for_ostack, srv_network_ip_pools_for_cstack, srv_network_ip_pools_for_ostack


class TEST_SINGLE_7124SW(COMMONS_UTILS):

 def __init__(self,builder_class_name,input_datas_list):
  #################################################
  # initialize input variables                    #
  #################################################
  self.builder_class_name = builder_class_name
  self.input_datas_list = input_datas_list

  #################################################
  # shell script input arguments definition       #
  #################################################
  self.linux_args = "%(mgmt_swname)s %(mgmt_desc)s %(mgmt_ipnet)s %(gateway_ip)s"
  
  #################################################
  # display parameter, similar with @api_view     #
  #################################################
  self.selective_viewer = ['running_status', 'error_details', 'success_details']
  self.success_pattern = re.compile('success',re.I)


 def run(self):
  for input_data_dict in self.input_datas_list:
   requested_swname = input_data_dict['mgmt_swname']
   requested_mgmt_desc = input_data_dict['mgmt_desc']
   requested_mgmt_ipnet = input_data_dict['mgmt_ipnet']
   requested_gateway_ip = input_data_dict['gateway_ip']

   #################################################
   # confirmation of mgmt swname is                #
   #################################################
   if not self.mgmt_swname_usage_confirm_from_database('ip_manager',
                                                       'switch_configuration_urls',
                                                       requested_swname):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_swname)
    continue
   
   #################################################
   # confirmation for gateway ip address in        #
   #################################################
   ip_address_pool = self.get_ipaddress_list_from_network(requested_mgmt_ipnet)
   matched_gatewayip_pattern = re.compile(requested_gateway_ip.split('/')[0])
   gateway_status = False
   for ip_net in ip_address_pool:
    if matched_gatewayip_pattern.search(ip_net):
     gateway_status = True
     break
   if not gateway_status:
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s is not belonged to %s' % (requested_gateway_ip, requested_mgmt_ipnet)
    continue
   
   #################################################
   # shell commander and run the shell             #
   #################################################
   shell_arguments = self.linux_args % input_data_dict 
   shell_command = "%s %s" % (self.builder_class_name,shell_arguments)
   result_after_shell_execute = self.shell_command_exec(shell_command)
   if not self.success_pattern.search(result_after_shell_execute):   
    input_data_dict['running_status']=u'error'
    if result_after_shell_execute:
     input_data_dict['error_details']=result_after_shell_execute
    else:
     input_data_dict['error_details']=u'%s command is failed' % (self.builder_class_name)
    continue

   #################################################
   # database update processing                    #
   # switch_configuration_urls                     #
   #################################################
   switch_configuration_urls(mgmt_swname=input_data_dict['mgmt_swname'],
                             builder_name=self.builder_class_name,
                             url=result_after_shell_execute).save()

   ################################################
   # return value                                 #
   ################################################
   input_data_dict['running_status']=u'success'
   input_data_dict['success_details']=u'%s is completed' % (input_data_dict['mgmt_swname'])
   return self.select_viewer_items(self.input_datas_list,self.selective_viewer) 

 def detail_view(self,mgmtsw_name):
  return_result_dict = {}
  return_result_dict['running_status'] = 'sample'
  return return_result_dict
  
 def delete(self,mgmtsw_name):
  #############################################
  # database information remove               #
  # switch_configuration_urls                 #
  #############################################
  deleting_table_list = ['switch_configuration_urls']
  for table_name in deleting_table_list:
   self.delete_database_entry_matched_by_mgmt_swname('ip_manager',table_name,mgmtsw_name)
  #############################################
  # shell file remove                         #
  #############################################
  exec_command = "rm -rf /var/www/html/config/%s" % (mgmtsw_name)
  os.system(exec_command)
  result_dict = [{"running_status":"success","success_details":"deleted"}]
  return self.select_viewer_items(result_dict,self.selective_viewer)



class KR1B_CS_T2_7050S_NEX(COMMONS_UTILS):

 def __init__(self,builder_class_name,input_datas_list):
  #################################################
  # initialize input variables                    #
  #################################################
  self.builder_class_name = builder_class_name
  self.input_datas_list = input_datas_list

  #################################################
  # shell script input arguments definition       #
  #################################################
  self.linux_args = "%(mgmt_swname)s %(mgmt_desc_uptor)s %(mgmt_desc_downtor)s %(mgmt_network)s"
  self.extra_linux_args = "%(gateway_vip)s %(gateway_r1)s %(gateway_r2)s %(mgmtsw_mip)s %(upsrvsw_mip)s %(dnsrvsw_mip)s"

  #################################################
  # display parameter, similar with @api_view     #
  #################################################
  self.selective_viewer = ['running_status', 'error_details', 'success_details']
  self.success_pattern = re.compile('success',re.I)


 def run(self):
  for input_data_dict in self.input_datas_list:
   requested_swname = input_data_dict['mgmt_swname']
   requested_network = input_data_dict['mgmt_network']
   #################################################
   # confirmation of mgmt swname is                #
   #################################################
   if not self.mgmt_swname_usage_confirm_from_database('ip_manager',
                                                       'switch_configuration_urls',
                                                       requested_swname):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_swname)
    continue
   #################################################
   # get the ip address pool from network          #
   #################################################
   ip_address_pool = self.get_ipaddress_list_from_network(requested_network)
   if not ip_address_pool:
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has error' % (requested_network)
    continue
   #################################################
   # ip usage confirmation                         #
   #################################################
   if not self.ip_address_usage_confirm_from_database('ip_manager',
                                                      'mgmt_network_ip_pools_for_cstack',
                                                      ip_address_pool):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_network)
    continue
   #################################################
   # get the extra ip address to builder up        #
   #################################################
   extra_args={}
   extra_args['gateway_vip'] = ip_address_pool[-2]
   extra_args['gateway_r1'] = ip_address_pool[-3]
   extra_args['gateway_r2'] = ip_address_pool[-4]
   extra_args['mgmtsw_mip'] = ip_address_pool[-5]
   extra_args['upsrvsw_mip'] = ip_address_pool[-6]
   extra_args['dnsrvsw_mip'] = ip_address_pool[-7]
   #################################################
   # shell commander and run the shell             #
   #################################################
   shell_arguments = self.linux_args % input_data_dict +" "+ self.extra_linux_args % extra_args 
   shell_command = "%s %s" % (self.builder_class_name,shell_arguments)
   result_after_shell_execute = self.shell_command_exec(shell_command)
   if not self.success_pattern.search(result_after_shell_execute):   
    input_data_dict['running_status']=u'error'
    if result_after_shell_execute:
     input_data_dict['error_details']=result_after_shell_execute
    else:
     input_data_dict['error_details']=u'%s command is failed' % (self.builder_class_name)
    continue
   #################################################
   # database update processing                    #
   # switch_configuration_urls                     #
   # switch_network_usages                         # 
   # mgmt_network_ip_pools_for_cstack              #
   # mgmt_network_ip_pools_for_ostack              #
   # class srv_network_ip_pools_for_cstack         #
   # srv_network_ip_pools_for_ostack               #
   #################################################
   switch_configuration_urls(mgmt_swname=input_data_dict['mgmt_swname'],
                             builder_name=self.builder_class_name,
                             url=result_after_shell_execute).save()
   switch_network_usages(mgmt_swname=input_data_dict['mgmt_swname'],
                         mgmt_network=requested_network).save()

   for index in range(len(ip_address_pool)):
    if index == 0:
     useby_value='network'
    elif index == len(ip_address_pool)-1:
     useby_value='broadcast'
    else:
     useby_value=''
    mgmt_network_ip_pools_for_cstack(allocated_ip_address=ip_address_pool[index],
                                     mgmt_swname=input_data_dict['mgmt_swname'],
                                     usedby=useby_value).save()

   input_data_dict['running_status']=u'success'
   input_data_dict['success_details']=u'%s is completed' % (input_data_dict['mgmt_swname'])
  return self.select_viewer_items(self.input_datas_list,self.selective_viewer)
   
 def detail_view(self,mgmtsw_name):
  return_result_dict = {} 
  return_result_dict['running_status'] = 'success'
  return_result_dict['builder_name'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_configuration_urls','builder_name',mgmtsw_name)
  return_result_dict['url'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_configuration_urls','url',mgmtsw_name)
  return_result_dict['mgmt_network'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_network_usages','mgmt_network',mgmtsw_name)
  return_result_dict['srv_network'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_network_usages','srv_network',mgmtsw_name)
  return return_result_dict
  




 def delete(self,mgmtsw_name):
  #############################################
  # database information remove               #
  # switch_configuration_urls                 #
  # switch_network_usages                     #
  # mgmt_network_ip_pools_for_cstack          #
  # mgmt_network_ip_pools_for_ostack          #
  # srv_network_ip_pools_for_cstack           #
  # srv_network_ip_pools_for_ostack           #
  #############################################
  deleting_table_list = ['switch_configuration_urls', 
                         'switch_network_usages', 
                         'mgmt_network_ip_pools_for_cstack', 
                         'mgmt_network_ip_pools_for_ostack',
                         'srv_network_ip_pools_for_cstack',
                         'srv_network_ip_pools_for_ostack']
  for table_name in deleting_table_list:
   self.delete_database_entry_matched_by_mgmt_swname('ip_manager',table_name,mgmtsw_name)
  #############################################
  # shell file remove                         #
  #############################################
  exec_command = "rm -rf /var/www/html/config/%s" % (mgmtsw_name)
  os.system(exec_command)
  result_dict = [{"running_status":"success","success_details":"deleted"}]
  return self.select_viewer_items(result_dict,self.selective_viewer)


class KR1B_CS_T2_7050S_DELL(COMMONS_UTILS):

 def __init__(self,builder_class_name,input_datas_list):
  #################################################
  # initialize input variables                    #
  #################################################
  self.builder_class_name = builder_class_name
  self.input_datas_list = input_datas_list

  #################################################
  # shell script input arguments definition       #
  #################################################
  self.linux_args = "%(mgmt_swname)s %(mgmt_desc_uptor)s %(mgmt_desc_downtor)s %(mgmt_network)s"
  self.extra_linux_args = "%(gateway_vip)s %(gateway_r1)s %(gateway_r2)s %(mgmtsw_mip)s %(upsrvsw_mip)s %(dnsrvsw_mip)s"

  #################################################
  # display parameter, similar with @api_view     #
  #################################################
  self.selective_viewer = ['running_status', 'error_details', 'success_details']
  self.success_pattern = re.compile('success',re.I)


 def run(self):
  for input_data_dict in self.input_datas_list:
   requested_swname = input_data_dict['mgmt_swname']
   requested_network = input_data_dict['mgmt_network']
   #################################################
   # confirmation of mgmt swname is                #
   #################################################
   if not self.mgmt_swname_usage_confirm_from_database('ip_manager',
                                                       'switch_configuration_urls',
                                                       requested_swname):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_swname)
    continue
   #################################################
   # get the ip address pool from network          #
   #################################################
   ip_address_pool = self.get_ipaddress_list_from_network(requested_network)
   if not ip_address_pool:
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has error' % (requested_network)
    continue
   #################################################
   # ip usage confirmation                         #
   #################################################
   if not self.ip_address_usage_confirm_from_database('ip_manager',
                                                      'mgmt_network_ip_pools_for_cstack',
                                                      ip_address_pool):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_network)
    continue
   #################################################
   # get the extra ip address to builder up        #
   #################################################
   extra_args={}
   extra_args['gateway_vip'] = ip_address_pool[-2]
   extra_args['gateway_r1'] = ip_address_pool[-3]
   extra_args['gateway_r2'] = ip_address_pool[-4]
   extra_args['mgmtsw_mip'] = ip_address_pool[-5]
   extra_args['upsrvsw_mip'] = ip_address_pool[-6]
   extra_args['dnsrvsw_mip'] = ip_address_pool[-7]
   #################################################
   # shell commander and run the shell             #
   #################################################
   shell_arguments = self.linux_args % input_data_dict +" "+ self.extra_linux_args % extra_args 
   shell_command = "%s %s" % (self.builder_class_name,shell_arguments)
   result_after_shell_execute = self.shell_command_exec(shell_command)
   if not self.success_pattern.search(result_after_shell_execute):   
    input_data_dict['running_status']=u'error'
    if result_after_shell_execute:
     input_data_dict['error_details']=result_after_shell_execute
    else:
     input_data_dict['error_details']=u'%s command is failed' % (self.builder_class_name)
    continue
   #################################################
   # database update processing                    #
   # switch_configuration_urls                     #
   # switch_network_usages                         # 
   # mgmt_network_ip_pools_for_cstack              #
   # mgmt_network_ip_pools_for_ostack              #
   # class srv_network_ip_pools_for_cstack         #
   # srv_network_ip_pools_for_ostack               #
   #################################################
   switch_configuration_urls(mgmt_swname=input_data_dict['mgmt_swname'],
                             builder_name=self.builder_class_name,
                             url=result_after_shell_execute).save()
   switch_network_usages(mgmt_swname=input_data_dict['mgmt_swname'],
                         mgmt_network=requested_network).save()

   for index in range(len(ip_address_pool)):
    if index == 0:
     useby_value='network'
    elif index == len(ip_address_pool)-1:
     useby_value='broadcast'
    else:
     useby_value=''
    mgmt_network_ip_pools_for_cstack(allocated_ip_address=ip_address_pool[index],
                                     mgmt_swname=input_data_dict['mgmt_swname'],
                                     usedby=useby_value).save()

   input_data_dict['running_status']=u'success'
   input_data_dict['success_details']=u'%s is completed' % (input_data_dict['mgmt_swname'])
  return self.select_viewer_items(self.input_datas_list,self.selective_viewer)
   
 def detail_view(self,mgmtsw_name):
  return_result_dict = {} 
  return_result_dict['running_status'] = 'success'
  return_result_dict['builder_name'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_configuration_urls','builder_name',mgmtsw_name)
  return_result_dict['url'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_configuration_urls','url',mgmtsw_name)
  return_result_dict['mgmt_network'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_network_usages','mgmt_network',mgmtsw_name)
  return_result_dict['srv_network'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_network_usages','srv_network',mgmtsw_name)
  return return_result_dict
  




 def delete(self,mgmtsw_name):
  #############################################
  # database information remove               #
  # switch_configuration_urls                 #
  # switch_network_usages                     #
  # mgmt_network_ip_pools_for_cstack          #
  # mgmt_network_ip_pools_for_ostack          #
  # srv_network_ip_pools_for_cstack           #
  # srv_network_ip_pools_for_ostack           #
  #############################################
  deleting_table_list = ['switch_configuration_urls', 
                         'switch_network_usages', 
                         'mgmt_network_ip_pools_for_cstack', 
                         'mgmt_network_ip_pools_for_ostack',
                         'srv_network_ip_pools_for_cstack',
                         'srv_network_ip_pools_for_ostack']
  for table_name in deleting_table_list:
   self.delete_database_entry_matched_by_mgmt_swname('ip_manager',table_name,mgmtsw_name)
  #############################################
  # shell file remove                         #
  #############################################
  exec_command = "rm -rf /var/www/html/config/%s" % (mgmtsw_name)
  os.system(exec_command)
  result_dict = [{"running_status":"success","success_details":"deleted"}]
  return self.select_viewer_items(result_dict,self.selective_viewer)


class KR1B_CS_T2_7050S_NETAPP(COMMONS_UTILS):

 def __init__(self,builder_class_name,input_datas_list):
  #################################################
  # initialize input variables                    #
  #################################################
  self.builder_class_name = builder_class_name
  self.input_datas_list = input_datas_list

  #################################################
  # shell script input arguments definition       #
  #################################################
  self.linux_args = "%(mgmt_swname)s %(mgmt_desc_uptor)s %(mgmt_desc_downtor)s %(mgmt_network)s"
  self.extra_linux_args = "%(gateway_vip)s %(gateway_r1)s %(gateway_r2)s %(mgmtsw_mip)s %(upsrvsw_mip)s %(dnsrvsw_mip)s"

  #################################################
  # display parameter, similar with @api_view     #
  #################################################
  self.selective_viewer = ['running_status', 'error_details', 'success_details']
  self.success_pattern = re.compile('success',re.I)


 def run(self):
  for input_data_dict in self.input_datas_list:
   requested_swname = input_data_dict['mgmt_swname']
   requested_network = input_data_dict['mgmt_network']
   #################################################
   # confirmation of mgmt swname is                #
   #################################################
   if not self.mgmt_swname_usage_confirm_from_database('ip_manager',
                                                       'switch_configuration_urls',
                                                       requested_swname):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_swname)
    continue
   #################################################
   # get the ip address pool from network          #
   #################################################
   ip_address_pool = self.get_ipaddress_list_from_network(requested_network)
   if not ip_address_pool:
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has error' % (requested_network)
    continue
   #################################################
   # ip usage confirmation                         #
   #################################################
   if not self.ip_address_usage_confirm_from_database('ip_manager',
                                                      'mgmt_network_ip_pools_for_cstack',
                                                      ip_address_pool):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s network has been already used' % (requested_network)
    continue
   #################################################
   # get the extra ip address to builder up        #
   #################################################
   extra_args={}
   extra_args['gateway_vip'] = ip_address_pool[-2]
   extra_args['gateway_r1'] = ip_address_pool[-3]
   extra_args['gateway_r2'] = ip_address_pool[-4]
   extra_args['mgmtsw_mip'] = ip_address_pool[-5]
   extra_args['upsrvsw_mip'] = ip_address_pool[-6]
   extra_args['dnsrvsw_mip'] = ip_address_pool[-7]
   #################################################
   # shell commander and run the shell             #
   #################################################
   shell_arguments = self.linux_args % input_data_dict +" "+ self.extra_linux_args % extra_args 
   shell_command = "%s %s" % (self.builder_class_name,shell_arguments)
   result_after_shell_execute = self.shell_command_exec(shell_command)
   if not self.success_pattern.search(result_after_shell_execute):   
    input_data_dict['running_status']=u'error'
    if result_after_shell_execute:
     input_data_dict['error_details']=result_after_shell_execute
    else:
     input_data_dict['error_details']=u'%s command is failed' % (self.builder_class_name)
    continue
   #################################################
   # database update processing                    #
   # switch_configuration_urls                     #
   # switch_network_usages                         # 
   # mgmt_network_ip_pools_for_cstack              #
   # mgmt_network_ip_pools_for_ostack              #
   # class srv_network_ip_pools_for_cstack         #
   # srv_network_ip_pools_for_ostack               #
   #################################################
   switch_configuration_urls(mgmt_swname=input_data_dict['mgmt_swname'],
                             builder_name=self.builder_class_name,
                             url=result_after_shell_execute).save()
   switch_network_usages(mgmt_swname=input_data_dict['mgmt_swname'],
                         mgmt_network=requested_network).save()

   for index in range(len(ip_address_pool)):
    if index == 0:
     useby_value='network'
    elif index == len(ip_address_pool)-1:
     useby_value='broadcast'
    else:
     useby_value=''
    mgmt_network_ip_pools_for_cstack(allocated_ip_address=ip_address_pool[index],
                                     mgmt_swname=input_data_dict['mgmt_swname'],
                                     usedby=useby_value).save()

   input_data_dict['running_status']=u'success'
   input_data_dict['success_details']=u'%s is completed' % (input_data_dict['mgmt_swname'])
  return self.select_viewer_items(self.input_datas_list,self.selective_viewer)
   
 def detail_view(self,mgmtsw_name):
  return_result_dict = {} 
  return_result_dict['running_status'] = 'success'
  return_result_dict['builder_name'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_configuration_urls','builder_name',mgmtsw_name)
  return_result_dict['url'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_configuration_urls','url',mgmtsw_name)
  return_result_dict['mgmt_network'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_network_usages','mgmt_network',mgmtsw_name)
  return_result_dict['srv_network'] = self.get_items_list_from_database_matched_by_mgmt_swname('ip_manager','switch_network_usages','srv_network',mgmtsw_name)
  return return_result_dict
  




 def delete(self,mgmtsw_name):
  #############################################
  # database information remove               #
  # switch_configuration_urls                 #
  # switch_network_usages                     #
  # mgmt_network_ip_pools_for_cstack          #
  # mgmt_network_ip_pools_for_ostack          #
  # srv_network_ip_pools_for_cstack           #
  # srv_network_ip_pools_for_ostack           #
  #############################################
  deleting_table_list = ['switch_configuration_urls', 
                         'switch_network_usages', 
                         'mgmt_network_ip_pools_for_cstack', 
                         'mgmt_network_ip_pools_for_ostack',
                         'srv_network_ip_pools_for_cstack',
                         'srv_network_ip_pools_for_ostack']
  for table_name in deleting_table_list:
   self.delete_database_entry_matched_by_mgmt_swname('ip_manager',table_name,mgmtsw_name)
  #############################################
  # shell file remove                         #
  #############################################
  exec_command = "rm -rf /var/www/html/config/%s" % (mgmtsw_name)
  os.system(exec_command)
  result_dict = [{"running_status":"success","success_details":"deleted"}]
  return self.select_viewer_items(result_dict,self.selective_viewer)

