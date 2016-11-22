from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .add_route import *
from .models import VerifySession, NetworkForVerifySession
import json
import urllib

# Create your views here.
def flush(request):
    Node.objects.all().delete()
    Network.objects.all().delete()
    Session.objects.all().delete()
    return HttpResponse("Flush successfully for App: verifyAgents!")

# Add the hops in the Client's route and get the client's route networks, server, and device info.
@csrf_exempt
@transaction.atomic
def addVideoSession(request):
    isVideoPath = True
    if request.method == "POST":
        client_info = json.loads(request.body.decode("utf-8"))
        add(client_info, isVideoPath)
        return HttpResponse("OK")
    else:
        return HttpResponse("You should use POST method!")

@csrf_exempt
@transaction.atomic
def addAgentPath(request):
    isVideoPath = False
    if request.method == "POST":
        client_info = json.loads(request.body.decode("utf-8"))
        add(client_info, isVideoPath)
        return HttpResponse("OK")
    else:
        return HttpResponse("You should use POST method!")

def getNode(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('ip' in request_dict.keys()):
            node_ip = request_dict['ip'][0]
            node = Node.objects.get(ip=node_ip)
            template = loader.get_template('verifyAgents/node.html')
            return HttpResponse(template.render({'node': node}, request))
        else:
            return HttpResponse("Please use http://manager/verify/get_node?ip=node_ip to get the node info!")
    else:
        return HttpResponse("Please use http://manager/verify/get_node?ip=node_ip to get the node info!")

def getNetwork(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('id' in request_dict.keys()):
            network_id = request_dict['id'][0]
            network = Network.objects.get(id=network_id)
            edges = Edge.objects.filter(Q(src__in=network.nodes.all()) | Q(dst__in=network.nodes.all()))
            template = loader.get_template('verifyAgents/network.html')
            return HttpResponse(template.render({'network': network, 'edges': edges}, request))
        else:
            return HttpResponse('You need to use http://manager/verify/get_network?id=network_id to get the network info!')
    else:
        return HttpResponse('You need to use http://manager/verify/get_network?id=network_id to get the network info!')

def getRoute(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('src' in request_dict.keys()) and ('dst' in request_dict.keys()):
            src_ip = request_dict['src'][0]
            dst_ip = request_dict['dst'][0]
            session = Session.objects.get(src_ip=src_ip, dst_ip=dst_ip)
            route = Hop.objects.filter(session=session)
            template = loader.get_template('verifyAgents/route.html')
            return HttpResponse(template.render({'session': session, 'route': route}, request))
        else:
            return HttpResponse(
                "You should use GET request http://manager/verify/get_route?src=src_ip&dst=dst_ip to get the route info for the session (src, dst)!")
    else:
        return HttpResponse(
            "You should use GET request http://manager/verify/get_route?src=src_ip&dst=dst_ip to get the route info for the session (src, dst)!")

def getSubnetwork(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('src' in request_dict.keys()) and ('dst' in request_dict.keys()):
            src_ip = request_dict['src'][0]
            dst_ip = request_dict['dst'][0]
            session = Session.objects.get(src_ip=src_ip, dst_ip=dst_ip)
            subnetworks = Subnetwork.objects.filter(session=session)
            template = loader.get_template('verifyAgents/subnetworks.html')
            return HttpResponse(template.render({'session': session, 'subnetworks': subnetworks}, request))
        else:
            return HttpResponse(
                "You should use GET request http://manager/verify/get_subnetworks?src=src_ip&dst=dst_ip to get the route info for the session (src, dst)!")
    else:
        return HttpResponse(
        "You should use GET request http://manager/verify/get_subnetworks?src=src_ip&dst=dst_ip to get the subnetwork info for the session (src, dst)!")

def getSession(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('src' in request_dict.keys()) and ('dst' in request_dict.keys()):
            src_ip = request_dict['src'][0]
            dst_ip = request_dict['dst'][0]
            session = Session.objects.get(src_ip=src_ip, dst_ip=dst_ip)
            template = loader.get_template('verifyAgents/session.html')
            return HttpResponse(template.render({'session': session}, request))
        else:
            return HttpResponse(
                "You should use GET request http://manager/verify/get_session?src=src_ip&dst=dst_ip to get the session info for the session (src, dst)!")
    else:
        return HttpResponse(
            "You should use GET request http://manager/verify/get_session?src=src_ip&dst=dst_ip to get the session info for the session (src, dst)!")

def showVideoNetworks(request):
    networks = Network.objects.filter(isVideoPath=True)
    tempate = loader.get_template('verifyAgents/networks.html')
    return HttpResponse(tempate.render({'networks':networks}, request))

def showVerifyNetworks(request):
    networks = Network.objects.filter(isVideoPath=False)
    tempate = loader.get_template('verifyAgents/networks.html')
    return HttpResponse(tempate.render({'networks':networks}, request))

def initNetworksForVerifySessions(request):
    NetworkForVerifySession.objects.all().delete()
    verifySessionForVideoNetworks = Subnetwork.objects.filter(
        Q(session__isVideoSession=False) & Q(network__isVideoPath=True))
    for subNtw in verifySessionForVideoNetworks:
        try:
            curNetwork = NetworkForVerifySession.objects.get(network=subNtw.network)
        except:
            curNetwork = NetworkForVerifySession(network=subNtw.network)
        curNetwork.save()
        curNetwork.verify_sessions.add(subNtw.session)
        curNetwork.save()
    return showNetworksForVerifySessions(request)

def showNetworksForVerifySessions(request):
    networks_for_verify_sessions = NetworkForVerifySession.objects.all()
    template = loader.get_template('verifyAgents/networks_for_verify_sessions.html')
    return HttpResponse(template.render({'network_sessions': networks_for_verify_sessions}, request))

def initVerifySessionsForNetwork(request):
    VerifySession.objects.all().delete()
    verifySessionForVideoNetworks = Subnetwork.objects.filter(
        Q(session__isVideoSession=False) & Q(network__isVideoPath=True))
    for subNtw in verifySessionForVideoNetworks:
        try:
            cur_verify_session = VerifySession.objects.get(src_ip=subNtw.session.src_ip, dst_ip=subNtw.session.dst_ip, length=subNtw.session.route.count())
        except:
            cur_verify_session = VerifySession(src_ip=subNtw.session.src_ip, dst_ip=subNtw.session.dst_ip,
                                                           length=subNtw.session.route.count())
        cur_verify_session.save()
        cur_verify_session.networks.add(subNtw.network)
        cur_verify_session.save()
    return showVerifySessionsForNetworks(request)

def showVerifySessionsForNetworks(request):
    verify_sessions = VerifySession.objects.all()
    template = loader.get_template('verifyAgents/verify_sessions.html')
    return HttpResponse(template.render({'verify_sessions': verify_sessions}, request))

def getVerifySessionBySrc(request):
    src_ip = request.META['REMOTE_ADDR']
    verify_sessions_by_src = VerifySession.objects.filter(src_ip=src_ip)
    rst = {}
    for session in verify_sessions_by_src:
        if session.dst_ip not in rst.keys():
            rst[session.dst_ip] = []
        cur_session = {}
        cur_session['length'] = session.length
        cur_session['networks'] = []
        for ntw in session.networks.all():
            cur_session['networks'].append(ntw.id)
        rst[session.dst_ip] = cur_session
    return JsonResponse(rst)

def showVideoSessions(request):
    sessions = Session.objects.filter(isVideoSession=True)
    template = loader.get_template('verifyAgents/sessions.html')
    return HttpResponse(template.render({'sessions': sessions, 'sessionType': "video"}, request))

def showVerifySessions(request):
    sessions = Session.objects.filter(isVideoSession=False)
    template = loader.get_template('verifyAgents/sessions.html')
    return HttpResponse(template.render({'sessions': sessions, 'sessionType': "verify"}, request))