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
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    product = Products.objects.get(pk=id)
    product.is_deleted = 1
    product.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/products/' + get_params)


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
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            new_product = Products.objects.create(title=title, price=price)
            return HttpResponseRedirect('/products/' + get_params)
        else:
            out.update({"error": 1})
    else:
        form = ProductForm()
    products = Products.objects.filter(is_deleted=0)
    for product in products:
        product.price_right_format = right_money_format(product.price)
    product_edit_form = ProductEditForm()
    out.update({'page_title': "Продукты"})
    out.update({'products': products})
    out.update({'product_form': form})
    out.update({'product_edit_form': product_edit_form})
    return render(request, 'get_products.html', out)


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
        product.title = title
        product.price = price
        product.save(force_update=True)
        return HttpResponseRedirect('/products/' + get_params)
    return HttpResponseRedirect('/products/' + get_params)