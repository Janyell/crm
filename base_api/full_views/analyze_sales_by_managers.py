#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_analyze_sales_by_managers(request):
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
                               - int(first_data_mounth) + 2
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
            orders_count = orders_count[::-1]
            shipped_orders_count = shipped_orders_count[::-1]
            bill_orders_count = bill_orders_count[::-1]
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