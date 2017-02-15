__author__ = 'jinhongjun'
from django.conf.urls import patterns, url
from salt_api import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'master', views.MasterViewSet)
router.register(r'minion', views.MinionViewSet)
router.register(r'module', views.ModuleViewSet)
router.register(r'log', views.LogViewSet)
urlpatterns = router.urls