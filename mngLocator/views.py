from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Locator, Cache
from client.models import GeoConnected, NetConnected
from .list_agents import *

# Create your views here.
def index(request):
	# return HttpResponse("This is the main page of the management Portal of locator agents!")
	locators = Locator.objects.all()
	template = loader.get_template('mngLocator/index.html')
	return HttpResponse(template.render({'locators':locators}, request))
#	return render_to_response("mngLocator/index.html")

def init(request):
	Locator.objects.all().delete()
	locators = list_agents("agens", "locator-")
	for locator in locators:
		new_locator = Locator(name=locator['name'], ip=locator['ip'], location=locator['location'], latitude=locator['latitude'], longitude=locator['longitude'])
		new_locator.save()

	Cache.objects.all().delete()
	caches = list_agents("cache", "cache-")
	for cache in caches:
		new_cache = Cache(name=cache['name'], ip=cache['ip'], location=cache['location'], latitude=cache['latitude'], longitude=cache['longitude'])
		new_cache.save()

	return view(request)

def view(request):
	locators = Locator.objects.all()
	caches = Cache.objects.all()
	template = loader.get_template('mngLocator/all.html')
	return HttpResponse(template.render({'locators':locators, 'caches':caches}, request))

def viewLocators(request):
	locators = Locator.objects.all()
	template = loader.get_template('mngLocator/locators.html')
	return HttpResponse(template.render({'locators':locators}, request))

def getJsonData(request):
	data = {}
	locators = Locator.objects.all()
	locator_geo_json = []
	for locator in locators:
		cur_agent = {'name' : locator.name, 'lat' : locator.latitude, 'lon' : locator.longitude, 'ip' : locator.ip}
		locator_geo_json.append(cur_agent)
	data['agent'] = locator_geo_json

	caches = Cache.objects.all()
	cache_geo_json = []
	for cache in caches:
		cur_cache = {'name' : cache.name, 'lat' : cache.latitude, 'lon' : cache.longitude, 'ip' : cache.ip}
		cache_geo_json.append(cur_cache)
	data['cache'] = cache_geo_json

	clients = GeoConnected.objects.all()
	client_geo_json = []
	for client in clients:
		cur_client = {'name': client.client, 'lat': client.latitude, 'lon':client.longitude, 'ip' : client.ip}
		client_geo_json.append(cur_client)
	data['client'] = client_geo_json

	rsp = JsonResponse(data, safe=False)
	rsp["Access-Control-Allow-Origin"] = "*"
	return rsp


def clearAll(request):
	GeoConnected.objects.all().delete()
	NetConnected.objects.all().delete()
	return index(request)


def getCloudAgents(request):
	data = {}
	locators = Locator.objects.all()
	locator_geo_json = []
	for locator in locators:
		cur_agent = {'name': locator.name, 'lat': locator.latitude, 'lon': locator.longitude, 'ip': locator.ip}
		locator_geo_json.append(cur_agent)

	rsp = JsonResponse(locator_geo_json, safe=False)
	rsp["Access-Control-Allow-Origin"] = "*"
	return rsp