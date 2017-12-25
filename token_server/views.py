# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from token_server.models import Market, AdminAccount, TokenType, CustomerTokenBinding, TokenKey
from django.utils.crypto import get_random_string
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, requires_csrf_token, csrf_exempt
import jwt

secret_key = "dc2bd2a004f7ea14c05ba8aa07345"
# Create your views here.

def loginview(request):
    c = {}
    return render_to_response('login.html', c)

def decrypt(payload):
    payload = jwt.decode(payload, secret_key, algorithms=['HS256'])
    return payload

@csrf_exempt
def auth_and_login(request, onsuccess='/', onfail='/login/'):
    # Obtain our request's context.
    context_dict = {}
    # If HTTP POST, pull out form data and process it.
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Attempt to log the user in with the supplied credentials.
        # A User object is returned if correct - None if not.
        user = authenticate(username=username, password=password)

        # A valid user logged in?
        if user is not None:
            # Check if the account is active (can be used).
            # If so, log the user in and redirect them to the homepage.
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/token_server/index/')
            # The account is inactive; tell by adding variable to the template context.
            else:
                context_dict['disabled_account'] = True
                return render(request, 'login.html', context_dict)
        # Invalid login details supplied!
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            context_dict['bad_details'] = True
            return render(request,'login.html', context_dict)

    # Not a HTTP POST - most likely a HTTP GET. In this case, we render the login form for the user.
    else:
        return render(request, 'login.html', context_dict)

@login_required
def user_logout(request):
    # As we can assume the user is logged in, we can just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/login/')

def create_user(username, email, password):
    user = User(username=username, email=email)
    user.set_password(password)
    user.save()
    return user


def user_exists(username):
    user_count = User.objects.filter(username=username).count()
    if user_count == 0:
        return False
    return True

def login_view(request):
    context = RequestContext(request)
    context_dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/token_server/index/')
        else:
            context_dict['bad_details'] = True
            return render_to_response('login.html', context_dict, context)

@login_required(login_url='/token_server/login/')
def index_view(request):
    context_dict = {}

    token_key_free_list = TokenKey.objects.filter(customertokenbinding__isnull=True).distinct()
    token_key_used_list = TokenKey.objects.filter(customertokenbinding__isnull=False).distinct()
    context_dict['token_key_used_list'] = token_key_used_list
    context_dict['token_key_free_list'] = token_key_free_list

    return render(request, 'index.html', context_dict)


@csrf_exempt
def token_binding(request):
    reponse_object = {}
    if request.method == 'POST':
        if 'payload' in request.POST:
            try:
                payload = jwt.decode(request.POST['payload'], secret_key, algorithms=['HS256'])
                api_key = payload['api_key']
                token_key = payload['token_key']
                customer_email = payload['customer_email']
                market = Market.objects.get(pk=1)
                token_object = TokenKey.objects.filter(token_hash=token_key, active_flag=True)

                if token_object:
                    token_object = token_object[0]
                    old_binding = CustomerTokenBinding.objects.filter(token_key=token_object, market=market)
                    if old_binding:
                        reponse_object['result'] = False
                        reponse_object['message'] = 'Token in used.'
                        return JsonResponse(reponse_object)

                    token_object.customer_email = customer_email
                    token_object.save()
                    token_child = CustomerTokenBinding(token_key=token_object, api_key=api_key, market=market)
                    token_child.save()
                    reponse_object['result'] = True
                    reponse_object['message'] = 'Token register successfully.'
                    return JsonResponse(reponse_object)
                else:
                    reponse_object['result'] = False
                    reponse_object['message'] = 'Invalid token information. Please contact admin.'
                    return JsonResponse(reponse_object)
            except jwt.InvalidTokenError:
                reponse_object['result'] = False
                reponse_object['message'] = 'Invalid request. Please retry'
                return JsonResponse(reponse_object)
        else:
            reponse_object['result'] = False
            reponse_object['message'] = 'Invalid request. Please retry'
            return JsonResponse(reponse_object)
    else:
        reponse_object['result'] = False
        reponse_object['message'] = 'Invalid request. Please retry'
        return JsonResponse(reponse_object)


def token_detail(request, pk):
    pass

@csrf_exempt
def token_validation(request):
    reponse_object = {}
    if request.method == 'POST':
        if 'api_key' in request.POST:
            api_key = request.POST['api_key']
            market = Market.objects.get(pk=1)
            child_token = CustomerTokenBinding.objects.filter(api_key=api_key, active_flag=1, market=market)

            if child_token:
                reponse_object['result'] = True
                reponse_object['message'] = 'Token validation success.'
                return JsonResponse(reponse_object)
            else:
                reponse_object['result'] = False
                reponse_object['message'] = 'Token validation failed.'
                return JsonResponse(reponse_object)
    else:
        reponse_object['result'] = False
        reponse_object['message'] = 'Invalid request'
        return JsonResponse(reponse_object)

@login_required(login_url='/token_server/login/')
def token_add(request, pk_type):
    random_token = get_random_string(16)
    if int(pk_type) == 1:
        normal_type = TokenType.objects.filter(id=pk_type)[0]
        new_token_key = TokenKey(token_hash=random_token, token_type=normal_type)
        new_token_key.save()
        return HttpResponseRedirect('/token_server/index/')
    elif int(pk_type) == 2:
        trial_type = TokenType.objects.filter(id=pk_type)[0]
        new_token_key = TokenKey(token_hash=random_token, token_type=trial_type)
        new_token_key.save()
        return HttpResponseRedirect('/token_server/index/')
