from django.shortcuts import render
from django.http import HttpResponse

from .models import Order
# Create your views here.

#def index(request):
#    return HttpResponse("Hello, world. You' reat the polls index.")


def show_map(request, address_id):
    address = Order.objects.get(pk=address_id)
    location = address.convert_to_coordinates()
    context =  {'home' : [47.5467117, 7.5931471],
                'stop_list': [
            [47.5604656, 7.579825273611457],
            [47.4523151, 7.579825273611457],
            [48.5604656, 7.579825273611457],
            [48.5604656, 7.979825273611457],
            [47.5604656, 7.579825273611457],
            ],
                }
    return render(request, 'gmapsdisplay/index.html', context)
    #return HttpResponse(x)


def index(request):
    context =  {'latitude':  latitude,
                'longitude': longitude,
                'stop_list': stop_list,
                }
    return HttpResponse('TEST')