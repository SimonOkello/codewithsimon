from django.shortcuts import get_object_or_404, render
from django.conf import settings
import requests
import json
from django.contrib import messages

# Create your views here.


def index(request):
    context = {}
    category_url = f'{settings.CODEWITHSIMON_BASE_URL}/dashboard/'
    try:
        res = requests.get(category_url)
        if res.status_code == 200:
            try:
                response = json.loads(res.text)
                context = {
                    'categories': response['categories'],
                    'trending_today': response['trending_today'],
                    'recent_posts': response['recent_posts'],
                    'beginner_posts': response['beginner_posts'],
                }
            except KeyError as error:
                pass
    except requests.exceptions.RequestException as error:
        messages.error(request, str(error))
    return render(request, 'home/index.html', context)


def categoryView(request, slug):
    context = {}
    category_url = f'{settings.CODEWITHSIMON_BASE_URL}/categories/{slug}/'
    try:
        res = requests.get(category_url)
        if res.status_code == 200:
            try:
                response = json.loads(res.text)
                context = {
                    'category': response['category'],
                    'posts': response['posts']
                }
            except KeyError as error:
                pass
    except requests.exceptions.RequestException as error:
        messages.error(request, str(error))
    return render(request, 'home/category.html', context)
