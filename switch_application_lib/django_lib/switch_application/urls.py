from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'switch_application.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),

    # authentication with jwt
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),

    # net_builder application url path
    url(r'^net_builder/', include('net_builder.urls')),
)
