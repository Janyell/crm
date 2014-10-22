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
from base_api.full_views.analyze_products import *
from base_api.full_views.analyze_managers import *
from base_api.full_views.analyze_sales_by_managers import *
from base_api.full_views.analyze_total_sales import *
from base_api.full_views.analyze_period import *
from base_api.full_views.product_views import *


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
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
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
                if Roles.objects.get(id=request.user.id).role != 0:
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
        if Roles.objects.get(id=request.user.id).role != 0:
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
    out.update({'user_role': user_role})
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


def analyze_sale(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_sale.html', out)


def analyze_managers(request):
    return full_analyze_managers(request)


def analyze_total_sales(request):
    return full_analyze_total_sales(request)


def analyze_sales_by_managers(request):
    return full_analyze_sales_by_managers(request)


def analyze_period(request):
    return full_analyze_period(request)


def give_order_status(request):
    order_unic = request.GET['id']
    order_status = Orders.objects.get(unique_number=order_unic).order_status
    if order_status == 0:
        order_status_str = 'В производстве'
    if order_status == 1:
        order_status_str = 'Нужна доплата'
    if order_status == 2:
        order_status_str = 'Отгружен'
    if order_status == 3:
        order_status_str = 'Готов'
    out = {}
    out.update({'page_title': order_status_str})
    return render(request, 'page_not_found.html', out)


def get_products(request):
    return full_get_products(request)


def delete_product(request):
    return full_delete_product(request)


def add_product(request):
    return full_add_product(request)
