from django.conf.urls import url
from django.contrib.auth.views import login
from django.views.generic import RedirectView

import site_views, authorization_views, account_views

urlpatterns = [
    url(r'^$', site_views.home, name='home'),
    url(r'^patient/([0-9]+)', site_views.patient_page, name='patient_page'),
    url(r'^refresh_patients/', site_views.refresh_patients, name='refresh_patients'),
    url(r'^about/', site_views.about, name='about'),
   
    url(r'^authorize/', authorization_views.authorize, name='authorize'),
    url(r'^authorization_redirect/', authorization_views.authorization_redirect, name='authorization_redirect'),
    url(r'^permissions_error/', authorization_views.permissions_error, name='permissions_error'),

    url(r'^login/', login, {'template_name': 'login.html'}),
    url(r'^logout/', account_views.logout, name='logout'),
    url(r'^manual_logout/', account_views.manual_logout, name='manual_logout'),
    url(r'^register/', account_views.register, name='register'),
      
    # Not part of the project. I just want this url to still work while django is hogging port 80 
    url(r'^muse_server/$', RedirectView.as_view(url='http://gaster.caltech.edu:8000/muse_server/'))
]
