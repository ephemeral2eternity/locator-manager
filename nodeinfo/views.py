from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.template import RequestContext, loader
from nodeinfo.models import Node, Edge, Network
import urllib
import json

# Create your views here.
@csrf_exempt
@transaction.atomic
def addRouteInfo(request):
    if request.method == "POST":
        client_info = json.loads(request.body.decode("utf-8"))
        # print(client_info)
        try:
            client_node = Node.objects.get(ip=client_info['ip'])
            if client_node.city == "":
                client_node.city = client_info['city']
            if client_node.region == "":
                client_node.region = client_info['region']
            if client_node.country == "":
                client_node.country = client_info['country']
        except:
            client_node = Node(name=client_info['name'], ip=client_info['ip'], type="client",
                           city=client_info['city'], region=client_info['region'], country=client_info['country'],
                           AS=client_info['AS'], ISP=client_info['ISP'],
                           latitude=client_info['latitude'], longitude=client_info['longitude'])
        client_node.save()

        pre_node = client_node
        for i, node in enumerate(client_info['route']):
            node_ip = node['ip']
            if node_ip != client_info['ip']:
                if node_ip == client_info['server']:
                    node_type = "server"
                else:
                    node_type = "router"
                try:
                    cur_node = Node.objects.get(ip=node_ip)
                    if cur_node.city == "":
                        cur_node.city = node['city']
                    if cur_node.region == "":
                        cur_node.region = node['region']
                    if cur_node.country == "":
                        cur_node.country = node['country']
                except:
                    cur_node = Node(name=node['name'], ip=node_ip, type=node_type,
                           city=node['city'], region=node['region'], country=node['country'],
                           AS=node['AS'], ISP=node['ISP'],
                           latitude=node['latitude'], longitude=node['longitude'])
                cur_node.save()

                if pre_node.ip != cur_node.ip:
                    try:
                        cur_edge = Edge.objects.get(src=pre_node, dst=cur_node)
                    except:
                        cur_edge = Edge(src=pre_node, dst=cur_node)
                    cur_edge.save()
                pre_node = cur_node

        return HttpResponse("Successful!")
    else:
        return HttpResponse("Please use POST method for http://manage.cmu-agens.com/nodeinfo/add_route_info request!")

def initNetworks(request):
    if Network.objects.count() > 0:
        Network.objects.all().delete()

    nodes = Node.objects.all()
    for node in nodes:
        node_as = int(node.AS)
        node_latitude = float(node.latitude)
        node_longitude = float(node.longitude)
        try:
            node_network = Network.objects.get(AS=node_as, latitude=node_latitude, longitude=node_longitude)
        except:
            node_network = Network(AS=node_as, name=node.ISP, latitude=node_latitude, longitude=node_longitude,
                                   city=node.city, region=node.region, country=node.country)
        node_network.save()

    return showNetworks(request)

@csrf_exempt
@transaction.atomic
def addNode(request):
    if request.method == "POST":
        node_info = json.loads(request.body.decode("utf-8"))
        try:
            node = Node.objects.get(ip=node_info['ip'])
            if node.city == "":
                node.city = node_info['city']
            if node.region == "":
                node.region = node_info['region']
            if node.country == "":
                node.country = node_info['country']
        except:
            node = Node(name=node_info['name'], ip=node_info['ip'], type=node_info['type'],
                           city=node_info['city'], region=node_info['region'], country=node_info['country'],
                           AS=node_info['AS'], ISP=node_info['ISP'],
                           latitude=node_info['latitude'], longitude=node_info['longitude'])
        node.save()
        template = loader.get_template('nodeinfo/edit_node.html')
        return HttpResponse(template.render({'node': node}, request))
    else:
        return HttpResponse(
            "Please use POST method for http://manage.cmu-agens.com/nodeinfo/add_node request!")


@csrf_exempt
@transaction.atomic
def editNode(request):
    url = request.get_full_path()
    params = url.split('?')[1]
    request_dict = urllib.parse.parse_qs(params)
    if ('id' in request_dict.keys()):
        node_id = int(request_dict['id'][0])
        node = Node.objects.get(id=node_id)
        if request.method == "POST":
            node_info = request.POST.dict()
            # print(node_info)
            node.type = node_info['type']
            node.name = node_info['name']
            node.ISP = node_info['isp']
            node.AS = int(node_info['asn'])
            node.latitude = float(node_info['latitude'])
            node.longitude = float(node_info['longitude'])
            node.city = node_info['city']
            node.region = node_info['region']
            node.country = node_info['country']
            node.save()
            template = loader.get_template('nodeinfo/node.html')
            return HttpResponse(template.render({'node':node}, request))
        else:
            template = loader.get_template('nodeinfo/edit_node.html')
            return HttpResponse(template.render({'node':node}, request))
    else:
        return HttpResponse("Wrong network id denoted!")


# Get the json info of a node by denoting its ip
def getNode(request):
    url = request.get_full_path()
    if '?' in url:
        params = url.split('?')[1]
        request_dict = urllib.parse.parse_qs(params)
        if ('ip' in request_dict.keys()):
            ip = request_dict['ip'][0]
        else:
            ip = request.META['REMOTE_ADDR']
    else:
        ip = request.META['REMOTE_ADDR']
    node_dict = {}
    try:
        node = Node.objects.get(ip=ip)
        node_dict['name'] = node.name
        node_dict['ip'] = node.ip
        node_dict['type'] = node.type
        node_dict['city'] = node.city
        node_dict['region'] = node.region
        node_dict['country'] = node.country
        node_dict['AS'] = node.AS
        node_dict['ISP'] = node.ISP
        node_dict['latitude'] = node.latitude
        node_dict['longitude'] = node.longitude
    except:
        print("No node with ip = " + ip)
    rsp = JsonResponse(node_dict, safe=False)
    rsp["Access-Control-Allow-Origin"] = "*"
    return rsp

# Show detailed info of all nodes.
def showNodes(request):
    nodes = Node.objects.all()
    template = loader.get_template('nodeinfo/nodes.html')
    return HttpResponse(template.render({'nodes': nodes}, request))

# Show detailed info of all nodes.
def showEdges(request):
    edges = Edge.objects.all()
    template = loader.get_template('nodeinfo/edges.html')
    return HttpResponse(template.render({'edges': edges}, request))

def showNetworks(request):
    networks = Network.objects.all()
    template = loader.get_template('nodeinfo/networks.html')
    return HttpResponse(template.render({'networks':networks}, request))