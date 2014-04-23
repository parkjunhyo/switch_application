#! /bin/env python

import os,re,copy
from net_builder.MyProgram.commons_utils import commons_utils as COMMONS_UTILS

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
   requested_network = input_data_dict['mgmt_network']
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
    input_data_dict['error_details']=result_after_shell_execute
    continue
   #################################################
   # shell commander and run the shell             #
   #################################################

   
   input_data_dict['running_status']=u'success'
   input_data_dict['success_details']=u'completed'
  return self.input_datas_list
   

