#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_add_edit_company(request, action):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if action == 'edit':
            title = request.POST['title']
            last_name = request.POST['last_name']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            new_company = Companies(id=id, title=title, last_name=last_name, name=name, patronymic=patronymic)
            new_company.save(force_update=True)
            return HttpResponseRedirect('/companies/')
        else:
            if form.is_valid():
                title = form.cleaned_data['title']
                last_name = form.cleaned_data['last_name']
                name = form.cleaned_data['name']
                patronymic = form.cleaned_data['patronymic']
                new_company = Companies.objects.create(title=title, last_name=last_name, name=name, patronymic=patronymic)
                return HttpResponseRedirect('/companies/')
    else:
        if action == 'edit':
            company = Companies.objects.get(pk=id)
            form = CompanyForm({'title': company.title, 'last_name': company.last_name,
                                'name': company.name, 'patronymic': company.patronymic})
        else:
            form = CompanyForm()
    out = {}
    out.update({'company_form': form})
    out.update({'page_title': "Добавление компании"})
    return render(request, 'add_edit_company.html', out)


def full_delete_company(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    company = Companies.objects.get(pk=id)
    company.delete()
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