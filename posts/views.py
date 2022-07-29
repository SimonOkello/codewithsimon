from django.shortcuts import redirect, render, get_object_or_404
import requests
import json
from django.conf import settings
from django.contrib import messages

# Create your views here.


def index(request):
    context = {}
    posts_url = f'{settings.CODEWITHSIMON_BASE_URL}/posts/'
    try:
        res = requests.get(posts_url)
        if res.status_code == 200:
            try:
                response = json.loads(res.text)
                print('POSTS:', response)
                context = {'posts': response['posts']}
            except KeyError as error:
                pass
    except requests.exceptions.RequestException as error:
        messages.error(request, str(error))
    return render(request, 'posts/index.html', context)


def post_detail(request, category_slug, post_slug):
    context = {}
    api_url = f'{settings.CODEWITHSIMON_BASE_URL}/posts/{category_slug}/{post_slug}/'
    try:
        res = requests.get(api_url)
        if res.status_code == 200:
            try:
                response = json.loads(res.text)
                context = {
                    'post': response['post'],
                    'trending_this_week': response['trending_this_week'],
                }
            except KeyError as error:
                print('ERROR:', str(error))
                messages.error(request, 'We could not find the blog details.')
    except requests.exceptions.RequestException as error:
        messages.error(request, str(error))
    return render(request, 'posts/post-detail.html', context)


def createPost(request):
    context = {}
    if request.method == 'POST':
        FirstName = request.POST.get('FirstName')
        MiddleName = request.POST.get('MiddleName')
        LastName = request.POST.get('LastName')
        CountryCode = request.POST.get('CountryCode')
        MobileNumber = request.POST.get('MobileNumber')
        DocumentType = request.POST.get('DocumentType')
        DocumentNumber = request.POST.get('DocumentNumber')
        Email = request.POST.get('Email')

        # access_token = get_access_token()
        # headers = {'Authorization': 'Bearer %s' % access_token}
        headers = {'Content-Type': 'application/json'}

        payload = {
            'FirstName': FirstName,
            'MiddleName': MiddleName,
            'LastName': LastName,
            'CountryCode': CountryCode,
            'MobileNumber': MobileNumber,
            'DocumentType': DocumentType,
            'DocumentNumber': DocumentNumber,
            'email': Email,
        }

        endpoint = f'{settings.WAAS_BASE_URL}/posts/'
        try:
            res = requests.post(endpoint, json=payload, headers=headers)
            if res.status_code == 200:
                try:
                    response = json.loads(res.text)
                    if 'RequestId' in response:
                        request.session['RegistrationRequestId'] = response['RequestId']
                        messages.success(request, response['message'])
                        return redirect('confirm-beneficiary-view')
                    else:
                        messages.error(request, response['message'])
                except KeyError as error:
                    messages.error(request, str(error))
        except requests.exceptions.RequestException as error:
            messages.error(request, str(error))
    # form = CreatePostForm()
    # if request.method == 'POST':
    #     form = CreatePostForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('index')
    return render(request, 'posts/new-post.html', {'form': form})


def editPost(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    form = CreatePostForm(instance=obj)
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('index')
    return render(request, 'posts/edit-post.html', {'form': form, 'obj': obj})


def deletePost(request, post_id):
    obj = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('index')
    return render(request, 'posts/delete-confirmation.html', {'obj': obj})
