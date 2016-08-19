from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^friends$', views.friends),
    url(r'^add/(?P<id>\d+)$', views.add),
    url(r'^user/(?P<id>\d+)$', views.user),
    url(r'^delete/(?P<id>\d+)$', views.delete),
]
