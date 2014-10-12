#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_add_edit_company(request):
    out = {}
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if 'pk' in request.POST:
            id_company = request.POST['pk']
            title = request.POST['title']
            last_name = request.POST['last_name']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            if Companies.objects.filter(title=title).count() == 0:
                new_company = Companies(id=id_company, title=title, last_name=last_name, name=name, patronymic=patronymic)
                new_company.save(force_update=True)
                return HttpResponseRedirect('/companies/')
            else:
                exist_company = Companies.objects.get(title=title)
                if str(exist_company.id) == id_company:
                    new_company = Companies(id=id_company, title=title, last_name=last_name,
                                            name=name, patronymic=patronymic)
                    new_company.save(force_update=True)
                    return HttpResponseRedirect('/companies/')
                else:
                    out.update({"error": 1})
                    out.update({'page_title': "Редактирование компании"})
        else:
            if form.is_valid():
                title = form.cleaned_data['title']
                last_name = form.cleaned_data['last_name']
                name = form.cleaned_data['name']
                patronymic = form.cleaned_data['patronymic']
                new_company = Companies.objects.create(title=title, last_name=last_name, name=name, patronymic=patronymic)
                return HttpResponseRedirect('/companies/')
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
    id = request.GET['id']
    company = Companies.objects.get(pk=id)
    company.is_deleted = 1
    company.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/companies/')


def full_get_companies(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    companies = Companies.objects.filter(is_deleted=0)
    for c in companies:
        c.full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out = {}
    out.update({'page_title': "Компании"})
    out.update({'companies': companies})
    return render(request, 'get_companies.html', out)