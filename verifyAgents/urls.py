from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^add_video_session$', views.addVideoSession, name='add_video_session'),
	url(r'^add_verify_session$', views.addAgentPath, name='add_verify_session'),
	url(r'^show_video_sessions$', views.showVideoSessions, name='show_video_sessions'),
	url(r'^show_verify_sessions$', views.showVerifySessions, name='show_verify_sessions'),
	url(r'^init_networks_for_verify_sessions$', views.initNetworksForVerifySessions, name='init_networks_for_verify_sessions$'),
	url(r'^shorten_networks_for_verify_sessions$', views.shortenNetworksForVerifySessions, name='shorten_networks_for_verify_sessions'),
	url(r'^show_networks_for_verify_sessions$', views.showNetworksForVerifySessions, name='show_networks_for_verify_sessions$'),
	url(r'^init_verify_sessions_for_networks$', views.initVerifySessionsForNetwork, name='init_verify_sessions_for_networks$'),
	url(r'^show_verify_sessions_for_networks$', views.showVerifySessionsForNetworks, name='show_verify_sessions_for_networks$'),
	url(r'^show_video_networks$', views.showVideoNetworks, name='show_video_networks$'),
	url(r'^show_verify_networks$', views.showVerifyNetworks, name='show_verify_networks$'),
	url(r'^get_node', views.getNode, name='get_node'),
	url(r'^get_network', views.getNetwork, name='get_network'),
	url(r'^get_route', views.getRoute, name='get_route'),
	url(r'^get_subnetworks', views.getSubnetwork, name='get_subnetworks'),
	url(r'^get_session', views.getSession, name='get_session'),
	url(r'^get_verify_session_by_src', views.getVerifySessionBySrc, name='get_verify_session_by_src'),
	url(r'^get_peers', views.getPeerAgents, name='get_peers'),
	url(r'^flush', views.flush, name='flush'),
]
