#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
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
    type_of_period = request.GET['period']
    type_of_graphic = request.GET.getlist('graphic[]')
    current_time = str(datetime.now())
    current_mounth = current_time[5:]
    current_mounth = current_mounth[:2]
    current_year = current_time[:4]
    analyzed_product = Products.objects.get(id=product_id)
    product_name = analyzed_product.title
    product_in_orders = Order_Product.objects.filter(product_id=product_id, is_deleted=0)
    period = []
    amount = []
    sum_of_pr = []
    all_sum = 0
    all_amount = 0
    if type_of_period == 'month':
        long_mounths = ['01', '03', '05', '07', '08', '10', '12']
        for i in range(28):
            period.append(i+1)
            amount.append(0)
            sum_of_pr.append(0)
        if current_mounth != '02':
            period.append(29)
            period.append(30)
            amount.append(0)
            amount.append(0)
            sum_of_pr.append(0)
            if current_mounth in long_mounths:
                period.append(31)
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
                if data_year == current_year and data_mounth == current_mounth:
                    amount[int(data_day) - 1] = int(amount[int(data_day) - 1] + pr.count_of_products)
                    sum_of_pr[int(data_day) - 1] = sum_of_pr[int(data_day) - 1] + pr.count_of_products * pr.price
                    all_sum = all_sum + pr.count_of_products * pr.price
                    all_amount = all_amount + pr.count_of_products
        # period_str = str(period)[1:-1]
        period_str = period
    elif type_of_period == 'year':
        for i in range(12):
            period.append(i+1)
            amount.append(0)
            sum_of_pr.append(0)
        for pr in product_in_orders:
            order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
            if order and order.bill_status == 2:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                if data_year == current_year:
                    amount[int(data_mounth) - 1] = int(amount[int(data_mounth) - 1] + pr.count_of_products)
                    sum_of_pr[int(data_mounth) - 1] = sum_of_pr[int(data_mounth) - 1] + pr.count_of_products * pr.price
                    all_sum = all_sum + pr.count_of_products * pr.price
                    all_amount = all_amount + pr.count_of_products
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
                           - int(first_data_mounth) + 2
        for i in range(amount_of_period):
            period.append(i+1)
            amount.append(0)
            sum_of_pr.append(0)
        for pr in product_in_orders:
            order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
            if order and order.bill_status == 2:
                data = str(order.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_year = data[:4]
                data_year_and_mounth = data[:7]
                current_year_and_mounth = current_year + '-' + current_mounth
                i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                amount[i] = int(amount[i] + pr.count_of_products)
                sum_of_pr[i] = int(sum_of_pr[i] + pr.count_of_products * pr.price)
                all_sum = all_sum + pr.count_of_products * pr.price
                all_amount = all_amount + pr.count_of_products
        period_str = []
        for i in range(amount_of_period):
            if ((i+int(first_data_mounth)-1) % 12) == 1:
                period_str.append('Январь')
            elif ((i+int(first_data_mounth)-1) % 12) == 2:
                period_str.append('Февраль')
            elif ((i+int(first_data_mounth)-1) % 12) == 3:
                period_str.append('Март')
            elif ((i+int(first_data_mounth)-1) % 12) == 4:
                period_str.append('Апрель')
            elif ((i+int(first_data_mounth)-1) % 12) == 5:
                period_str.append('Май')
            elif ((i+int(first_data_mounth)-1) % 12) == 6:
                period_str.append('Июнь')
            elif ((i+int(first_data_mounth)-1) % 12) == 7:
                period_str.append('Июль')
            elif ((i+int(first_data_mounth)-1) % 12) == 8:
                period_str.append('Август')
            elif ((i+int(first_data_mounth)-1) % 12) == 9:
                period_str.append('Сентябрь')
            elif ((i+int(first_data_mounth)-1) % 12) == 10:
                period_str.append('Октябрь')
            elif ((i+int(first_data_mounth)-1) % 12) == 11:
                period_str.append('Ноябрь')
            elif ((i+int(first_data_mounth)-1) % 12) == 0:
                period_str.append('Декабрь')
        amount = amount[::-1]
        sum_of_pr = sum_of_pr[::-1]
    amount_str = str(amount)[1:-1]
    sum_str = str(sum_of_pr)[1:-1]
    average_sum = all_sum / all_amount
    average_sum_right_format = right_money_format(average_sum)
    out.update({'page_title': "Анализ продаж продукта"})
    out.update({'select_period': period_str})
    if 'number' in type_of_graphic:
        out.update({'number_data': amount_str})
    if 'sum' in type_of_graphic:
        out.update({'sum_data': sum_str})
    out.update({'product_name': product_name})
    out.update({'period': type_of_period})
    out.update({'graphic': type_of_graphic})
    out.update({'average_sum_right_format': average_sum_right_format})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'view_analyzed_product.html', out)
