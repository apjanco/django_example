from django.shortcuts import render
from django.http import JsonResponse
import json
from main.models import MadLib, Span
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Count



import names 
import requests
# Create your views here.
def home(request):
    context = {}

    context['name'] = names.get_full_name()
    context['words'] = ', '.join([a['word'] for a in requests.get('http://api.wordnik.com:80/v4/words.json/randomWords?hasDictionaryDef=true&minCorpusCount=0&minLength=5&maxLength=15&limit=10&api_key=a2a73e7b926c924fad7001ca3111acd55af2ffabf50eb4ae5').json()])
    context['quotes'] = requests.get('https://thesimpsonsquoteapi.glitch.me/quotes?count=10').json()

    return render(request, 'index.html', context)

def madlib(request):
    context = {}
    return render(request, 'madlib.html', context)

def madlib_data(request):
    if request.POST:
        data = request.POST.get('spans', None)
        data = json.loads(data)
        madlib, created = MadLib.objects.get_or_create(created=make_aware(datetime.now()), text=data['full_text'])
        for span in data.keys():
            if span == 'full_text':
                pass
            else:
                madlib.spans.create(span_id=span,pos=data[span]['class'],text=data[span]['text'])
        madlib.save()
        return madlib_stats()
    else:
        return JsonResponse({'message':'error'}, safe=False)

def madlib_stats():
    #total number of spans 
    data = {}
    data['total_count'] = len(Span.objects.all())
    for pos in list(Span.objects.values('pos').order_by('pos').annotate(count=Count('pos'))):
        data[pos['pos']] = pos['count']
    return JsonResponse(data, safe=False)


