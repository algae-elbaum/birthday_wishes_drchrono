from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/', views.login, name='login'),
    url(r'^authorize/', views.authorize, name='authorize'),
    url(r'^permissions_error/', views.permissions_error, name='permissions_error')
]
