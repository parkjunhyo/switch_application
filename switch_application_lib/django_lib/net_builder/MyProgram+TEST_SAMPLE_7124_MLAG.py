#! /bin/env python

import os,re,copy
from net_builder.MyProgram.commons_utils import commons_utils as COMMONS_UTILS
from ip_manager.models import switch_configuration_urls, switch_network_usages, mgmt_network_ip_pools_for_cstack, mgmt_network_ip_pools_for_ostack, srv_network_ip_pools_for_cstack, srv_network_ip_pools_for_ostack

class TEST_SAMPLE_7124_MLAG(COMMONS_UTILS):
 
 def __init__(self,builder_class_name,input_datas_list):
  #################################################
  # initialize input variables                    #
  #################################################
  self.builder_class_name = builder_class_name
  self.input_datas_list = input_datas_list

  #################################################
  # shell script input arguments definition       #
  #################################################
  # self.linux_args = "%(mgmt_swname)s %(mgmt_desc_uptor)s %(mgmt_desc_downtor)s %(mgmt_ip_uptor)s %(mgmt_ip_downtor)s %(mgmt_gateway_vip)s"
  self.linux_args = "%(mgmt_swname)s %(mgmt_portno_uptor)s %(mgmt_portno_downtor)s %(mgmt_ip_uptor)s %(mgmt_ip_downtor)s %(mgmt_gateway_vip)s"

  #################################################
  # display parameter, similar with @api_view     #
  #################################################
  self.selective_viewer = ['running_status', 'error_details', 'success_details']
  self.success_pattern = re.compile('success',re.I)

 def run(self):
  for input_data_dict in self.input_datas_list:
   requested_swname = input_data_dict['mgmt_swname']
   requested_mgmt_ip_uptor = input_data_dict['mgmt_ip_uptor']
   requested_mgmt_ip_downtor = input_data_dict['mgmt_ip_downtor']
   requested_mgmt_gateway_vip = input_data_dict['mgmt_gateway_vip']

   #################################################
   # Port Number extraction (only number string)   #
   #################################################
   Ethernet_pattern=re.compile("Ethernet",re.I)
   Dash_pattern=re.compile("/",re.I)
   requested_mgmt_portno = ['mgmt_portno_uptor','mgmt_portno_downtor']
   for mgmt_portno in requested_mgmt_portno:
    Ethernet_number = re.split(Ethernet_pattern,input_data_dict[mgmt_portno])[-1]
    input_data_dict[mgmt_portno] = re.split(Dash_pattern,Ethernet_number)[-1]

   #################################################
   # confirmation of mgmt swname is                #
   #################################################
   if not self.mgmt_swname_usage_confirm_from_database('ip_manager',
                                                       'switch_configuration_urls',
                                                       requested_swname):
    input_data_dict['running_status']=u'error'
    input_data_dict['error_details']=u'%s has been already used' % (requested_swname)
    continue

   #################################################
   # confirmation for gateway ip address in        #
   #################################################
   ip_address_pool = self.get_ipaddress_list_from_network(requested_mgmt_ip_uptor)
   matched_gatewayip_pattern = re.compile(requested_mgmt_gateway_vip.split('/')[0])
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
