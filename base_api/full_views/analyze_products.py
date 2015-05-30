#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime, timedelta
from base_api.full_views.order_views import right_money_format
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_analyze_products(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    products = Products.objects.filter(is_deleted=0)
    out.update({'products': products})
    out.update({'page_title': "Анализ продаж продукта"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyze_products.html', out)


def full_view_analyzed_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    product_id = request.GET['id']
    analyzed_product = Products.objects.get(id=product_id)
    product_name = analyzed_product.title
    if 'period' in request.POST:
        type_of_period = request.POST['period']
        start_period = type_of_period[:10]
        end_period = type_of_period[-10:]
    else:
        type_of_period = None
    if 'graphic[]' in request.POST:
        type_of_graphic = request.POST.getlist('graphic[]')
    else:
        type_of_graphic = []
    if request.method == 'POST':
        current_time = str(end_period)
        current_day = current_time[-2:]
        current_mounth = current_time[5:]
        current_mounth = current_mounth[:2]
        current_year = current_time[:4]
        product_in_orders = Order_Product.objects.filter(product_id=product_id, is_deleted=0)
        period = []
        period_str = ''
        amount = []
        sum_of_pr = []
        all_sum = 0
        all_amount = 0
        # по часам
        if start_period == end_period:
            for i in range(24):
                period.append(i+1)
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
                if order and order.bill_status == 2:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_day = data[8:]
                    data_day = data_day[:2]
                    data_year = data[:4]
                    data_hour = data[:13]
                    data_hour = data_hour[-2:]
                    if data_year == current_year and data_mounth == current_mounth and data_day == current_day:
                        amount[int(data_hour) - 1] = int(amount[int(data_hour) - 1] + pr.count_of_products)
                        sum_of_pr[int(data_hour) - 1] = sum_of_pr[int(data_hour) - 1] + pr.count_of_products * pr.price
                        all_sum = all_sum + pr.count_of_products * pr.price
                        all_amount = all_amount + pr.count_of_products
            period_str = period

        # по дням
        start_period_time = datetime.strptime(start_period, "%Y-%m-%d").date()
        end_period_time = datetime.strptime(end_period, "%Y-%m-%d").date()
        if (end_period_time - start_period_time).days < 61:
            for i in range((end_period_time - start_period_time).days + 1):
                period.append(start_period_time + timedelta(days=i))
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
                if order and order.bill_status == 2:
                    data = order.order_date.date()
                    if start_period_time < data and data < end_period_time:
                        amount[(data - start_period_time).days] = int(amount[(data - start_period_time).days] + pr.count_of_products)
                        sum_of_pr[(data - start_period_time).days] = sum_of_pr[(data - start_period_time).days] + pr.count_of_products * pr.price
                        all_sum = all_sum + pr.count_of_products * pr.price
                        all_amount = all_amount + pr.count_of_products
            period_str = period

        # по месяцам
        start_period_time = datetime.strptime(start_period, "%Y-%m-%d").date()
        end_period_time = datetime.strptime(end_period, "%Y-%m-%d").date()
        for i in range((end_period_time - start_period_time).mo + 1):
            period.append(start_period_time + timedelta(days=i))
            amount.append(0)
            sum_of_pr.append(0)
        for pr in product_in_orders:
            order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
            if order and order.bill_status == 2:
                data = order.order_date.date()
                if start_period_time < data and data < end_period_time:
                    amount[(data - start_period_time).days] = int(amount[(data - start_period_time).days] + pr.count_of_products)
                    sum_of_pr[(data - start_period_time).days] = sum_of_pr[(data - start_period_time).days] + pr.count_of_products * pr.price
                    all_sum = all_sum + pr.count_of_products * pr.price
                    all_amount = all_amount + pr.count_of_products
        period_str = period

        amount_str = str(amount)[1:-1]
        sum_str = str(sum_of_pr)[1:-1]
        if all_amount == 0:
            average_sum = 0
        else:
            average_sum = all_sum / all_amount
        average_sum_right_format = right_money_format(average_sum)
        out.update({'select_period': period_str})
        if 'number' in type_of_graphic:
            out.update({'number_data': amount_str})
        if 'sum' in type_of_graphic:
            out.update({'sum_data': sum_str})
        out.update({'period': type_of_period})
        out.update({'graphic': type_of_graphic})
        out.update({'average_sum_right_format': average_sum_right_format})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'page_title': "Анализ продаж продукта"})
    out.update({'product_name': product_name})
    out.update({'user_role': user_role})
    return render(request, 'view_analyzed_product.html', out)


def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31, 29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)
