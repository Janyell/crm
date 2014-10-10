#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import sys


def full_add_edit_client(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = ClientForm(request.POST)
        out = {}
        if form.is_valid():
            organization = form.cleaned_data['organization']
            last_name = form.cleaned_data['last_name']
            name = form.cleaned_data['name']
            patronymic = form.cleaned_data['patronymic']
            person_phone = form.cleaned_data['person_phone']
            organization_phone = form.cleaned_data['organization_phone']
            email = form.cleaned_data['email']
            if organization == '' and last_name == '' and name == '' and patronymic == '':
                out.update({"error": 3})
                out.update({'client_form': form})
                out.update({'page_title': "Добавление клиента"})
                return render(request, 'add_edit_client.html', out)
            if person_phone == '' and organization_phone == '' and email == '':
                out.update({"error": 2})
                out.update({'client_form': form})
                out.update({'page_title': "Добавление клиента"})
                return render(request, 'add_edit_client.html', out)
            if organization != '':
                try:
                    is_org_exist = Clients.objects.get(organization=organization)
                except ObjectDoesNotExist:
                    type = request.POST['organization-type']
                    if 'ip' == type:
                        organization = u'ИП' + ' ' + organization
                    elif 'ooo' == type:
                        organization = u'ООО' + ' ' + organization
                    elif 'zao' == type:
                        organization = u'ЗАО' + ' ' + organization
                    elif 'oao' == type:
                        organization = u'ОАО' + ' ' + organization
                    elif 'nko' == type:
                        organization = u'НКО' + ' ' + organization
                    elif 'tszh' == type:
                        organization = u'ТСЖ' + ' ' + organization
                    elif 'op' == type:
                        organization = u'ОП' + ' ' + organization
                    new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                        patronymic=patronymic, person_phone=person_phone,
                                                        organization_phone=organization_phone, email=email)
                    if 'save-and-add-order' in form.data:
                        return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                    elif 'only-save' in form.data:
                        return HttpResponseRedirect('/clients/')
                    return HttpResponseRedirect('/clients/')
                out.update({"error": 1})
                out.update({'client_form': form})
                out.update({'page_title': "Добавление клиента"})
                return render(request, 'add_edit_client.html', out)
            else:
                new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                    patronymic=patronymic, person_phone=person_phone,
                                                    organization_phone=organization_phone, email=email)
                if 'save-and-add-order' in form.data:
                    return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                elif 'only-save' in form.data:
                    return HttpResponseRedirect('/clients/')
                return HttpResponseRedirect('/clients/')
        else:
            print(form.errors)
    else:
        form = ClientForm()
    out = {}
    out.update({'client_form': form})
    out.update({'page_title': "Добавление клиента"})
    return render(request, 'add_edit_client.html', out)


def full_get_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    clients = Clients.objects.filter(is_deleted=0)
    for c in clients:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out = {}
    out.update({'page_title': "Клиенты"})
    out.update({'clients': clients})
    return render(request, 'get_clients.html', out)
