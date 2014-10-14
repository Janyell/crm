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
    managers = Roles.objects.filter(role=1, is_deleted=0)
    for manager in managers:
        manager.full_name = manager.surname + ' ' + manager.name + ' ' + manager.patronymic
        if manager.full_name == '  ':
            manager.full_name = User.objects.get(id=manager.id).username
    current_time = str(datetime.now())
    current_mounth = current_time[5:]
    current_mounth = current_mounth[:2]
    current_year = current_time[:4]
    if 'graphic' and 'id' and 'period' in request.GET:
        type_of_period = request.GET['period']
        type_of_graphic = request.GET['graphic']
        manager_id = request.GET['id']
        manager = Roles.objects.get(id=manager_id)
        period = []
        orders_count = []
        shipped_orders_count = []
        if type_of_period == 'month':
            long_mounths = ['01', '03', '05', '07', '08', '10', '12']
            for i in range(28):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
            if current_mounth != 02:
                period.append(29)
                period.append(30)
                orders_count.append(0)
                orders_count.append(0)
                shipped_orders_count.append(0)
                shipped_orders_count.append(0)
                if current_mounth in long_mounths:
                    period.append(31)
                    orders_count.append(0)
                    shipped_orders_count.append(0)
            orders = Orders.objects.filter(role_id=manager.id, is_deleted=0)
            shipped_orders1 = Orders.objects.filter(role_id=manager.id, is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(role_id=manager.id, is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    if type_of_graphic == 'number':
                        orders_count[int(data_day) - 1] += 1
                    if type_of_graphic == 'sum':
                        if order.bill != None:
                            orders_count[int(data_day) - 1] += int(order.bill)
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    if type_of_graphic == 'number':
                        shipped_orders_count[int(data_day) - 1] += 1
                    if type_of_graphic == 'sum':
                        if order.bill != None:
                            shipped_orders_count[int(data_day) - 1] += int(order.bill)
            period_str = period
        elif type_of_period == 'year':
            for i in range(12):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
            orders = Orders.objects.filter(role_id=manager.id, is_deleted=0)
            shipped_orders1 = Orders.objects.filter(role_id=manager.id, is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(role_id=manager.id, is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    if type_of_graphic == 'number':
                        orders_count[int(data_mounth) - 1] += 1
                    if type_of_graphic == 'sum':
                        if order.bill != None:
                            orders_count[int(data_mounth) - 1] += int(order.bill)
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    if type_of_graphic == 'number':
                        shipped_orders_count[int(data_mounth) - 1] += 1
                    if type_of_graphic == 'sum':
                        if order.bill != None:
                            shipped_orders_count[int(data_mounth) - 1] += int(order.bill)
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
            user = User.objects.get(id=manager.user_ptr_id)
            all_date_of_orders = user.date_joined
            first_data = str(all_date_of_orders)
            first_data_mounth = first_data[5:]
            first_data_mounth = first_data_mounth[:2]
            first_data_year = first_data[:4]
            amount_of_period = (int(current_year) - int(first_data_year)) * 12 + int(current_mounth)\
                               - int(first_data_mounth) + 1
            for i in range(amount_of_period):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
            orders = Orders.objects.filter(role_id=manager.id, is_deleted=0)
            shipped_orders1 = Orders.objects.filter(role_id=manager.id, is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(role_id=manager.id, is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                if type_of_graphic == 'number':
                    orders_count[i] += 1
                if type_of_graphic == 'sum':
                    if order.bill != None:
                        orders_count[i] += int(order.bill)
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                if type_of_graphic == 'number':
                    shipped_orders_count[i] += 1
                if type_of_graphic == 'sum':
                    if order.bill != None:
                        shipped_orders_count[i] += int(order.bill)
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
        orders_count_str = str(orders_count)[1:-1]
        shipped_orders_count_str = str(shipped_orders_count)[1:-1]
        out.update({'select_period': period_str})
        out.update({'bill_data': orders_count_str})
        out.update({'shipped_data': shipped_orders_count_str})
        out.update({'period': type_of_period})
    out.update({'page_title': "Анализ работы менеджеров"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'managers': managers})
    return render(request, 'analyze_managers.html', out)


def analyze_total_sales(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    current_time = str(datetime.now())
    current_mounth = current_time[5:]
    current_mounth = current_mounth[:2]
    current_year = current_time[:4]
    if 'period' in request.GET:
        type_of_period = request.GET['period']
        period = []
        orders_count = []
        shipped_orders_count = []
        bill_orders_count = []
        if type_of_period == 'month':
            long_mounths = ['01', '03', '05', '07', '08', '10', '12']
            for i in range(28):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
            if current_mounth != 02:
                period.append(29)
                period.append(30)
                orders_count.append(0)
                orders_count.append(0)
                shipped_orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
                bill_orders_count.append(0)
                if current_mounth in long_mounths:
                    period.append(31)
                    orders_count.append(0)
                    shipped_orders_count.append(0)
                    bill_orders_count.append(0)
            orders = Orders.objects.filter(is_deleted=0)
            shipped_orders1 = Orders.objects.filter(is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            bill_orders = Orders.objects.filter(is_deleted=0, bill_status=0)
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    if order.bill != None:
                            orders_count[int(data_day) - 1] += int(order.bill)
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    if order.bill != None:
                            shipped_orders_count[int(data_day) - 1] += int(order.bill)
            for order in bill_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    if order.bill != None:
                            bill_orders_count[int(data_day) - 1] += int(order.bill)
            period_str = period
        elif type_of_period == 'year':
            for i in range(12):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
            orders = Orders.objects.filter(is_deleted=0)
            shipped_orders1 = Orders.objects.filter(is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            bill_orders = Orders.objects.filter(is_deleted=0, bill_status=0)
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    if order.bill != None:
                            orders_count[int(data_mounth) - 1] += int(order.bill)
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    if order.bill != None:
                            shipped_orders_count[int(data_mounth) - 1] += int(order.bill)
            for order in bill_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    if order.bill != None:
                            bill_orders_count[int(data_mounth) - 1] += int(order.bill)
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
            all_date_of_orders = Order_Product.objects.filter(is_deleted=0).order_by('order_date')
            first_data = str(all_date_of_orders[0].order_date)
            first_data_mounth = first_data[5:]
            first_data_mounth = first_data_mounth[:2]
            first_data_year = first_data[:4]
            amount_of_period = (int(current_year) - int(first_data_year)) * 12 + int(current_mounth)\
                               - int(first_data_mounth) + 1
            for i in range(amount_of_period):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
            orders = Orders.objects.filter(is_deleted=0)
            shipped_orders1 = Orders.objects.filter(is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            bill_orders = Orders.objects.filter(is_deleted=0, bill_status=0)
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                if order.bill != None:
                        orders_count[i] += int(order.bill)
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                if order.bill != None:
                        shipped_orders_count[i] += int(order.bill)
            for order in bill_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                if order.bill != None:
                        bill_orders_count[i] += int(order.bill)
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
        print(orders_count)
        orders_count_str = str(orders_count)[1:-1]
        shipped_orders_count_str = str(shipped_orders_count)[1:-1]
        bill_orders_count_str = str(bill_orders_count)[1:-1]
        out.update({'select_period': period_str})
        out.update({'call_data': orders_count_str})
        out.update({'shipped_data': shipped_orders_count_str})
        out.update({'bill_data': bill_orders_count_str})
        out.update({'period': type_of_period})
    out.update({'page_title': "Общая воронка продаж"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_total_sales.html', out)


def analyze_sales_by_managers(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    current_time = str(datetime.now())
    current_mounth = current_time[5:]
    current_mounth = current_mounth[:2]
    current_year = current_time[:4]
    if 'period' in request.GET:
        type_of_period = request.GET['period']
        period = []
        orders_count = []
        shipped_orders_count = []
        bill_orders_count = []
        if type_of_period == 'month':
            long_mounths = ['01', '03', '05', '07', '08', '10', '12']
            for i in range(28):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
            if current_mounth != 02:
                period.append(29)
                period.append(30)
                orders_count.append(0)
                orders_count.append(0)
                shipped_orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
                bill_orders_count.append(0)
                if current_mounth in long_mounths:
                    period.append(31)
                    orders_count.append(0)
                    shipped_orders_count.append(0)
                    bill_orders_count.append(0)
            orders = Orders.objects.filter(is_deleted=0)
            shipped_orders1 = Orders.objects.filter(is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            bill_orders = Orders.objects.filter(is_deleted=0, bill_status=0)
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    orders_count[int(data_day) - 1] += 1
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    shipped_orders_count[int(data_day) - 1] += 1
            for order in bill_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                if data_year == current_year and data_mounth == current_mounth:
                    bill_orders_count[int(data_day) - 1] += 1
            period_str = period
        elif type_of_period == 'year':
            for i in range(12):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
            orders = Orders.objects.filter(is_deleted=0)
            shipped_orders1 = Orders.objects.filter(is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            bill_orders = Orders.objects.filter(is_deleted=0, bill_status=0)
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    orders_count[int(data_mounth) - 1] += 1
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    shipped_orders_count[int(data_mounth) - 1] += 1
            for order in bill_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    bill_orders_count[int(data_mounth) - 1] += 1
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
            all_date_of_orders = Order_Product.objects.filter(is_deleted=0).order_by('order_date')
            first_data = str(all_date_of_orders[0].order_date)
            first_data_mounth = first_data[5:]
            first_data_mounth = first_data_mounth[:2]
            first_data_year = first_data[:4]
            amount_of_period = (int(current_year) - int(first_data_year)) * 12 + int(current_mounth)\
                               - int(first_data_mounth) + 1
            for i in range(amount_of_period):
                period.append(i+1)
                orders_count.append(0)
                shipped_orders_count.append(0)
                bill_orders_count.append(0)
            orders = Orders.objects.filter(is_deleted=0)
            shipped_orders1 = Orders.objects.filter(is_deleted=0, order_status=2)
            shipped_orders2 = Orders.objects.filter(is_deleted=0, order_status=3)
            shipped_orders = shipped_orders1 | shipped_orders2
            bill_orders = Orders.objects.filter(is_deleted=0, bill_status=0)
            for order in orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                orders_count[i] += 1
            for order in shipped_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                shipped_orders_count[i] += 1
            for order in bill_orders:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                bill_orders_count[i] += 1
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
        orders_count_str = str(orders_count)[1:-1]
        shipped_orders_count_str = str(shipped_orders_count)[1:-1]
        bill_orders_count_str = str(bill_orders_count)[1:-1]
        out.update({'select_period': period_str})
        out.update({'call_data': orders_count_str})
        out.update({'shipped_data': shipped_orders_count_str})
        out.update({'bill_data': bill_orders_count_str})
        out.update({'period': type_of_period})
    out.update({'page_title': "Воронка продаж по менеджерам"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_sales_by_managers.html', out)


def analyze_period(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request,'analyze_period.html', out)
