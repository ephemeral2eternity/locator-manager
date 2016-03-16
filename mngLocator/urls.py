from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^init/$', views.initLocators, name='init'),
	url(r'^query/$', views.viewLocators, name='query'),
	url(r'^getJsonData/$', views.getJsonData, name='getJsonData'),
]
