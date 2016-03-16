from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import GeoConnected, NetConnected
import json
import urllib

# Create your views here.
@csrf_exempt
def add(request):
	url = request.get_full_path()
	params = url.split('?')[1]
	request_dict = urllib.parse.parse_qs(params)
	print(request_dict.keys())
	if ('method' in request_dict.keys()):
		method = request_dict['method'][0]
	else:
		method = "geo"

	if request.method == "POST":
		client_info = json.loads(request.body.decode("utf-8"))
		print("Receiving client info from " + client_info['hostname'])
		if method == "geo":
			client_exist = GeoConnected.objects.filter(ip=client_info['ip'])
		else:
			client_exist = NetConnected.objects.filter(ip=client_info['ip'])
		if client_exist.count() > 0:
			client_obj = client_exist[0]
			client_obj.client = client_info['hostname']
			client_obj.locator = client_info['locator']
			client_obj.ip = client_info['ip']
			client_obj.city = client_info['city']
			client_obj.region = client_info['region']
			client_obj.country = client_info['country']
			client_obj.AS = client_info['AS']
			client_obj.ISP = client_info['ISP']
			client_obj.longitude = client_info['longitude']
			client_obj.latitude = client_info['latitude']
		else:
			if method == "geo":
				client_obj = GeoConnected(client=client_info['hostname'], locator=client_info['locator'], ip=client_info['ip'], 
							city=client_info['city'], region=client_info['region'], country=client_info['region'],
							AS=client_info['AS'], ISP=client_info['ISP'], longitude=client_info['longitude'], 
							latitude=client_info['latitude'])
			else:
				client_obj = NetConnected(client=client_info['hostname'], locator=client_info['locator'], ip=client_info['ip'], 
							city=client_info['city'], region=client_info['region'], country=client_info['region'],
							AS=client_info['AS'], ISP=client_info['ISP'], longitude=client_info['longitude'], 
							latitude=client_info['latitude'])
		client_obj.save()
		if method == "geo":
			return queryGeo(request)
		else:
			return queryNet(request)
	else:
		return HttpResponse("Please use the POST method for http://manager/client/add?method=geo/net request to connect clients")


@csrf_exempt
def queryGeo(request):
	clients = GeoConnected.objects.all()
	method = "Geo-location"
	template = loader.get_template('client/clients.html')
	return HttpResponse(template.render({'method' : method, 'clients' : clients}))


@csrf_exempt
def queryNet(request):
	clients = NetConnected.objects.all()
	method = "Network Latencies"
	template = loader.get_template('client/clients.html')
	return HttpResponse(template.render({'method' : method, 'clients' : clients}))
