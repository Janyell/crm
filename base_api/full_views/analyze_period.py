#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_analyze_period(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if 'since-date' and 'until-date' in request.GET:
        since_date = request.GET['since-date']
        until_date = request.GET['until-date']
        orders = Order_Product.objects.filter(order_date__gte=since_date).filter(order_date__lte=until_date).filter(is_deleted=0)
        data_object = []
        products = []
        data = []
        i = 0
        for order in orders:
            order_from_table_order = Orders.objects.get(id=order.order_id)
            is_sell = False
            if order_from_table_order.order_status == 1 or order_from_table_order.order_status == 2:
                is_sell = True
            if is_sell and order.product_id not in products:
                products.append(order.product_id)
                data.append(data_object)
                data[i] = Products.objects.get(id=order.product_id)
                data[i].number = 0
                i += 1
        i = 0
        for product in products:
            for order in orders:
                order_from_table_order = Orders.objects.get(id=order.order_id)
                is_sell = False
                if order_from_table_order.is_deleted == 0 and (order_from_table_order.order_status == 1 or order_from_table_order.order_status == 2):
                    is_sell = True
                if is_sell and order.product_id == product:
                    data[i].number += order.count_of_products
            i += 1
        out.update({'analysed_data': data})
        out.update({'since_date': since_date})
        out.update({'until_date': until_date})
        if i == 0:
            out.update({'error': 'В данный период заказов не поступало'})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': 'Анализ продаж продуктов за период'})
    return render(request, 'analyze_period.html', out)