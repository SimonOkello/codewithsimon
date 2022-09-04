from email import message
import json
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
import requests
# Create your views here.


def user_login(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        if email != 'simonokello.dev@gmail.com' or password != '123':
            error = 'Invalid Credentials. Please try again.'
            messages.error(request, error)
        else:

            payload = {
                'email': email,
                'password': password
            }
            url = f'{settings.CODEWITHSIMON_BASE_URL}/auth/login/'
            headers = {
                'Content-Type': 'application/json'
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                json_response = json.loads(response.text)
                if 'message' not in json_response:
                    message = json_response['email'][0]
                else:
                    message = json_response['message']
                if 'status' not in json_response:
                    status = False
                else:
                    status = json_response['status']
                if status:
                    print('RESPONSE:', json_response)
                    # session['access_token']=json_response['access_token']
                    # session['refresh_token']=json_response['refresh_token']
                    request.session['user'] = json_response['user']
                    # messages.success(request, message)
                    return redirect('home:index')
                else:
                    messages.error(request, message)
            except requests.exceptions.RequestException as e:
                print('ERROR:', str(e))
                messages.error(request, f'{e}')
            except Exception as e:
                print('ERROR:', str(e))
                messages.error(request, f'{e}')
    return render(request, 'authentication/user-login.html', context)
