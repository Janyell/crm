#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import *
from base_api.form import *
from django.http import *


def full_add_city(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            name = request.POST['name']
            if Cities.objects.filter(name=name).count() == 0:
                new_city = Cities.objects.create(name=name)
                return HttpResponseRedirect('/' + get_params)
            else:
                out.update({"error": 1})
                out.update({'page_title': "Добавление города"})
        else:
            out.update({'page_title': "Добавление города"})
    else:
        form = CityForm()
    out.update({'form': form})
    return render(request, 'add_city.html', out)
