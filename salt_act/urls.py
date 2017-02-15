from django.conf.urls import url
import views

urlpatterns = [
    url(r'^exec', views.ExecCmdView.as_view()),
    url(r'^exec/salt', views.ExecCmdSaltView.as_view()),
    url(r'^salt/key/all', views.SaltGetKeyAllView.as_view()),
    url(r'^salt/key/accept', views.SaltAcceptKeyView.as_view()),
    url(r'^salt/key/delete', views.SaltDeleteKeyView.as_view()),
    url(r'^salt/minion/init', views.SaltInitMinionView.as_view()),
    url(r'^salt/module/name', views.SaltGetModuleNameView.as_view()),
]
