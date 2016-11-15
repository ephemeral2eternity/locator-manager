from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.template import RequestContext, loader
from nodeinfo.models import Node, Edge
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
            print(node_info)
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