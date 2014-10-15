#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_add_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            new_product = Products.objects.create(title=title)
            return HttpResponseRedirect('/products/')
        else:
            out.update({'page_title': "Добавление продукта"})
            out.update({"error": 1})
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


def full_delete_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    product = Products.objects.get(pk=id)
    product.is_deleted = 1
    product.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/products/')


def full_get_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    products = Products.objects.filter(is_deleted=0)
    out.update({'page_title': "Продукты"})
    out.update({'products': products})
    return render(request, 'get_products.html', out)