#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.full_views.attach import my_view_up
from base_api.models import *
from base_api.form import *
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
from base_api.full_views.claim_views import *


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
        out.update({'page_title': "Аналитика"})
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
    try:
        user_role = Roles.objects.get(id=request.user.id).role
        out = {'user_role': user_role}
        out.update({'page_title': "Страница не найдена"})
        return render(request, 'page_not_found.html', out)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/login/")


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


def analyze_managers(request):
    return full_analyze_managers(request)


def analyze_total_sales(request):
    return full_analyze_total_sales(request)


def analyze_sales_by_managers(request):
    return full_analyze_sales_by_managers(request)


def analyze_period(request):
    return full_analyze_period(request)


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % ('func', data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


@json_response
def give_order_status(request):
    order_unic = request.GET['id']
    result = {}
    try:
        order = Orders.objects.get(unique_number=order_unic)
        result['order_status'] = order.order_status
        result['order_date'] = str(order.order_date)
        result['payment_date'] = str(order.payment_date)
        result['bill_status'] = order.bill_status
        result['ready_date'] = str(order.ready_date)
    except ObjectDoesNotExist:
        result['error'] = u'order_is_not_exist'
    return result


def get_products(request):
    return full_get_products(request)


def delete_product(request):
    return full_delete_product(request)


def edit_order_for_other_managers(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        if 'pk' in request.POST:
            pk = request.POST['pk']
            comment = request.POST['comment']
            new_order = Orders.objects.get(id=pk, is_deleted=0)
            is_comment_my = False
            if new_order.role_id == request.user.id:
                is_comment_my = True
            new_order.is_comment_my = is_comment_my
            new_order.comment = comment
            new_order.save(force_update=True)
            return HttpResponseRedirect('/orders/')
        else:
            return HttpResponseRedirect('/orders')
    else:
        if 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0)
            form = OrdersForm({'comment': order.comment})
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заказа"})
        else:
            return HttpResponseRedirect('/orders/')
    return render(request, 'edit_order_for_other_managers.html', out)


def edit_claim_for_other_managers(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        if 'pk' in request.POST:
            pk = request.POST['pk']
            comment = request.POST['comment']
            new_order = Orders.objects.get(id=pk, is_deleted=0, is_claim=1)
            new_order.comment = comment
            is_comment_my = False
            if new_order.role_id == request.user.id:
                is_comment_my = True
            new_order.is_comment_my = is_comment_my
            new_order.save(force_update=True)
            return HttpResponseRedirect('/claims/')
        else:
            return HttpResponseRedirect('/claims')
    else:
        if 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0, is_claim=1)
            form = OrdersForm({'comment': order.comment})
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заявки"})
        else:
            return HttpResponseRedirect('/claims/')
    return render(request, 'edit_order_for_other_managers.html', out)


def get_claims(request):
    return full_get_claims(request)


def add_edit_claim(request):
    return full_add_edit_claim(request)


def delete_claim(request):
    return full_delete_claim(request)


def delete_from_archive(request):
    return full_delete_from_archive(request)


def my_view(request):
    return my_view_up(request)
