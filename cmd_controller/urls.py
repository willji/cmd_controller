from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'cmd_controller.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # Token Infra
    url(r'^api/token/', views.obtain_auth_token),
    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('salt_api.urls')),
    url(r'^', include('salt_act.urls')),
]
