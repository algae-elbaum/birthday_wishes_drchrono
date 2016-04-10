"""birthday_wishes URL Configuration"""

from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^', include('birthday_wishes_app.urls')),
    url(r'^admin/', admin.site.urls),
]
