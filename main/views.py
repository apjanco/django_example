from django.shortcuts import render
from django.http import JsonResponse

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
        data = request.POST.get('data', None)
        print(data)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'message':'error'}, safe=False)

    