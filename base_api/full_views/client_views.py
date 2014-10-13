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
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if 'pk' in request.POST:
            id_client = request.POST['pk']
            organization = request.POST['organization']
            last_name = request.POST['last_name']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            person_phone = request.POST['person_phone']
            organization_phone = request.POST['organization_phone']
            email = request.POST['email']
            account_number = request.POST['account_number']
            if organization == '' and last_name == '' and name == '' and patronymic == '':
                out.update({"error": 3})
                out.update({'client_form': form})
                out.update({'page_title': "Редактирование клиента"})
                return render(request, 'add_edit_client.html', out)
            if person_phone == '' and organization_phone == '' and email == '':
                out.update({"error": 2})
                out.update({'client_form': form})
                out.update({'page_title': "Редактирование клиента"})
                return render(request, 'add_edit_client.html', out)
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
            if organization != '':
                if Clients.objects.filter(organization=organization).count() == 0:
                    if 'save-and-add-order' in form.data:
                        new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         account_number=account_number)
                        new_client.save(force_update=True)
                        return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                    elif 'only-save' in form.data:
                        new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         account_number=account_number)
                        new_client.save(force_update=True)
                        return HttpResponseRedirect('/clients/')
                    return HttpResponseRedirect('/clients/')
                else:
                    exist_org = Clients.objects.get(organization=organization)
                    if str(exist_org.id) == id_client:
                        if 'save-and-add-order' in form.data:
                            new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                             patronymic=patronymic, person_phone=person_phone,
                                             organization_phone=organization_phone, email=email,
                                             account_number=account_number)
                            new_client.save(force_update=True)
                            return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                        elif 'only-save' in form.data:
                            new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                             patronymic=patronymic, person_phone=person_phone,
                                             organization_phone=organization_phone, email=email,
                                             account_number=account_number)
                            new_client.save(force_update=True)
                            return HttpResponseRedirect('/clients/')
                        return HttpResponseRedirect('/clients/')
                    else:
                        out.update({"error": 1})
                        out.update({'page_title': "Редактирование компании"})
            else:
                if 'save-and-add-order' in form.data:
                    new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                    patronymic=patronymic, person_phone=person_phone,
                                                    organization_phone=organization_phone, email=email,
                                                    account_number=account_number)
                    return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                elif 'only-save' in form.data:
                    new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                    patronymic=patronymic, person_phone=person_phone,
                                                    organization_phone=organization_phone, email=email,
                                                    account_number=account_number)
                    return HttpResponseRedirect('/clients/')
                return HttpResponseRedirect('/clients/')
        else:
            if form.is_valid():
                organization = form.cleaned_data['organization']
                last_name = form.cleaned_data['last_name']
                name = form.cleaned_data['name']
                patronymic = form.cleaned_data['patronymic']
                person_phone = form.cleaned_data['person_phone']
                organization_phone = form.cleaned_data['organization_phone']
                email = form.cleaned_data['email']
                account_number = form.cleaned_data['account_number']
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
                        is_org_exist = Clients.objects.get(organization=organization)
                    except ObjectDoesNotExist:
                        if 'save-and-add-order' in form.data:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                is_interested=0, account_number=account_number)
                            return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                        elif 'only-save' in form.data:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                is_interested=1, account_number=account_number)
                            return HttpResponseRedirect('/clients/')
                        return HttpResponseRedirect('/clients/')
                    out.update({"error": 1})
                    out.update({'client_form': form})
                    out.update({'page_title': "Добавление клиента"})
                    return render(request, 'add_edit_client.html', out)
                else:
                    if 'save-and-add-order' in form.data:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            is_interested=0, account_number=account_number)
                        return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                    elif 'only-save' in form.data:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            is_interested=1, account_number=account_number)
                        return HttpResponseRedirect('/clients/')
                    return HttpResponseRedirect('/clients/')
            else:
                out.update({'page_title': "Добавление клиента"})
    else:
        if 'id' in request.GET:
            id_client = request.GET['id']
            out.update({"error": 0})
            client = Clients.objects.get(pk=id_client)
            form = ClientForm({'last_name': client.last_name, 'name': client.name, 'patronymic': client.patronymic,
                               'organization': client.organization, 'person_phone': client.person_phone, 'pk': id_client,
                               'organization_phone': client.organization_phone, 'email': client.email,
                               'account_number': client.account_number})
            out.update({'page_title': "Редактирование клиента"})
        else:
            form = ClientForm()
            out.update({'page_title': "Добавление клиента"})
    out.update({'client_form': form})
    return render(request, 'add_edit_client.html', out)


def full_delete_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops')
    id = request.GET['id']
    client = Clients.objects.get(pk=id)
    client.is_deleted = 1
    client.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/clients/')


def full_get_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    clients = Clients.objects.filter(is_deleted=0, is_interested=0)
    for c in clients:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out.update({'page_title': "Клиенты"})
    out.update({'clients': clients})
    return render(request, 'get_clients.html', out)


def full_get_interested_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    clients = Clients.objects.filter(is_interested=1, is_deleted=0)
    for c in clients:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out.update({'page_title': "Интересовавшиеся клиенты"})
    out.update({'clients': clients})
    return render(request, 'get_clients.html', out)