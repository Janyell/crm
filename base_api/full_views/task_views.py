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
    # because fuck the logic
    if request.GET.get('is_done', 0) == '1':
        tasks = tasks.filter(is_done=0)
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
        if task.order.client.organization == '':
            task.order.client.organization_or_full_name = task.order.client.last_name + ' ' + task.order.client.name + ' ' + task.order.client.patronymic
        else:
            task.order.client.organization_or_full_name = task.order.client.organization
        task.order.client.full_name = ''
        task.order.client.email = ''
        task.order.client.person_phone = ''
        contact_faces = ContactFaces.objects.filter(organization=task.order.client.id, is_deleted=0).all()
        for contact_face in contact_faces:
            if task.order.client.full_name and task.order.client.full_name != '':
                task.order.client.full_name += ', '
            task.order.client.full_name = task.order.client.full_name + contact_face.last_name + ' ' \
                                 + contact_face.name + ' ' + contact_face.patronymic
            for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                if email.email:
                    if task.order.client.email and task.order.client.email != '':
                        task.order.client.email += ', '
                    task.order.client.email = task.order.client.email + email.email + ' (' + contact_face.last_name + ' ' \
                                         + contact_face.name + ' ' + contact_face.patronymic + ')'
            for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                if phone.phone:
                    if task.order.client.person_phone and task.order.client.person_phone != '':
                        task.order.client.person_phone += ', '
                    task.order.client.person_phone = task.order.client.person_phone + phone.phone + ' (' + \
                                                contact_face.last_name + ' ' + contact_face.name + ' ' + \
                                                contact_face.patronymic + ')'
        if task.is_done:
            task.results = task.results
        task_date = task.date.date()
        if task_date not in task_date_dict:
            task_date_dict.update({task_date: []})
        task_date_dict[task_date].append(task)
    out.update({'tasks_dict': OrderedDict(sorted(task_date_dict.items()))})
    out.update({'page_title': "Задачи"})
    TaskForm.base_fields['type'] = TaskTypeChoiceField(queryset=TaskTypes.objects.filter(is_deleted=0))
    out.update({'task_do_form': TaskForm()})
    out.update({'edit_task_form': TaskForm(initial={'is_important': False})})
    out.update({'tasks': tasks})
    out.update({'count': task_count})
    return render(request, 'task/get_tasks.html', out)


def full_edit_task(request):
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
        id = request.GET['id']
        task = Tasks.objects.get(id=id)
        comment = request.POST['task_comment']
        date = request.POST['date']
        if date:
            try:
                date = datetime.strptime(date, '%d.%m.%Y %H:%M')
            except Exception:
                date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        else:
            date = None
        if 'is_important' in request.POST:
            is_important = True
        else:
            is_important = False
        type = TaskTypes.objects.get(id=request.POST['type'])
        task.comment = comment
        task.date = date
        task.is_important = is_important
        task.type = type
        task.save()
        return HttpResponseRedirect('/tasks/' + get_params)
    return HttpResponseRedirect('/tasks/' + get_params)
