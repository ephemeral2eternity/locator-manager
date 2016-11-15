from django.shortcuts import render
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.db import transaction
from django.http import HttpResponse, JsonResponse

# Create your views here.
# Add the hops in the Client's route and get the client's route networks, server, and device info.
@csrf_exempt
@transaction.atomic
def add(request):
    if request.method == "POST":
        return HttpResponse("Add successfully!")
    else:
        return HttpResponse("Please use POST method to add networks and routers for verification sessions!")