#! /bin/env python

import os,re,copy

class KR1B_CS_T2_7050S_NEX:

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

