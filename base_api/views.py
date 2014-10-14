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
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    type_of_period = request.GET['period']
    type_of_graphic = request.GET['graphic']
    managers = Roles.objects.filter(role=1, is_deleted=0)
    current_time = str(datetime.now())
    current_mounth = current_time[5:]
    current_mounth = current_mounth[:2]
    current_year = current_time[:4]
    analyzed_product = Products.objects.get(id=product_id)
    product_name = analyzed_product.title
    product_in_orders = Order_Product.objects.filter(product_id=product_id, is_deleted=0)
    period = []
    amount = []
    if type_of_period == 'month':
        long_mounths = ['01', '03', '05', '07', '08', '10', '12']
        for i in range(28):
            period.append(i+1)
            amount.append(0)
        if current_mounth != 02:
            period.append(29)
            period.append(30)
            amount.append(0)
            amount.append(0)
            if current_mounth in long_mounths:
                period.append(31)
                amount.append(0)
        for pr in product_in_orders:
            order = Orders.objects.get(id=pr.order_id)
            data = str(order.order_date)
            data_mounth = data[5:]
            data_mounth = data_mounth[:2]
            data_day = data[8:]
            data_day = data_day[:2]
            data_year = data[:4]
            if data_year == current_year and data_mounth == current_mounth:
                amount[int(data_day) - 1] = int(amount[int(data_day) - 1] + pr.count_of_products)
        # period_str = str(period)[1:-1]
        period_str = period
    elif type_of_period == 'year':
        for i in range(12):
            period.append(i+1)
            amount.append(0)
        for pr in product_in_orders:
            order = Orders.objects.get(id=pr.order_id)
            data = str(order.order_date)
            data_mounth = data[5:]
            data_mounth = data_mounth[:2]
            data_year = data[:4]
            if data_year == current_year:
                amount[int(data_mounth) - 1] = int(amount[int(data_mounth) - 1] + pr.count_of_products)
        period_str = []
        period_str.append('Январь')
        period_str.append('Февраль')
        period_str.append('Март')
        period_str.append('Апрель')
        period_str.append('Май')
        period_str.append('Июнь')
        period_str.append('Июль')
        period_str.append('Август')
        period_str.append('Сентябрь')
        period_str.append('Октябрь')
        period_str.append('Ноябрь')
        period_str.append('Декабрь')
    elif type_of_period == 'all':
        all_date_of_orders = Order_Product.objects.filter(product_id=product_id, is_deleted=0).order_by('order_date')
        first_data = str(all_date_of_orders[0].order_date)
        first_data_mounth = first_data[5:]
        first_data_mounth = first_data_mounth[:2]
        first_data_year = first_data[:4]
        amount_of_period = (int(current_year) - int(first_data_year)) * 12 + int(current_mounth)\
                           - int(first_data_mounth) + 1
        for i in range(amount_of_period):
            period.append(i+1)
            amount.append(0)
        for pr in product_in_orders:
            order = Orders.objects.get(id=pr.order_id)
            data = str(order.order_date)
            data_mounth = data[5:]
            data_mounth = data_mounth[:2]
            data_year = data[:4]
            data_year_and_mounth = data[:7]
            current_year_and_mounth = current_year + '-' + current_mounth
            i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
            amount[i] = int(amount[i] + pr.count_of_products)
        period_str = []
        for i in range(amount_of_period):
            if ((i+int(first_data_mounth)) % 12) == 1:
                period_str.append('Январь')
            elif ((i+int(first_data_mounth)) % 12) == 2:
                period_str.append('Февраль')
            elif ((i+int(first_data_mounth)) % 12) == 3:
                period_str.append('Март')
            elif ((i+int(first_data_mounth)) % 12) == 4:
                period_str.append('Апрель')
            elif ((i+int(first_data_mounth)) % 12) == 5:
                period_str.append('Май')
            elif ((i+int(first_data_mounth)) % 12) == 6:
                period_str.append('Июнь')
            elif ((i+int(first_data_mounth)) % 12) == 7:
                period_str.append('Июль')
            elif ((i+int(first_data_mounth)) % 12) == 8:
                period_str.append('Август')
            elif ((i+int(first_data_mounth)) % 12) == 9:
                period_str.append('Сентябрь')
            elif ((i+int(first_data_mounth)) % 12) == 10:
                period_str.append('Октябрь')
            elif ((i+int(first_data_mounth)) % 12) == 11:
                period_str.append('Ноябрь')
            elif ((i+int(first_data_mounth)) % 12) == 0:
                period_str.append('Декабрь')
    amount_str = str(amount)[1:-1]
    out.update({'page_title': "Анализ продаж продукта"})
    out.update({'select_period': period_str})
    out.update({'data': amount_str})
    out.update({'product_name': product_name})
    out.update({'period': type_of_period})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'managers': managers})
    return render(request, 'analyze_managers.html')


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
    return render(request, 'analyze_manager_order_out_sum.html', out)    out = {}


def analyze_sales_by_managers(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_sales_by_managers.html', out)


def analyze_total_sales_by_managers(request):
    return render_to_response('analyze_total_sales_by_managers.html')


def analyze_total_sales(request):
    return render_to_response('analyze_total_sales.html')