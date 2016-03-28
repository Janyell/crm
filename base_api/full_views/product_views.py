#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.full_views.helper import get_request_param_as_string
from base_api.full_views.order_views import right_money_format
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_delete_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    product = Products.objects.get(pk=id)
    product.is_deleted = 1
    product.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/products/' + get_params)


def full_delete_product_group(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    product_group = ProductGroups.objects.get(pk=id)
    product_group.is_deleted = 1
    product_group.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/product_groups/' + get_params)


def full_get_products(request):
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
    get_params = '?'
    get_params += get_request_param_as_string(request)
    ProductForm.base_fields['group'] = ProductGroupModelChoiceField(queryset=ProductGroups.objects.filter(is_deleted=0),
                                                                    required=False)
    ProductEditForm.base_fields['group'] = ProductGroupModelChoiceField(queryset=ProductGroups.objects.filter(is_deleted=0),
                                                                        required=False)
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            group = form.cleaned_data['group']
            new_product = Products.objects.create(title=title, price=price, group=group, is_active=1)
            return HttpResponseRedirect('/products/' + get_params)
        else:
            out.update({"error": 1})
    else:
        form = ProductForm()
    products = Products.objects.filter(is_deleted=0)
    for product in products:
        product.price_right_format = right_money_format(product.price)
    product_edit_form = ProductEditForm()
    product_groups = ProductGroups.objects.filter(is_deleted=0)
    out.update({'page_title': "Продукты"})
    out.update({'products': products})
    out.update({'product_form': form})
    out.update({'product_edit_form': product_edit_form})
    out.update({'count': products.count()})
    out.update({'product_groups': product_groups})
    return render(request, 'product/get_products.html', out)


def full_get_product_groups(request):
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
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        form = ProductGroupForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            new_product_group = ProductGroups.objects.create(title=title)
            return HttpResponseRedirect('/product_groups/' + get_params)
        else:
            out.update({"error": 1})
    else:
        form = ProductGroupForm()
    product_group_edit_form = ProductGroupEditForm()
    product_groups = ProductGroups.objects.filter(is_deleted=0)
    out.update({'page_title': "Группы товаров"})
    out.update({'product_groups': product_groups})
    out.update({'product_group_form': form})
    out.update({'product_group_edit_form': product_group_edit_form})
    out.update({'count': product_groups.count()})
    return render(request, 'product/get_product_groups.html', out)


def full_edit_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        id = request.GET['id']
        product = Products.objects.get(id=id)
        title = request.POST['title']
        price = request.POST['price']
        group = request.POST['group']
        is_active = int(request.POST['is_active'])
        product.title = title
        product.price = price
        if group:
            product.group = ProductGroups.objects.get(id=group)
        else:
            product.group = None
        product.is_active = is_active
        product.save()
        return HttpResponseRedirect('/products/' + get_params)
    return HttpResponseRedirect('/products/' + get_params)


def full_edit_product_group(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        id = request.GET['id']
        product_group = ProductGroups.objects.get(id=id)
        title = request.POST['title']
        product_group.title = title
        product_group.save()
        return HttpResponseRedirect('/product_groups/' + get_params)
    return HttpResponseRedirect('/product_groups/' + get_params)