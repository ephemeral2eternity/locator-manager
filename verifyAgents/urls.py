from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^add_video_session$', views.addVideoSession, name='add_video_session'),
	url(r'^add_verify_session$', views.addAgentPath, name='add_verify_session'),
	url(r'^show_video_sessions$', views.showVideoSessions, name='show_video_sessions'),
	url(r'^show_verify_sessions$', views.showVerifySessions, name='show_verify_sessions'),
	url(r'^show_video_networks$', views.showVideoNetworks, name='show_video_networks$'),
	url(r'^show_verify_networks$', views.showVerifyNetworks, name='show_verify_networks$'),
	url(r'^get_node', views.getNode, name='get_node'),
	url(r'^get_network', views.getNetwork, name='get_network'),
	url(r'^get_route', views.getRoute, name='get_route'),
	url(r'^get_subnetworks', views.getSubnetwork, name='get_subnetworks'),
	url(r'^get_sessions_for_networks', views.getVerifySessionForVideoNetworks, name='get_sessions_for_networks'),
	url(r'^flush', views.flush, name='flush'),
]
