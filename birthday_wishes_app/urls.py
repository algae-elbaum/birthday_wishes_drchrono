from django.conf.urls import url
from django.contrib.auth.views import login
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/', login, {'template_name': 'login.html'}),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^manual_logout/', views.manual_logout, name='manual_logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^authorize/', views.authorize, name='authorize'),
    url(r'^authorization_redirect/', views.authorization_redirect, name='authorization_redirect'),
    url(r'^permissions_error/', views.permissions_error, name='permissions_error'),
    url(r'^patient/([0-9]+)', views.patient_page, name='patient_page'),
    url(r'^refresh_patients/', views.refresh_patients, name='refresh_patients'),
    
    # Not part of the project. I just want this url to still work while django is hogging port 80 
    url(r'^muse_server/$', RedirectView.as_view(url='http://gaster.caltech.edu:8000/muse_server/'))
]
