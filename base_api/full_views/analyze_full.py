#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_analyze_products(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
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
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    product_id = request.GET['id']
    type_of_period = request.GET['period']
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
        period_str.append("Январь")
        period_str.append("Февраль")
        period_str.append("Март")
        period_str.append("Апрель")
        period_str.append("Май")
        period_str.append("Июнь")
        period_str.append("Июль")
        period_str.append("Август")
        period_str.append("Сентябрь")
        period_str.append("Октябрь")
        period_str.append("Ноябрь")
        period_str.append("Декабрь")
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
            if ((i+1+int(first_data_mounth)) % 12) == 1:
                period_str.append("Январь")
            elif ((i+1+int(first_data_mounth)) % 12) == 2:
                period_str.append("Февраль")
            elif ((i+1+int(first_data_mounth)) % 12) == 3:
                period_str.append("Март")
            elif ((i+1+int(first_data_mounth)) % 12) == 4:
                period_str.append("Апрель")
            elif ((i+1+int(first_data_mounth)) % 12) == 5:
                period_str.append("Май")
            elif ((i+1+int(first_data_mounth)) % 12) == 6:
                period_str.append("Июнь")
            elif ((i+1+int(first_data_mounth)) % 12) == 7:
                period_str.append("Июль")
            elif ((i+1+int(first_data_mounth)) % 12) == 8:
                period_str.append("Август")
            elif ((i+1+int(first_data_mounth)) % 12) == 9:
                period_str.append("Сентябрь")
            elif ((i+1+int(first_data_mounth)) % 12) == 10:
                period_str.append("Октябрь")
            elif ((i+1+int(first_data_mounth)) % 12) == 11:
                period_str.append("Ноябрь")
            elif ((i+1+int(first_data_mounth)) % 12) == 0:
                period_str.append("Декабрь")
        print(period_str)
    amount_str = str(amount)[1:-1]
    print(period)
    out.update({'page_title': "Анализ продаж продукта"})
    out.update({'select_period': period_str})
    out.update({'data': amount_str})
    out.update({'product_name': product_name})
    out.update({'period': type_of_period})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'view_analyzed_product.html', out)
