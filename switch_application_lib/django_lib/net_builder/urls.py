from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('net_builder.views',
 url(r'^config_templates/$', 'show_config_templates_list', name='show_config_templates_list'),
 url(r'^config_templates/(?P<template_id>[0-9]+)/$', 'show_config_templates_details', name='show_config_templates_details'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
