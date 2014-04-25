from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from net_builder.views import show_config_templates_details as SHOW_CONFIG_TEMPLATES_DETAILS
from net_builder.views import show_mgmtsw_details as SHOW_MGMTSW_DETAILS

urlpatterns = patterns('net_builder.views',
 url(r'^config_templates/$', 'show_config_templates_list', name='show_config_templates_list'),
# url(r'^config_templates/(?P<template_id>[\w\W]+)/$', 'show_config_templates_details', name='show_config_templates_details'),
 url(r'^config_templates/(?P<template_id>[\w\W]+)/$', SHOW_CONFIG_TEMPLATES_DETAILS.as_view(), name='SHOW_CONFIG_TEMPLATES_DETAILS'),

 url(r'^mgmtsw_list/$', 'show_mgmtsw_list', name='show_mgmtsw_list'),
# url(r'^mgmtsw_list/(?P<mgmtsw_name>[\w\W]+)/$', 'show_mgmtsw_details', name='show_mgmtsw_details'),
 url(r'^mgmtsw_list/(?P<mgmtsw_name>[\w\W]+)/$', SHOW_MGMTSW_DETAILS.as_view(), name='SHOW_MGMTSW_DETAILS'),


)

urlpatterns = format_suffix_patterns(urlpatterns)
