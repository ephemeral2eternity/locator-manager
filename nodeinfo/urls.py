from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^add$', views.addRouteInfo, name='add'),
	url(r'^show_nodes', views.showNodes, name='show_nodes'),
	url(r'^show_edges', views.showEdges, name='show_edges'),
	url(r'^edit_node', views.editNode, name='edit_node'),
]
