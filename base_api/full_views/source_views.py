#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import *
from base_api.form import *
from django.http import *


def full_delete_source(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    source = Sources.objects.get(pk=id)
    source.is_deleted = 1
    source.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/settings/sources/' + get_params)


def full_get_sources(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            is_active = True
            if 'is_active' in request.POST:
                is_active = int(request.POST['is_active'])
            new_source = Sources.objects.create(title=title, is_active=is_active)
            return HttpResponseRedirect('/settings/sources/' + get_params)
        else:
            out.update({"error": 1})
    else:
        form = SourceForm()
    sources = Sources.objects.filter(is_deleted=0)
    source_edit_form = SourceEditForm()
    out.update({'page_title': "Источники"})
    out.update({'entities': sources})
    out.update({'entity_form': form})
    out.update({'count': sources.count()})
    out.update({'entity_edit_form': source_edit_form})
    return render(request, 'setting/get_sources.html', out)


def full_edit_source(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        id = request.GET['id']
        source = Sources.objects.get(id=id)
        title = request.POST['title']
        is_active = int(request.POST['is_active'])
        source.title = title
        source.is_active = is_active
        source.save()
        return HttpResponseRedirect('/settings/sources/' + get_params)
    return HttpResponseRedirect('/settings/sources/' + get_params)
