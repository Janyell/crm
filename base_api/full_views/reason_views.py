#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import *
from base_api.form import *
from django.http import *


def full_delete_reason(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    reason = CloseReasons.objects.get(pk=id)
    reason.is_deleted = 1
    reason.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/settings/reasons/' + get_params)


def full_get_reasons(request):
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
        form = CloseReasonsForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            is_active = True
            new_reason = CloseReasons.objects.create(title=title)
            return HttpResponseRedirect('/settings/reasons/' + get_params)
        else:
            out.update({"error": 1})
    else:
        form = CloseReasonsForm()
    reasons = CloseReasons.objects.filter(is_deleted=0)
    reason_edit_form = CloseReasonsEditForm()
    out.update({'page_title': "Причины закрытия заявок"})
    out.update({'entities': reasons})
    out.update({'entity_form': form})
    out.update({'count': reasons.count()})
    out.update({'entity_edit_form': reason_edit_form})
    return render(request, 'setting/get_reasons.html', out)


def full_edit_reason(request):
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
        reason = TransportCampaigns.objects.get(id=id)
        title = request.POST['title']
        is_active = int(request.POST['is_active'])
        reason.title = title
        reason.is_active = is_active
        reason.save()
        return HttpResponseRedirect('/settings/transport_companies/' + get_params)
    return HttpResponseRedirect('/settings/transport_companies/' + get_params)
