#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from base_api.full_views.company_views import *
from base_api.full_views.role_views import *
from base_api.full_views.client_views import *
from base_api.full_views.order_views import *
from base_api.full_views.analyze_full import *


def add_edit_role(request):
    return full_add_edit_role(request)


def delete_role(request):
    return full_delete_roles(request)


def get_roles(request):
    return full_get_roles(request)


def add_edit_company(request):
    return full_add_edit_company(request)


def delete_company(request):
    return full_delete_company(request)


def get_companies(request):
    return full_get_companies(request)


def add_edit_client(request):
    return full_add_edit_client(request)


def delete_client(request):
    return full_delete_clients(request)


def get_clients(request):
    return full_get_clients(request)


def add_edit_order(request):
    return full_add_edit_order(request)


def delete_order(request):
    return full_delete_order(request)


def get_orders(request):
    return full_get_orders(request)


def edit_order_for_factory(request):
    return full_edit_order_for_factory(request)


def analyst(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    return render(request, 'index.html', out)


def log_in(request):
    if not request.user.is_active:
        out = {}
        if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            print (user)
            if user is not None:
                login(request, user)
                if Roles.objects.get(id=request.user.id).role == 2:
                    return HttpResponseRedirect('/orders/')
                else:
                    return HttpResponseRedirect('/')
            else:
                out.update({"error": 1})
        else:
            form = LoginForm()
        out.update({'login_form': form})
        out.update({'page_title': "Авторизация"})
        return render(request, 'log_in.html', out)
    else:
        if Roles.objects.get(id=request.user.id).role == 2:
            return HttpResponseRedirect('/orders/')
        else:
            return HttpResponseRedirect('/')


def log_out(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    logout(request)
    return HttpResponseRedirect("/login/")


def page_not_found(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    out = {'user_role': user_role}
    out.update({'page_title': "Страница не найдена"})
    return render(request, 'page_not_found.html', out)


def permission_deny(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    out = {'user_role': user_role}
    out.update({'page_title': "К сожалению, у вас нет доступа к данной странице"})
    return render(request, 'page_not_found.html', out)


def get_old_orders(request):
    return full_get_old_orders(request)


def add_in_archive(request):
    return full_add_in_archive(request)


def get_interested_clients(request):
    return full_get_interested_clients(request)


def analyze_products(request):
    return full_analyze_products(request)


def view_analyzed_product(request):
    return full_view_analyzed_product(request)


# Менеджер количество выставленных счетов
def analyze_manager_order_give(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    managers = []
    orders_count = []
    managers_ids = Roles.objects.filter(role=1, is_deleted=0)
    for managers_id in managers_ids:
        orders_count.append(Orders.objects.filter(role_id=managers_id, is_deleted=0).count())
        managers.append(str(managers_id.surname + ' ' + managers_id.name))
    amount_str = str(orders_count)[1:-1]
    out.update({'page_title': "Анализ"})
    out.update({'data': amount_str})
    out.update({'managers': managers})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_manager_order_give.html', out)


# Менеджер количество отгрузок
def analyze_manager_order_out(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    managers = []
    orders_count = []
    managers_ids = Roles.objects.filter(role=1, is_deleted=0)
    for managers_id in managers_ids:
        count = Orders.objects.filter(role_id=managers_id, is_deleted=0, order_status=2).count()
        count += Orders.objects.filter(role_id=managers_id, is_deleted=0, order_status=3).count()
        orders_count.append(count)
        managers.append(str(managers_id.surname + ' ' + managers_id.name))
    amount_str = str(orders_count)[1:-1]
    out.update({'page_title': "Анализ"})
    out.update({'data': amount_str})
    out.update({'managers': managers})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_manager_order_out.html', out)


# Менеджер сумма выставленных счетов
def analyze_manager_order_sum(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    managers = []
    orders_bill = []
    managers_ids = Roles.objects.filter(role=1, is_deleted=0)
    for managers_id in managers_ids:
        managers_orders = Orders.objects.filter(role_id=managers_id, is_deleted=0)
        bill = 0
        for managers_order in managers_orders:
            bill += managers_order.bill
        orders_bill.append(bill)
        managers.append(str(managers_id.surname + ' ' + managers_id.name))
    amount_str = str(orders_bill)[1:-1]
    out.update({'page_title': "Анализ"})
    out.update({'data': amount_str})
    out.update({'managers': managers})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_manager_order_sum.html', out)


# Менеджер сумма отгрузок
def analyze_manager_order_out_sum(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    managers = []
    orders_bill = []
    managers_ids = Roles.objects.filter(role=1, is_deleted=0)
    for managers_id in managers_ids:
        managers_orders = Orders.objects.filter(role_id=managers_id, is_deleted=0, order_status=2)
        bill = 0
        for managers_order in managers_orders:
            bill += managers_order.bill
        managers_orders = Orders.objects.filter(role_id=managers_id, is_deleted=0, order_status=3)
        for managers_order in managers_orders:
            bill += managers_order.bill
        orders_bill.append(bill)
        managers.append(str(managers_id.surname + ' ' + managers_id.name))
    amount_str = str(orders_bill)[1:-1]
    out.update({'page_title': "Анализ"})
    out.update({'data': amount_str})
    out.update({'managers': managers})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_manager_order_out_sum.html', out)