from django.db import models

# Create your models here.

class switch_configuration_urls(models.Model):
 mgmt_swname = models.CharField(max_length=100, blank=True, default='')
 builder_name = models.CharField(max_length=100, blank=True, default='')
 url = models.CharField(max_length=100, blank=True, default='')
 class Meta:
  ordering = ('mgmt_swname',)

class switch_network_usages(models.Model):
 mgmt_swname = models.CharField(max_length=100, blank=True, default='')
 mgmt_network = models.CharField(max_length=100, blank=True, default='')
 srv_network = models.CharField(max_length=100, blank=True, default='')
 class Meta:
  ordering = ('mgmt_swname',)

class mgmt_network_ip_pools_for_cstack(models.Model):
 allocated_ip_address = models.CharField(max_length=100, blank=True, default='')
 mgmt_swname = models.CharField(max_length=100, blank=True, default='')
 usedby = models.CharField(max_length=100, blank=True, default='') 
 class Meta:
  ordering = ('mgmt_swname',)

class mgmt_network_ip_pools_for_ostack(models.Model):
 allocated_ip_address = models.CharField(max_length=100, blank=True, default='')
 mgmt_swname = models.CharField(max_length=100, blank=True, default='')
 usedby = models.CharField(max_length=100, blank=True, default='')              
 class Meta:
  ordering = ('mgmt_swname',)

class srv_network_ip_pools_for_cstack(models.Model):
 allocated_ip_address = models.CharField(max_length=100, blank=True, default='')
 mgmt_swname = models.CharField(max_length=100, blank=True, default='')
 usedby = models.CharField(max_length=100, blank=True, default='')              
 class Meta:
  ordering = ('mgmt_swname',)

class srv_network_ip_pools_for_ostack(models.Model):
 allocated_ip_address = models.CharField(max_length=100, blank=True, default='')
 mgmt_swname = models.CharField(max_length=100, blank=True, default='')
 usedby = models.CharField(max_length=100, blank=True, default='')
 class Meta:
  ordering = ('mgmt_swname',)
