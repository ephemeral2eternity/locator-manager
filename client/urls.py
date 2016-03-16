from django.conf.urls import patterns, url
from . import views

urlpatterns = [
	url(r'^add$', views.add, name='add'),
	url(r'^queryGeo$', views.queryGeo, name='queryGeo'),
	url(r'^queryNet$', views.queryNet, name='queryNet'),
]
