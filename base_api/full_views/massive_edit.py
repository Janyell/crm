#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from base_api.models import Roles, Orders, Clients, Companies, Products


def massive_delete_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.is_deleted = 1
        order.save(update_fields=["is_deleted"])
    if 'archive' in request.POST:
        return HttpResponseRedirect('/orders/archive/')
    return HttpResponseRedirect('/orders/')


def massive_delete_claims(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.is_deleted = 1
        order.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/claims/')


def massive_delete_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops')
    ids = request.POST.getlist['id[]']
    for id in ids:
        client = Clients.objects.get(pk=id)
        client.is_deleted = 1
        client.save(update_fields=["is_deleted"])
    if 'interested' in request.POST:
        return HttpResponseRedirect('/clients/interested/')
    else:
        return HttpResponseRedirect('/clients/')


def massive_delete_companies(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2 or user_role == 1:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    for id in ids:
        company = Companies.objects.get(pk=id)
        company.is_deleted = 1
        company.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/companies/')


def massive_delete_products(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    for id in ids:
        product = Products.objects.get(pk=id)
        product.is_deleted = 1
        product.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/products/')


def massive_delete_roles(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    for id in ids:
        role = Roles.objects.get(pk=id)
        role.delete()
    return HttpResponseRedirect('/roles/')


def massive_add_in_archive(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.in_archive = 1
        order.save(update_fields=["in_archive"])
    return HttpResponseRedirect('/orders/')


def massive_change_manager_in_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    ids = request.POST.getlist['id[]']
    manager_id = request.POST.get['manager_id']
    for id in ids:
        order = Orders.objects.get(pk=id, is_deleted=0)
        if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/oops/')
        order.role = manager_id
        order.save(update_fields=["role"])
    return HttpResponseRedirect('/orders/')
