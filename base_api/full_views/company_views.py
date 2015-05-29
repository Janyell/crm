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


def full_add_edit_company(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2 or user_role == 1:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if 'pk' in request.POST:
            id_company = request.POST['pk']
            title = request.POST['title']
            last_name = request.POST['last_name']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            new_company = Companies(id=id_company, title=title, last_name=last_name, name=name, patronymic=patronymic)
            new_company.save(force_update=True)
            return HttpResponseRedirect('/companies/' + get_params)
        else:
            if form.is_valid():
                title = form.cleaned_data['title']
                last_name = form.cleaned_data['last_name']
                name = form.cleaned_data['name']
                patronymic = form.cleaned_data['patronymic']
                if Companies.objects.filter(title=title, is_deleted=0).count() == 0:
                    new_company = Companies.objects.create(title=title, last_name=last_name, name=name,
                                                           patronymic=patronymic)
                    return HttpResponseRedirect('/companies/' + get_params)
                else:
                    out.update({"error": 1})
                    out.update({'page_title': "Добавление компании"})
            else:
                out.update({'page_title': "Добавление компании"})
    else:
        if 'id' in request.GET:
            id_company = request.GET['id']
            out.update({"error": 0})
            company = Companies.objects.get(pk=id_company)
            form = CompanyForm({'title': company.title, 'last_name': company.last_name,
                                'name': company.name, 'patronymic': company.patronymic})
            out.update({'page_title': "Редактирование компании"})
        else:
            form = CompanyForm()
            out.update({'page_title': "Добавление компании"})
    out.update({'company_form': form})
    return render(request, 'add_edit_company.html', out)


def full_delete_company(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2 or user_role == 1:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    company = Companies.objects.get(pk=id)
    company.is_deleted = 1
    company.save(update_fields=["is_deleted"])
    get_params = '?'
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += 'page=' + str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += 'length=' + str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += 'sort=' + str(sort) + '&'
    return HttpResponseRedirect('/companies/' + get_params)


def full_get_companies(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2 or user_role == 1:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    # companies = Companies.search.query(u'ООО').filter(is_deleted=0)
    # companies = Companies.objects.filter(is_deleted=0)
    companies = list(Companies.search.query(u'ХИТ*').filter(is_deleted=0))
    for c in companies:
        c.full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out.update({'page_title': "Компании"})
    out.update({'companies': companies})
    return render(request, 'get_companies.html', out)