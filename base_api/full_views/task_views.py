#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_do_task(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    task = Tasks.objects.get(pk=id)
    task.is_done = 1
    task.save(update_fields=["is_done"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/tasks/' + get_params)


def full_get_tasks(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if user_role == 0 or user_role == 3:
        out.update({'is_senior': True})
    tasks = Tasks.objects.filter(is_deleted=0)
    out.update({'page_title': "Задачи"})
    out.update({'tasks': tasks})
    out.update({'count': tasks.count()})
    return render(request, 'task/get_tasks.html', out)
