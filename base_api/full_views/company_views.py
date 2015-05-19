#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.constants import SORT_TYPE_FOR_COMPANY, DEFAULT_SORT_TYPE_FOR_COMPANY, DEFAULT_NUMBER_FOR_PAGE
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
            return HttpResponseRedirect('/companies/')
        else:
            if form.is_valid():
                title = form.cleaned_data['title']
                last_name = form.cleaned_data['last_name']
                name = form.cleaned_data['name']
                patronymic = form.cleaned_data['patronymic']
                if Companies.objects.filter(title=title, is_deleted=0).count() == 0:
                    new_company = Companies.objects.create(title=title, last_name=last_name, name=name,
                                                           patronymic=patronymic)
                    return HttpResponseRedirect('/companies/')
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
    return HttpResponseRedirect('/companies/')


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
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_COMPANY)
    sort = SORT_TYPE_FOR_COMPANY.get(sort_key, DEFAULT_SORT_TYPE_FOR_COMPANY)
    try:
        companies = Companies.objects.filter(is_deleted=0).order_by(sort)
    except TypeError:
        companies = Companies.objects.filter(is_deleted=0).order_by(*sort)
    number = request.GET.get('number', DEFAULT_NUMBER_FOR_PAGE)
    companies_pages = Paginator(companies, number)
    page = request.GET.get('page')
    try:
        company_list = companies_pages.page(page)
    except PageNotAnInteger:
        company_list = companies_pages.page(1)
    except EmptyPage:
        company_list = companies_pages.page(companies_pages.num_pages)
    for c in company_list:
        c.full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out.update({'page_title': "Компании"})
    out.update({'companies': company_list})
    return render(request, 'get_companies.html', out)