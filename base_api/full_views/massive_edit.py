#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.shortcuts import render
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import Roles, Orders, Clients, Companies, Products, ProductGroups


def massive_delete_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.is_deleted = 1
        order.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if 'in_archive' in request.POST:
        return HttpResponseRedirect('/orders/archive/' + get_params)
    if 'is_claim' in request.POST:
        return HttpResponseRedirect('/claims/' + get_params)
    return HttpResponseRedirect('/orders/' + get_params)


def massive_delete_claims(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.is_deleted = 1
        order.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/claims/' + get_params)


def massive_delete_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops')
    ids = request.POST.getlist('id[]')
    for id in ids:
        client = Clients.objects.get(pk=id)
        client.is_deleted = 1
        client.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if 'is_interested' in request.POST:
        return HttpResponseRedirect('/clients/interested/' + get_params)
    else:
        return HttpResponseRedirect('/clients/' + get_params)


def massive_delete_companies(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2 or user_role == 1:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        company = Companies.objects.get(pk=id)
        company.is_deleted = 1
        company.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/companies/' + get_params)


def massive_delete_products(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        product = Products.objects.get(pk=id)
        product.is_deleted = 1
        product.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/products/' + get_params)


def massive_delete_roles(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        role = Roles.objects.get(pk=id)
        role.is_deleted = 1
        role.save(update_fields=["is_deleted"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/roles/' + get_params)


def massive_add_in_archive(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.in_archive = 1
        order.save(update_fields=["in_archive"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/orders/' + get_params)


def massive_change_manager_in_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    manager_id = request.POST.get('manager_id')
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.role = Roles.objects.get(id=manager_id)
        order.save(update_fields=["role"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if 'in_archive' in request.POST:
        return HttpResponseRedirect('/orders/archive/' + get_params)
    if 'is_claim' in request.POST:
        return HttpResponseRedirect('/claims/' + get_params)
    return HttpResponseRedirect('/orders/' + get_params)


def massive_deactivate_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        product = Products.objects.get(pk=id, is_deleted=0)
        product.is_active = 0
        product.save(update_fields=["is_active"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/products/' + get_params)


def massive_activate_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        product = Products.objects.get(pk=id, is_deleted=0)
        product.is_active = 1
        product.save(update_fields=["is_active"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/products/' + get_params)


def massive_change_product_group(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    group_id = request.POST.get('group_id')
    for id in ids:
        product = Products.objects.get(pk=id, is_deleted=0)
        product.group = ProductGroups.objects.get(id=group_id)
        product.save(update_fields=["group"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/products/' + get_params)


def massive_delete_product_groups(request):
    pass