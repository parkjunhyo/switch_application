from django.shortcuts import render

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from django.http import Http404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.decorators import authentication_classes
from rest_framework.response import Response
from django.http import Http404

from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated

from net_builder.MyProgram.templates_list import templates_list as TEMPLATES_LIST
from net_builder.MyProgram.builder_urls import builder_urls as BUILDER_URLS
import types,os,sys
from rest_framework.compat import BytesIO
from switch_application.settings import DATABASES as DB_CONNECT_INFO
import MySQLdb

################################################################################
# function : show_config_templates_list                                        #
################################################################################
@csrf_exempt
@api_view(['GET'])
################################################################################
# authentication                                                               #
################################################################################
@authentication_classes((SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication))
# @authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
################################################################################
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
    #############################################################################
    # content = JSONRenderer().render(request.QUERY_PARAMS)                     #
    # stream = BytesIO(content)                                                 #
    # data = JSONParser().parse(stream)                                         #
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

#@csrf_exempt
#@api_view(['GET','POST'])
#def show_config_templates_details(request, template_id):
#
# if request.method == 'GET':
#  if request.content_type == 'text/plain':
#   if request.QUERY_PARAMS:
#    return Response(status=status.HTTP_400_BAD_REQUEST)
#   ########################################################################
#   # matched_templates_details : type 'list', elements are dictionary     #
#   ########################################################################
#   matched_by_template_id_templates_details = get_matched_templates_by_template_id(template_id)
#   return Response(matched_by_template_id_templates_details)
#  else:
#   return Response(status=status.HTTP_400_BAD_REQUEST)
#
# elif request.method == 'POST':
#  
#  if request.content_type == 'application/json':
#   #########################################################################################################################################
#   # curl -X POST http://192.168.42.135:8080/net_builder/config_templates/1/ -d '[{"name":"junhyo"}]' -H "Content-Type: application/json"  #
#   # print request.POST : only form-data 
#   # print request.DATA
#   #########################################################################################################################################
#   input_datas_list = request.DATA
#   if type(input_datas_list) == types.DictType:
#    input_datas_list = [ input_datas_list ]
#   elif type(input_datas_list) != types.ListType:
#    return Response([{"running_status":"error","error_details":"POST inputs should be list format"}])
#   
#   ## error input parameters
#   not_perfect_component = dictionary_key_is_fully_occupied(template_id,input_datas_list)
#   if not_perfect_component:
#    return Response(not_perfect_component)
#
#   ##########################################################################
#   # from now, run linux shell script                                       #
#   ##########################################################################
#   builder_class_name, builder_class = get_builder_class_by_template_id(template_id)
#   builder_instance = builder_class(builder_class_name,input_datas_list)
#   builder_instance.run()
#   return Response(input_datas_list)
#  else:
#   return Response(status=status.HTTP_400_BAD_REQUEST)



class show_config_templates_details(APIView):

 authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
 # authentication_classes = (SessionAuthentication, BasicAuthentication)
 permission_classes = (IsAuthenticated,)
 #############################################################################################
 # default by http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions #
 #############################################################################################
 # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)                             #
 #############################################################################################

 @csrf_exempt
 def get(self, request, template_id, format=None):
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

 @csrf_exempt
 def post(self, request, template_id, format=None):

  content = {'user': unicode(request.user),'auth': unicode(request.auth)}

  if request.content_type == 'application/json':
   #########################################################################################################################################
   # curl -X POST http://192.168.42.135:8080/net_builder/config_templates/1/ -d '[{"name":"junhyo"}]' -H "Content-Type: application/json"  #
   # print request.POST : only form-data
   # print request.DATA
   ##############################################################################################################
   input_datas_list = request.DATA
   if type(input_datas_list) == types.DictType:
    input_datas_list = [ input_datas_list ]
   elif type(input_datas_list) != types.ListType:
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



################################################################################
# function : show_mgmtsw_list                                                  #
################################################################################
def database_connect():
 ##### Access information to Database
 django_database_user = DB_CONNECT_INFO['default']['USER']
 django_database_pass = DB_CONNECT_INFO['default']['PASSWORD']
 django_database_host = DB_CONNECT_INFO['default']['HOST']

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

def database_disconnect(open_db,open_cursor):
 open_cursor.close()
 open_db.close()

@csrf_exempt
@api_view(['GET'])
#####################################################################
# authentication                                                    #
#####################################################################
@authentication_classes((SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication))
# @authentication_classes((SessionAuthentication, BasicAuthentication))
@permission_classes((IsAuthenticated,))
#####################################################################
def show_mgmtsw_list(request):

 if request.method == 'GET':
  if request.content_type == 'text/plain':
   if request.QUERY_PARAMS:
    return Response(status=status.HTTP_400_BAD_REQUEST)
   #############################################
   # database model information                #
   # switch_configuration_urls                 #
   # switch_network_usages                     #
   # mgmt_network_ip_pools_for_cstack          #
   # mgmt_network_ip_pools_for_ostack          #
   # srv_network_ip_pools_for_cstack           #
   # srv_network_ip_pools_for_ostack           #
   #############################################
   django_database_host = DB_CONNECT_INFO['default']['NAME']
   query_msg = "select mgmt_swname,builder_name,url from %s.%s_%s;" % (django_database_host,'ip_manager','switch_configuration_urls')
   open_db,open_cursor = database_connect()
   if not open_cursor:
    return Response(status=status.HTTP_400_BAD_REQUEST)
   open_cursor.execute(query_msg)
   query_results = open_cursor.fetchall()
   database_disconnect(open_db,open_cursor)
   #############################################
   # re arrange to display                     #
   #############################################
   mgmtsw_list = []
   for result_tuple in query_results:
    mgmtsw_list.append({'mgmt_swname':result_tuple[0],'builder_name':result_tuple[1],'url':result_tuple[2]})
   return Response(mgmtsw_list)

  else: ## end of if request.content_type == 'text/plain':
   return Response(status=status.HTTP_400_BAD_REQUEST)
 else: ## end of if request.method == 'GET':
  return Response(status=status.HTTP_400_BAD_REQUEST)


################################################################################
# function : show_mgmtsw_details                                               #
################################################################################
def get_builder_class_by_mgmt_swname(mgmt_swname):
 django_database_host = DB_CONNECT_INFO['default']['NAME']
 query_msg = "select builder_name from %s.%s_%s where mgmt_swname=\'%s\';" % (django_database_host,'ip_manager','switch_configuration_urls',mgmt_swname)
 open_db,open_cursor = database_connect()
 open_cursor.execute(query_msg)
 query_results = open_cursor.fetchall() 
 database_disconnect(open_db,open_cursor)
 for result_tuple in query_results:
  builder_class_name = result_tuple[0].strip()
  builder_class = BUILDER_URLS[builder_class_name]
  return builder_class_name, builder_class
  break

#@csrf_exempt
#@api_view(['GET','DELETE'])
#def show_mgmtsw_details(request,mgmtsw_name):
# if request.method == 'GET':
#  if request.content_type == 'text/plain':
#   if request.QUERY_PARAMS:
#    return Response(status=status.HTTP_400_BAD_REQUEST)
#
#   #############################################
#   # find builder class                        #
#   #############################################
#   try:
#    builder_class_name, builder_class = get_builder_class_by_mgmt_swname(mgmtsw_name)
#    builder_instance = builder_class(builder_class_name,None)
#   except:
#    return Response([{"running_status":"error","error_details":"check the mgmt_swname"}],status=status.HTTP_400_BAD_REQUEST)
#   run_result = builder_instance.detail_view(mgmtsw_name)
#   return Response(run_result) 
#
#  else:
#   return Response(status=status.HTTP_400_BAD_REQUEST)
#
# elif request.method == 'DELETE':
#  try:
#   builder_class_name, builder_class = get_builder_class_by_mgmt_swname(mgmtsw_name)
#   builder_instance = builder_class(builder_class_name,None)
#  except:
#   return Response(status=status.HTTP_400_BAD_REQUEST)
#  run_result = builder_instance.delete(mgmtsw_name)
#  return Response(run_result)
#
# else:
#  return Response(status=status.HTTP_400_BAD_REQUEST)


class show_mgmtsw_details(APIView):

 authentication_classes = (SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication)
 # authentication_classes = (SessionAuthentication, BasicAuthentication)
 permission_classes = (IsAuthenticated,)
 #############################################################################################
 # default by http://www.django-rest-framework.org/tutorial/4-authentication-and-permissions #
 #############################################################################################
 # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)                             #
 ############################################################################################# 
 
 @csrf_exempt
 def get(self, request, mgmtsw_name, format=None):

  if request.content_type == 'text/plain':
   if request.QUERY_PARAMS:
    return Response(status=status.HTTP_400_BAD_REQUEST)

   #############################################
   # find builder class                        #
   #############################################
   try:
    builder_class_name, builder_class = get_builder_class_by_mgmt_swname(mgmtsw_name)
    builder_instance = builder_class(builder_class_name,None)
   except:
    return Response([{"running_status":"error","error_details":"check the mgmt_swname"}],status=status.HTTP_400_BAD_REQUEST)
   run_result = builder_instance.detail_view(mgmtsw_name)
   return Response(run_result)

  else:
   return Response(status=status.HTTP_400_BAD_REQUEST)

 @csrf_exempt
 def delete(self, request, mgmtsw_name, format=None):
  
  content = {'user': unicode(request.user),'auth': unicode(request.auth)}

  try:
   builder_class_name, builder_class = get_builder_class_by_mgmt_swname(mgmtsw_name)
   builder_instance = builder_class(builder_class_name,None)
  except:
   return Response(status=status.HTTP_400_BAD_REQUEST)
  run_result = builder_instance.delete(mgmtsw_name)
  return Response(run_result)
