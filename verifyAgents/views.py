from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Count
from .add_route import *
from .models import VerifySession, NetworkVerifySessionsPair
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

@csrf_exempt
@transaction.atomic
def editNetwork(request):
    url = request.get_full_path()
    params = url.split('?')[1]
    request_dict = urllib.parse.parse_qs(params)
    if ('id' in request_dict.keys()):
        network_id = int(request_dict['id'][0])
        network = Network.objects.get(id=network_id)
        if request.method == "POST":
            network_info = request.POST.dict()
            # print(node_info)
            try:
                existing_network = Network.objects.get(ASNumber=int(network_info['asn']), latitude=float(network_info['latitude']), longitude=float(network_info['longitude']))
                print("Edited network exists!")
                print("Merge the current network nodes to existing network" + str(existing_network))
                for node in network.nodes.all():
                    if node not in existing_network.nodes.all():
                        existing_network.nodes.add(node)
                existing_network.save()
                network.delete()
                template = loader.get_template('verifyAgents/edit_network.html')
                return HttpResponse(template.render({'network':existing_network}, request))
            except:
                network.type = network_info['type']
                network.name = network_info['name']
                network.ASNumber = int(network_info['asn'])
                network.latitude = float(network_info['latitude'])
                network.longitude = float(network_info['longitude'])
                network.city = network_info['city']
                network.region = network_info['region']
                network.country = network_info['country']
                network.save()
                template = loader.get_template('verifyAgents/edit_network.html')
                return HttpResponse(template.render({'network':network}, request))
        else:
            template = loader.get_template('verifyAgents/edit_network.html')
            return HttpResponse(template.render({'network':network}, request))
    else:
        return HttpResponse("Wrong network id denoted!")

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


def showVideoSubnetworks(request):
    subnetworks = Subnetwork.objects.filter(network__isVideoPath=True)
    template = loader.get_template('verifyAgents/session_network_pairs.html')
    return HttpResponse(template.render({'subnetworks': subnetworks, 'type': "video"}, request))

def showVerifySubnetworks(request):
    subnetworks = Subnetwork.objects.filter(network__isVideoPath=False)
    template = loader.get_template('verifyAgents/session_network_pairs.html')
    return HttpResponse(template.render({'subnetworks': subnetworks, 'type': "verify"}, request))

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

def getVideoSessionsPerNetwork(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('id' in request_dict.keys()):
            network_id = request_dict['id'][0]
            video_sessions = Session.objects.filter(route_networks__id=network_id, isVideoSession=True)
            template = loader.get_template('verifyAgents/sessions.html')
            return HttpResponse(template.render({'network_id': network_id, 'sessions': video_sessions, 'sessionType': "video"}, request))
        else:
            return HttpResponse("Please give the network id !")
    else:
        return HttpResponse("Please use the request : http://manage.cmu-agens.com/verify/get_video_session_per_network?id=network_id")

def getVerifySessionsPerNetwork(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('id' in request_dict.keys()):
            network_id = request_dict['id'][0]
            verify_sessions = VerifySession.objects.filter(networks__id=network_id)
            template = loader.get_template('verifyAgents/sessions.html')
            return HttpResponse(template.render({'network_id': network_id, 'sessions': verify_sessions, 'sessionType': "verify"}, request))
        else:
            return HttpResponse("Please give the network id !")
    else:
        return HttpResponse("Please use the request : http://manage.cmu-agens.com/verify/get_verify_session_per_network?id=network_id")

def showVerifyNetworks(request):
    networks = Network.objects.filter(isVideoPath=False)
    tempate = loader.get_template('verifyAgents/networks.html')
    return HttpResponse(tempate.render({'networks':networks}, request))

def initNetworksForVerifySessions(request):
    video_subnets = Subnetwork.objects.filter(Q(session__isVideoSession=False) & Q(network__isVideoPath=True))

    K = 5
    ## Assign each verify session to a unique network
    for video_subnet in video_subnets:
        try:
            network_verify_session_pair = NetworkVerifySessionsPair.objects.get(network=video_subnet.network)
            if network_verify_session_pair.verify_sessions.count() >= K:
                pass
            else:
                try:
                    network_verify_session_pair.verify_sessions.get(video_subnet.session)
                except:
                    network_verify_session_pair.verify_sessions.add(video_subnet.session)
        except:
            network_verify_session_pair = NetworkVerifySessionsPair(network=video_subnet.network)
            network_verify_session_pair.verify_sessions.add(video_subnet.session)
        print("Add session " + str(video_subnet.session) + " to " + str(network_verify_session_pair))
        network_verify_session_pair.save()
    return showNetworksForVerifySessions(request)

def shortenNetworksForVerifySessions(request):
    K = 5
    for cur_network in NetworkVerifySessionsPair.objects.all():
        print("Shorten verify sessions for network " + str(cur_network))
        verify_sessions = cur_network.verify_sessions
        if verify_sessions.count() > K:
            sorted_sessions = verify_sessions.all().annotate(length=Count('route')).order_by('length')
            i = 0
            for cur_session in sorted_sessions:
                if i > K:
                    cur_network.verify_sessions.remove(cur_session)
                i += 1
        cur_network.save()
    return showNetworksForVerifySessions(request)

def showNetworksForVerifySessions(request):
    networks_for_verify_sessions = NetworkVerifySessionsPair.objects.all()
    template = loader.get_template('verifyAgents/networks_for_verify_sessions.html')
    return HttpResponse(template.render({'network_sessions': networks_for_verify_sessions}, request))

def initVerifySessionsForNetwork(request):
    print("Deleting previous verify sessions!")
    VerifySession.objects.all().delete()
    for network_verify_session_pair in NetworkVerifySessionsPair.objects.all():
        for session in network_verify_session_pair.verify_sessions.all():
            print("Add " + str(session) + " from " + str(network_verify_session_pair.network))
            try:
                cur_verify_session = VerifySession.objects.get(src_ip=session.src_ip, dst_ip=session.dst_ip, length=session.route.count())
            except:
                cur_verify_session = VerifySession(src_ip=session.src_ip, dst_ip=session.dst_ip, length=session.route.count())
            cur_verify_session.save()
            cur_verify_session.networks.add(network_verify_session_pair.network)
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

def getPeerAgents(request):
    src_ip = request.META['REMOTE_ADDR']
    verify_sessions_by_src = VerifySession.objects.filter(src_ip=src_ip)
    rst = []
    for session in verify_sessions_by_src:
        if session.dst_ip not in rst:
            rst.append(session.dst_ip)
    return HttpResponse(",".join(rst))

def showVideoSessions(request):
    sessions = Session.objects.filter(isVideoSession=True)
    template = loader.get_template('verifyAgents/sessions.html')
    return HttpResponse(template.render({'sessions': sessions, 'sessionType': "video"}, request))

def showVerifySessions(request):
    sessions = Session.objects.filter(isVideoSession=False)
    template = loader.get_template('verifyAgents/sessions.html')
    return HttpResponse(template.render({'sessions': sessions, 'sessionType': "verify"}, request))