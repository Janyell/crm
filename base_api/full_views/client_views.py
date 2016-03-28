#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import *
from django.core.exceptions import ObjectDoesNotExist
from base_api.constants import SORT_TYPE_FOR_CLIENT, DEFAULT_SORT_TYPE_FOR_CLIENT, DEFAULT_NUMBER_FOR_PAGE

from base_api.form import *
from base_api.full_views.helper import get_request_param_as_string


def full_add_edit_client(request):
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
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if 'pk' in request.POST:
            is_interested = 0
            if 'is_interested' in request.POST:
                is_interested = 1
            id_client = request.POST['pk']
            organization = request.POST['organization']
            last_name = request.POST['last_name']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            person_phone = request.POST['person_phone']
            organization_phone = request.POST['organization_phone']
            if '_' in person_phone or '_' in organization_phone:
                out.update({"error": 4})
                out.update({'client_form': form})
                out.update({'page_title': "Редактирование клиента"})
                return render(request, 'client/add_edit_client.html', out)
            email = request.POST['email']
            if organization == '' and last_name == '' and name == '' and patronymic == '':
                out.update({"error": 3})
                out.update({'client_form': form})
                out.update({'page_title': "Редактирование клиента"})
                return render(request, 'client/add_edit_client.html', out)
            if person_phone == '' and organization_phone == '' and email == '':
                out.update({"error": 2})
                out.update({'client_form': form})
                out.update({'page_title': "Редактирование клиента"})
                return render(request, 'client/add_edit_client.html', out)
            type = request.POST['organization-type']
            if 'ip' == type:
                organization_type = u'ИП'
            elif 'ooo' == type:
                organization_type = u'ООО'
            elif 'zao' == type:
                organization_type = u'ЗАО'
            elif 'oao' == type:
                organization_type = u'ОАО'
            elif 'nko' == type:
                organization_type = u'НКО'
            elif 'tszh' == type:
                organization_type = u'ТСЖ'
            elif 'op' == type:
                organization_type = u'ОП'
            else:
                organization_type = u''
            # if organization != '':
            #     if Clients.objects.filter(organization=organization).count() == 0:
            #         if 'save-and-add-order' in form.data:
            #             new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                  patronymic=patronymic, person_phone=person_phone,
            #                                  organization_phone=organization_phone, email=email,
            #                                  organization_type=organization_type, is_interested=is_interested)
            #             new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                            "person_phone", "organization_phone", "email", "is_interested",
            #                                            "organization_type"])
            #             if is_interested == 1:
            #                 return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
            #             return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
            #         elif 'only-save' in form.data:
            #             new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                  patronymic=patronymic, person_phone=person_phone,
            #                                  organization_phone=organization_phone, email=email,
            #                                  organization_type=organization_type, is_interested=is_interested)
            #             new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                            "person_phone", "organization_phone", "email", "is_interested",
            #                                            "organization_type"])
            #             if is_interested == 1:
            #                 return HttpResponseRedirect('/clients/interested/')
            #         return HttpResponseRedirect('/clients/')
            #     else:
            #         exist_org = Clients.objects.get(organization=organization)
            #         if str(exist_org.id) == id_client:
            #             if 'save-and-add-order' in form.data:
            #                 new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                      patronymic=patronymic, person_phone=person_phone,
            #                                      organization_phone=organization_phone, email=email,
            #                                      organization_type=organization_type, is_interested=is_interested)
            #                 new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                                "person_phone", "organization_phone", "email",
            #                                                "organization_type", "is_interested"])
            #                 if is_interested == 1:
            #                     return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
            #                 return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
            #             elif 'only-save' in form.data:
            #                 new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                      patronymic=patronymic, person_phone=person_phone,
            #                                      organization_phone=organization_phone, email=email,
            #                                      organization_type=organization_type, is_interested=is_interested)
            #                 new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                            "person_phone", "organization_phone", "email", "is_interested",
            #                                            "organization_type"])
            #                 if is_interested == 1:
            #                     return HttpResponseRedirect('/clients/interested/')
            #                 return HttpResponseRedirect('/clients/')
            #             return HttpResponseRedirect('/clients/')
            #         else:
            #             out.update({"error": 1})
            #             out.update({'page_title': "Редактирование компании"})
            # else:
            if 'save-and-add-order' in form.data:
                new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         organization_type=organization_type, is_interested=is_interested)
                new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
                                                   "person_phone", "organization_phone", "email", "is_interested",
                                                   "organization_type"])
                if is_interested == 1:
                        return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
            elif 'save-and-upload-file' in form.data:
                new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         organization_type=organization_type, is_interested=is_interested)
                new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
                                                   "person_phone", "organization_phone", "email", "is_interested",
                                                   "organization_type"])
                return HttpResponseRedirect('/uploads/client/?id=%s' % new_client.id)
            else:
                new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         organization_type=organization_type, is_interested=is_interested)
                new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
                                                   "person_phone", "organization_phone", "email", "is_interested",
                                                   "organization_type"])
                get_params = '?'
                if 'search' in request.GET:
                    search = request.GET.get('search')
                    get_params += 'search=' + unicode(search)
                    return HttpResponseRedirect('/search/' + get_params)
                get_params += get_request_param_as_string(request)
                if is_interested == 1:
                    return HttpResponseRedirect('/clients/interested/' + get_params)
                return HttpResponseRedirect('/clients/' + get_params)
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
                type = request.POST['organization-type']
                if 'ip' == type:
                    organization_type = u'ИП'
                elif 'ooo' == type:
                    organization_type = u'ООО'
                elif 'zao' == type:
                    organization_type = u'ЗАО'
                elif 'oao' == type:
                    organization_type = u'ОАО'
                elif 'nko' == type:
                    organization_type = u'НКО'
                elif 'tszh' == type:
                    organization_type = u'ТСЖ'
                elif 'op' == type:
                    organization_type = u'ОП'
                else:
                    organization_type = u''
                role = Roles.objects.get(id=request.user.id, is_deleted=0)
                is_interested = 0
                if 'is_interested' in request.POST:
                    is_interested = 1
                if '_' in person_phone or '_' in organization_phone:
                    out.update({"error": 4})
                    out.update({'client_form': form})
                    out.update({'page_title': "Добавление клиента"})
                    return render(request, 'client/add_edit_client.html', out)
                if organization == '' and last_name == '' and name == '' and patronymic == '':
                    out.update({"error": 3})
                    out.update({'client_form': form})
                    out.update({'page_title': "Добавление клиента"})
                    out.update({'is_interested': 1})
                    return render(request, 'client/add_edit_client.html', out)
                if person_phone == '' and organization_phone == '' and email == '':
                    out.update({"error": 2})
                    out.update({'client_form': form})
                    out.update({'page_title': "Добавление клиента"})
                    return render(request, 'client/add_edit_client.html', out)
                if organization != '':
                    try:
                        is_org_exist = Clients.objects.get(organization_type=organization_type,
                                                           organization=organization,
                                                           organization_phone=organization_phone,
                                                           is_deleted=0)
                    except ObjectDoesNotExist:
                        if 'save-and-upload-file' in form.data:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), is_interested=is_interested,
                                                                role=role, organization_type=organization_type)
                            return HttpResponseRedirect('/uploads/client/?id=%s' % new_client.pk)
                        elif 'only-save' in form.data:
                            get_params = '?'
                            get_params += get_request_param_as_string(request)
                            if is_interested == 1:
                                new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                    patronymic=patronymic, person_phone=person_phone,
                                                                    organization_phone=organization_phone, email=email,
                                                                    creation_date=datetime.now(), is_interested=is_interested,
                                                                    role=role, organization_type=organization_type)
                                return HttpResponseRedirect('/clients/interested/' + get_params)
                            else:
                                new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                    patronymic=patronymic, person_phone=person_phone,
                                                                    organization_phone=organization_phone, email=email,
                                                                    creation_date=datetime.now(), role=role,
                                                                    organization_type=organization_type)
                                return HttpResponseRedirect('/clients/' + get_params)
                        # if 'save-and-add-order' in form.data:
                        else:
                            if is_interested == 1:
                                new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                    patronymic=patronymic, person_phone=person_phone,
                                                                    organization_phone=organization_phone, email=email,
                                                                    creation_date=datetime.now(), is_interested=is_interested,
                                                                    role=role, organization_type=organization_type)
                                return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                            else:
                                new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                    patronymic=patronymic, person_phone=person_phone,
                                                                    organization_phone=organization_phone, email=email,
                                                                    creation_date=datetime.now(), role=role,
                                                                    organization_type=organization_type)
                                return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
                        return HttpResponseRedirect('/clients/')
                    out.update({"error": 1})
                    out.update({'client_form': form})
                    out.update({'page_title': "Добавление клиента"})
                    return render(request, 'client/add_edit_client.html', out)
                else:
                    if 'only-save' in form.data:
                        get_params = '?'
                        get_params += get_request_param_as_string(request)
                        if is_interested == 1:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), is_interested=is_interested,
                                                                role=role, organization_type=organization_type)
                            return HttpResponseRedirect('/clients/interested/' + get_params)
                        else:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), role=role,
                                                                organization_type=organization_type)
                            return HttpResponseRedirect('/clients/' + get_params)
                    elif 'save-and-upload-file' in form.data:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), is_interested=is_interested,
                                                                role=role, organization_type=organization_type)
                            return HttpResponseRedirect('/uploads/client/?id=%s' % new_client.pk)
                    # elif 'save-and-add-order' in form.data:
                    else:
                        if is_interested == 1:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(),
                                                                is_interested=is_interested, role=role,
                                                                organization_type=organization_type)
                            return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                        else:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), role=role,
                                                                organization_type=organization_type)
                            return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
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
                               'organization_type': client.organization_type})
            out.update({'page_title': "Редактирование клиента"})
        else:
            form = ClientForm()
            out.update({'page_title': "Добавление клиента"})
    organizations = []
    for organization in Clients.objects.all().order_by('organization'):
        if organization.organization != "":
            organizations.append(organization.organization.strip())
    out.update({'client_form': form})
    out.update({'organizations': organizations})
    return render(request, 'client/add_edit_client.html', out)


def full_delete_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops')
    id = request.GET['id']
    client = Clients.objects.get(pk=id)
    is_interested = client.is_interested
    client.is_deleted = 1
    client.save(update_fields=["is_deleted"])
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    if is_interested == 0:
        return HttpResponseRedirect('/clients/' + get_params)
    else:
        return HttpResponseRedirect('/clients/interested/' + get_params)


def full_get_clients(request):
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
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_CLIENT)
    sort = SORT_TYPE_FOR_CLIENT.get(sort_key, DEFAULT_SORT_TYPE_FOR_CLIENT)
    try:
        clients = Clients.objects.filter(is_deleted=0, is_interested=0).order_by(sort)
    except TypeError:
        clients = Clients.objects.filter(is_deleted=0, is_interested=0).order_by(*sort)
    number = request.GET.get('length', DEFAULT_NUMBER_FOR_PAGE)
    clients_pages = Paginator(clients, number)
    page = request.GET.get('page')
    try:
        client_list = clients_pages.page(page)
    except PageNotAnInteger:
        client_list = clients_pages.page(1)
    except EmptyPage:
        client_list = clients_pages.page(clients_pages.num_pages)
    for c in client_list:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
        c.files = []
        if Client_Files.objects.filter(client_id=c.id).all() is not None:
            for client_file in Client_Files.objects.filter(client_id=c.id).all():
                if client_file.file is not None and client_file.file != '':
                    client_file.name = client_file.title
                    client_file.url = client_file.file.url
                    c.files.append(client_file)
    out.update({'page_title': "Клиенты"})
    out.update({'clients': client_list})
    out.update({'count': clients.count()})
    return render(request, 'client/get_clients.html', out)


def full_get_interested_clients(request):
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
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_CLIENT)
    sort = SORT_TYPE_FOR_CLIENT.get(sort_key, DEFAULT_SORT_TYPE_FOR_CLIENT)
    try:
        clients = Clients.objects.filter(is_deleted=0).order_by(sort)
    except TypeError:
        clients = Clients.objects.filter(is_deleted=0).order_by(*sort)
    number = request.GET.get('length', DEFAULT_NUMBER_FOR_PAGE)
    clients_pages = Paginator(clients, number)
    page = request.GET.get('page')
    try:
        client_list = clients_pages.page(page)
    except PageNotAnInteger:
        client_list = clients_pages.page(1)
    except EmptyPage:
        client_list = clients_pages.page(clients_pages.num_pages)
    for c in client_list:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
        c.files = []
        if Client_Files.objects.filter(client_id=c.id).all() is not None:
            for client_file in Client_Files.objects.filter(client_id=c.id).all():
                if client_file.file is not None and client_file.file != '':
                    client_file.name = client_file.title
                    client_file.url = client_file.file.url
                    c.files.append(client_file)
    out.update({'page_title': "Люди"})
    out.update({'clients': client_list})
    out.update({'count': clients.count()})
    return render(request, 'client/get_clients.html', out)