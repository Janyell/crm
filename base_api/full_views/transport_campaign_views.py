#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import *
from base_api.form import *
from django.http import *


def full_delete_transport_campaign(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    transport_campaign = TransportCampaigns.objects.get(pk=id)
    transport_campaign.is_deleted = 1
    transport_campaign.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/settings/transport_campaigns/' + get_params)


def full_get_transport_campaigns(request):
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
        form = TransportCampaignForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            is_active = True
            if 'is_active' in request.POST:
                is_active = int(request.POST['is_active'])
            new_transport_campaign = TransportCampaigns.objects.create(title=title, is_active=is_active)
            return HttpResponseRedirect('/settings/transport_campaigns/' + get_params)
        else:
            out.update({"error": 1})
    else:
        form = TransportCampaignForm()
    transport_campaigns = TransportCampaigns.objects.filter(is_deleted=0)
    transport_campaign_edit_form = TransportCampaignEditForm()
    out.update({'page_title': "Транспортные компании"})
    out.update({'transport_campaigns': transport_campaigns})
    out.update({'transport_campaign_form': form})
    out.update({'count': transport_campaigns.count()})
    out.update({'transport_campaign_edit_form': transport_campaign_edit_form})
    return render(request, 'setting/get_transport_campaigns.html', out)


def full_edit_transport_campaign(request):
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
        transport_campaign = TransportCampaigns.objects.get(id=id)
        title = request.POST['title']
        is_active = int(request.POST['is_active'])
        transport_campaign.title = title
        transport_campaign.is_active = is_active
        transport_campaign.save()
        return HttpResponseRedirect('/settings/transport_campaigns/' + get_params)
    return HttpResponseRedirect('/settings/transport_campaigns/' + get_params)
