#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from base_api.models import Roles, Orders, Clients, Companies, Products


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
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
    if 'archive' in request.POST:
        return HttpResponseRedirect('/orders/archive/' + get_params)
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
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
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
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
    if 'interested' in request.POST:
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
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
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
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
    return HttpResponseRedirect('/products/' + get_params)


def massive_delete_roles(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    for id in ids:
        role = Roles.objects.get(pk=id)
        role.delete()
    get_params = '?'
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
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
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += str(length) + '&'
    if 'sort' in request.GET:
        sort = int(request.GET['sort'])
        get_params += str(sort) + '&'
    return HttpResponseRedirect('/orders/' + get_params)


def massive_change_manager_in_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist('id[]')
    manager_id = request.POST.get['manager_id']
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.role = manager_id
        order.save(update_fields=["role"])
    return HttpResponseRedirect('/orders/')
