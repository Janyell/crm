#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from base_api.full_views.company_views import *
from base_api.full_views.role_views import *
from base_api.full_views.client_views import *


def add_edit_role(request):
    return full_add_edit_role(request)


def delete_role(request):
    return full_delete_roles(request)


def get_roles(request):
    return full_get_roles(request)


def add_edit_company(request, id, action):
    return full_add_edit_company(request, id, action)


def delete_company(request, id):
    return full_delete_company(request, id)


def get_companies(request):
    return full_get_companies(request)


def add_edit_client(request):
    return full_add_edit_client(request)


def get_clients(request):
    return full_get_clients(request)


def add_edit_order(request):
    return render(request, 'add_edit_order.html')


def get_orders(request):
    return render(request, 'get_orders.html')


def analyst(request):
    return render(request, 'index.html')


def log_in(request):
    if not request.user.is_active:
        out = {}
        if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            print (user)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                out.update({"error": 1})
        else:
            form = LoginForm()
        out.update({'login_form': form})
        out.update({'page_title': "Авторизация"})
        return render(request, 'log_in.html', out)
    else:
        return HttpResponseRedirect('/')


def log_out(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    logout(request)
    return HttpResponseRedirect("/login/")


def page_not_found(request):
    out = {}
    out.update({'page_title': "Страница не найдена"})
    return render(request, 'page_not_found.html', out)