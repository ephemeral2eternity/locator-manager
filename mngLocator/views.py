from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, JsonResponse
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from .models import Locator
from .list_agents import *

# Create your views here.
def index(request):
	# return HttpResponse("This is the main page of the management Portal of locator agents!")
	locators = Locator.objects.all()
	template = loader.get_template('mngLocator/index.html')
	return HttpResponse(template.render({'locators':locators}, request))
#	return render_to_response("mngLocator/index.html")

def initLocators(request):
	Locator.objects.all().delete()
	locators = list_agents("agens", "locator-")
	for locator in locators:
		new_locator = Locator(name=locator['name'], ip=locator['ip'], location=locator['location'], latitude=locator['latitude'], longitude=locator['longitude'])
		new_locator.save()

	return viewLocators(request)

def viewLocators(request):
	locators = Locator.objects.all()
	template = loader.get_template('mngLocator/locators.html')
	return HttpResponse(template.render({'locators':locators}, request))

def getJsonData(request):
	locators = Locator.objects.all()
	locator_geo_json = []
	for locator in locators:
		cur_agent = {'name' : locator.name, 'lat' : locator.latitude, 'lon' : locator.longitude, 'ip' : locator.ip}
		locator_geo_json.append(cur_agent)
	data = {}
	data['data'] = locator_geo_json
	rsp = JsonResponse(data, safe=False)
	rsp["Access-Control-Allow-Origin"] = "*"
	return rsp
