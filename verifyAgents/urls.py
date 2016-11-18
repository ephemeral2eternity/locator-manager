from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^add_video_session$', views.addVideoSession, name='add_video_session'),
	url(r'^add_verify_session$', views.addAgentPath, name='add_verify_session'),
	url(r'^show_sessions$', views.showVideoSessions, name='show_sessions'),
	url(r'^get_node', views.getNode, name='get_node'),
	url(r'^get_network', views.getNetwork, name='get_network'),
	url(r'^get_route', views.getRoute, name='get_route'),
]
