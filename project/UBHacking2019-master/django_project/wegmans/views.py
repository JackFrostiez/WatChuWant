from django.shortcuts import render
from django.http import HttpResponse
import requests
import random

headers = {'Subscription-Key': '9ac371482a4542b6a1045de771eac60e'}
time = None;
input = None;


def land(request):
    return render(request, 'wegmans/land.html', {'title': 'Welcome',})

def pregenerated(request):
    global input
    input = request.POST.get('event')
    return render(request, 'wegmans/pre_generated.html', {'title' : 'Time?'})


def generated(request):
    global time
    global input
    time = request.POST.get('minutes')

    response = requests.get('https://api.wegmans.io/meals/recipes/search?query=' + input + '&api-version=2018-10-18', headers).json()
    list_of_recipes = response['results']

    acceptable_recipes = []

    for i in list_of_recipes:
        recipe = requests.get('https://api.wegmans.io/meals/recipes/' + i['id'] + '?api-version=2018-10-18', headers).json()
        i.update({'link':recipe['_links'][1]['href']})

        # total min time = prep min time + cook min time
        total_min_time = recipe['preparationTime']['min'] + recipe['cookingTime']['min']
        if(total_min_time <= float(time)):
            acceptable_recipes.append(i)


    return render(request, 'wegmans/generated.html', {
        'title' : 'Recipes',
        'list_of_acceptable_recipes' : acceptable_recipes,
        'input' : input,
        'time' : time,
    })
