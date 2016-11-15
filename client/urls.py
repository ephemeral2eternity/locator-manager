from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^add$', views.add, name='add'),
	url(r'^queryGeo$', views.queryGeo, name='queryGeo'),
	url(r'^queryNet$', views.queryNet, name='queryNet'),
	url(r'^get$', views.get, name='get'),
	url(r'^getJson$', views.getJson, name='getJson'),
	url(r'^getGraph$', views.getGraph, name='getGraph'),
	url(r'^getLocator$', views.getLocator, name='getLocator'),
]
