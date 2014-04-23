from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from net_builder.MyProgram.templates_list import templates_list as TEMPLATES_LIST
from net_builder.MyProgram.builder_urls import builder_urls as BUILDER_URLS
import types,os,sys

################################################################################
# function : show_config_templates_list                                        #
################################################################################
@csrf_exempt
@api_view(['GET'])
def show_config_templates_list(request):
 if request.method == 'GET':

  if request.content_type == 'text/plain':
   if request.QUERY_PARAMS:
    #############################################################################
    # curl http://192.168.42.135:8080/net_builder/config_templates/?name=junhyo #
    # http://192.168.42.135:8080/net_builder/config_templates/?name=junhyo      #
    # request.QUERY_PARAMS : <QueryDict: {u'name': [u'junhyo']}>                #
    # data = JSONRenderer().render(request.QUERY_PARAMS)                        #
    # data : {"name": "junhyo"}                                                 #
    # data(type) : <type 'str'>                                                 # 
    # return Response(data)                                                     #
    # data = [{"name": "junhyo"}]  : [{"name": "junhyo"}], curl, web is OK      #
    # data = {"name": "junhyo"}    : {"name": "junhyo"},   curl, web is OK      #
    #############################################################################
    return Response(status=status.HTTP_400_BAD_REQUEST)
   # return 
   return Response(TEMPLATES_LIST)

  else: ## end of if request.content_type == 'text/plain':
   return Response(status=status.HTTP_400_BAD_REQUEST)

 else: ## end of if request.method == 'GET':
  return Response(status=status.HTTP_400_BAD_REQUEST)

################################################################################
# function : show_config_templates_details                                     #
################################################################################
def get_matched_templates_by_template_id(template_id):
 try:
  for dictionary_item in TEMPLATES_LIST:
   if dictionary_item['id'] == int(template_id):
    return [ dictionary_item ]
    break
 except:
  raise Http404
 else:
  raise Http404

def dictionary_key_is_fully_occupied(template_id,input_datas_list):
 compare_key_name_list = []
 try:
  for dictionary_item in TEMPLATES_LIST:
   if dictionary_item['id'] == int(template_id):
    compare_key_name_list = dictionary_item['params']
    break
 except:
  raise Http404

 not_perfect_component = []
 if compare_key_name_list:
  for input_data_dict in input_datas_list:
   for key_name in compare_key_name_list:
    if key_name not in input_data_dict.keys():
     input_data_dict['running_status']=u'error'
     input_data_dict['error_details']='%s parameter is not matched!' % (key_name)
     not_perfect_component.append(input_data_dict)
     break
  return not_perfect_component
 else:
  raise Http404

def get_builder_class_by_template_id(template_id):
 try:
  for dictionary_item in TEMPLATES_LIST:
   if dictionary_item['id'] == int(template_id):
    builder_class_name = dictionary_item['builder']
    builder_class = BUILDER_URLS[builder_class_name]
    return builder_class_name, builder_class
    break
 except:
  raise Http404
 else:
  raise Http404

@csrf_exempt
@api_view(['GET','POST'])
def show_config_templates_details(request, template_id):

 if request.method == 'GET':
  if request.content_type == 'text/plain':
   if request.QUERY_PARAMS:
    return Response(status=status.HTTP_400_BAD_REQUEST)
   ########################################################################
   # matched_templates_details : type 'list', elements are dictionary     #
   ########################################################################
   matched_by_template_id_templates_details = get_matched_templates_by_template_id(template_id)
   return Response(matched_by_template_id_templates_details)
  else:
   return Response(status=status.HTTP_400_BAD_REQUEST)

 elif request.method == 'POST':
  
  if request.content_type == 'application/json':
   #########################################################################################################################################
   # curl -X POST http://192.168.42.135:8080/net_builder/config_templates/1/ -d '[{"name":"junhyo"}]' -H "Content-Type: application/json"  #
   # print request.POST : only form-data 
   # print request.DATA
   ##############################################################################################################
   input_datas_list = request.DATA
   if type(input_datas_list) != types.ListType:
    return Response([{"running_status":"error","error_details":"POST inputs should be list format"}])
   
   ## error input parameters
   not_perfect_component = dictionary_key_is_fully_occupied(template_id,input_datas_list)
   if not_perfect_component:
    return Response(not_perfect_component)

   ##########################################################################
   # from now, run linux shell script                                       #
   ##########################################################################
   builder_class_name, builder_class = get_builder_class_by_template_id(template_id)
   builder_instance = builder_class(builder_class_name,input_datas_list)
   builder_instance.run()
   return Response(input_datas_list)
  else:
   return Response(status=status.HTTP_400_BAD_REQUEST)


