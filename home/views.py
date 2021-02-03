from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.

def home(request):
    context = {'emenities' : []}
    
    pincodes = Pincode.objects.all()
    
    pincode_to_be_found = "226020"

    pincode = Pincode.objects.filter(pincode = pincode_to_be_found).first()
    
    distance = []
    for pi in pincodes:
        if pi.pincode != pincode.pincode:
            dis = pi.distance(pincode.lat , pincode.lon)
            distance.append({'pincode' : pi.pincode  , 'km' : dis })
    distance = sorted(distance , key=lambda i:i ['km']) 
    print(distance)
    
    
    return render(request,'home.html', context)

from home.constant import isa_academy_pincodes

from geopy.geocoders import Nominatim

def distance(lat1 , long1, lat2, long2):
        lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
        dlon = long2 - long1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371* c    
        return km

def api_pincode(request):
    pincode = request.GET.get('get_pincode')
    if pincode is None:
        return JsonResponse({'error': 'some error'})
    result = {}
    user_lat = ""
    user_lon =""
    if False:#isa_academy_pincodes.get(pincode):
        result["found"] = True
    else:
        geolocator = Nominatim(user_agent="geoapiExercises")
        zipcode = int(pincode)
        print(zipcode)
        location = geolocator.geocode(zipcode)
        print(location)
        user_lat = location.latitude
        user_lon = location.longitude

    dist = []
    for pi in isa_academy_pincodes:
        key = list(pi.keys())[0]
        pi_obj = pi[key]
        dis = distance(float(pi_obj['Xlat']) , float(pi_obj['Ylong']), user_lat ,user_lon)
        dist.append({'pincode' : pi  , 'km' : dis })
        print(dis)
    dist = sorted(dist , key=lambda i:i ['km'])

    result = dist
    print(result)

    return JsonResponse({"created" : result} , safe=False)

def api_hotels(request):
    hotels_objs = Hotels.objects.all()
    print(request.GET.get('price'))
    
    if request.GET.get('price'):
        hotels_objs = hotels_objs.filter(price__lte=int(request.GET.get('price')))
    print(request.GET.get('emenities'))
    
    if request.GET.get('emenities'):
        emenities = request.GET.get('emenities').split(',')
        em = []
        for e in emenities:
            try:
                em.append(int(e))
            except Exception as e:
                pass
        try:
            hotels_objs = hotels_objs.filter(emenities__in=(em)).distinct()
        except Exception as e:
            print(e)
    
    payload = []
    for hotel_obj in hotels_objs:
        result = {}
        result['hotel_name'] = hotel_obj.hotel_name
        result['hotel_description'] = hotel_obj.hotel_description
        result['price'] = hotel_obj.price
        result['image'] = hotel_obj.image
        payload.append(result)
    return JsonResponse(payload , safe=False)


def hotel_search(request):
    hotel_name = request.GET.get('hotel_name')
    payload = []
    if hotel_name:
        hotels_objs = Hotels.objects.filter(hotel_name__contains=hotel_name)
        for hotel_obj in hotels_objs:
            result = {}
            result['hotel_name'] = hotel_obj.hotel_name
            result['hotel_description'] = hotel_obj.hotel_description
            result['price'] = hotel_obj.price
            result['image'] = hotel_obj.image
            payload.append(result)
    return JsonResponse(payload , safe=False)
    
        
        
        
        
    
    