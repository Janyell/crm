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
from datetime import timedelta
from datetime import date
from django.db.models import Q
from django.db.models import Count


def full_do_task(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    task = Tasks.objects.get(pk=id)
    task.is_done = 1
    task.results = request.POST.get('results', '')
    task.save(update_fields=["is_done", "results"])
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
    roles = [Roles(username='все менеджеры', pk=0)]
    roles += list(Roles.objects.filter(is_deleted=0).filter(Q(role=1) | Q(role=0) | Q(role=3)).all())
    out.update({'roles': roles})
    is_senior = False
    if user_role == 0 or user_role == 3:
        is_senior = True
        out.update({'is_senior': is_senior})
    tasks = Tasks.objects.filter(is_deleted=0, order__is_deleted=0)
    period = 'today'
    if 'period' in request.GET:
        period = request.GET['period']
    if period == 'today':
        end_date = datetime.today() + timedelta(days=1)
    elif period == 'week':
        end_date = datetime.today() + timedelta(days=7)
    elif period == 'month':
        end_date = datetime.today() + timedelta(days=32)
    elif period == 'year':
        end_date = datetime.today() + timedelta(days=366)
    tasks = tasks.filter(date__lte=end_date)
    if 'manager' in request.GET:
        manager_id = request.GET['manager']
        if manager_id != '0':
            role = Roles.objects.get(id=manager_id)
            tasks = tasks.filter(role=role)
    if not is_senior:
        tasks = tasks.filter(role=Roles.objects.get(id=request.user.id))
    task_count = tasks.count()
    from collections import defaultdict
    from collections import OrderedDict
    task_date_dict = defaultdict(list)
    for task in tasks.order_by('date', 'is_done').all():
        if task.is_done:
            task.comment = task.results
        task_date = task.date.date()
        if task_date not in task_date_dict:
            task_date_dict.update({task_date: []})
        task_date_dict[task_date].append(task)
    out.update({'tasks_dict': OrderedDict(sorted(task_date_dict.items()))})
    out.update({'page_title': "Задачи"})
    out.update({'task_do_form': TaskForm()})
    out.update({'tasks': tasks})
    out.update({'count': task_count})
    return render(request, 'task/get_tasks.html', out)
