from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
from main.models import MadLib, Span
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Count
import random
from bs4 import BeautifulSoup  

import spacy
nlp = spacy.load('en_core_web_sm')

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
    if request.session.get('text', False):
        print(request.session.get('text', False))
    context = {}
    return render(request, 'madlib.html', context)

def custom_madlib(request):
    context = {}
    if request.POST:
        #get values from the template
        text = request.POST.get('text', None)
        swap_percent = request.POST.get('swap_percent', None)
        print('swap', swap_percent)
        soup = BeautifulSoup()
        #identify swap words and generate madlib spans 
        doc = nlp(text)
        word_types = ['NOUN','PROPN','ADJ','VERB','ADV']
        madlib_words = [token.i for token in doc if token.pos_ in word_types]
        swap_percent = 1.0 #TODO add this feature
        number_to_swap = swap_percent * len(madlib_words)
        swap_words = random.choices(madlib_words, k=int(number_to_swap))
        soup_string = '<h4 style="margin-top:20px; padding:10px;" id="theText">'
        for i, token in enumerate(doc):
            
            #add span with id and class if in swap_words
            if i in swap_words:
                print('[s]',token.text)
                new_span = soup.new_tag("span") 
                new_span.attrs['id'] = i 
                new_span.attrs['class'] = token.pos_
                if i+1 < len(doc) and doc[i+1].pos_ == 'PUNCT':
                    soup_string += token.text
                else:
                    soup_string += str(new_span) + ' '
                

            #add the text of regular words
            else:
                print('[ns]',token.text)
                if i+1 < len(doc) and doc[i+1].pos_ == 'PUNCT':
                    soup_string += token.text + ' '
                else:
                    soup_string += token.text + ' '
        soup = BeautifulSoup(soup_string) 
        theText = soup.find("h4")         
    
        context['theText'] = str(theText)
        #auto-fill random choices
        return render(request, 'madlib-result.html', context)

    return render(request, 'custom-madlib-text.html', context)


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


