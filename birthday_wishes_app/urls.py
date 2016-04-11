from django.conf.urls import url
from django.contrib.auth.views import login, logout_then_login

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/', login, {'template_name': 'login.html'}),
    url(r'^logout/', logout_then_login),
    url(r'^manual_logout/', views.manual_logout, name='manual_logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^authorize/', views.authorize, name='authorize'),
    url(r'^permissions_error/', views.permissions_error, name='permissions_error'),
    url(r'^patient/([0-9]+)', views.patient_page, name='patient_page')
]
