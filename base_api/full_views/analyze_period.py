#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db.models import Sum, Count, Q
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
        count_for = request.GET['count']
        if since_date == '' or until_date == '':
            out.update({'since_date': since_date})
            out.update({'until_date': until_date})
            out.update({'error': 'Укажите период полностью!'})
            user_role = Roles.objects.get(id=request.user.id).role
            out.update({'user_role': user_role})
            out.update({'page_title': 'Анализ продаж продуктов за период'})
            return render(request, 'analyze_period.html', out)
        if count_for == 'shipped':
            orders = Order_Product.objects.filter(is_deleted=0)\
                                            .filter(order__order_date__gte=since_date)\
                                            .filter(order__order_date__lte=until_date)\
                                            .filter(Q(order__order_status=-1) | Q(order__order_status=2))\
                                            .values("product__title")\
                                            .annotate(number=Sum('count_of_products'))\
                                            .order_by()
        elif count_for == 'made-claims':
            orders = Order_Product.objects.filter(is_deleted=0)\
                                            .filter(order__order_date__gte=since_date)\
                                            .filter(order__order_date__lte=until_date)\
                                            .filter(order__is_claim=1)\
                                            .values("product__title")\
                                            .annotate(number=Sum('count_of_products'))\
                                            .order_by()
        out.update({'analysed_data': orders})
        out.update({'since_date': since_date})
        out.update({'until_date': until_date})
        if not orders.exists():
            out.update({'error': 'В данный период заказов не поступало'})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': 'Анализ продаж продуктов за период'})
    return render(request, 'analyze_period.html', out)


def full_analyze_period_product_groups(request):
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
        count_for = request.GET['count']
        if since_date == '' or until_date == '':
            out.update({'since_date': since_date})
            out.update({'until_date': until_date})
            out.update({'error': 'Укажите период полностью!'})
            user_role = Roles.objects.get(id=request.user.id).role
            out.update({'user_role': user_role})
            out.update({'page_title': 'Анализ продаж групп товаров за период'})
            return render(request, 'analyze_period.html', out)
        if count_for == 'shipped':
            orders = Order_Product.objects.filter(is_deleted=0)\
                                            .filter(order__order_date__gte=since_date)\
                                            .filter(order__order_date__lte=until_date)\
                                            .filter(Q(order__order_status=-1) | Q(order__order_status=2))\
                                            .values("product__group")\
                                            .annotate(number=Sum('count_of_products'))\
                                            .order_by()
        elif count_for == 'made-claims':
            orders = Order_Product.objects.filter(is_deleted=0)\
                                            .filter(order__order_date__gte=since_date)\
                                            .filter(order__order_date__lte=until_date)\
                                            .filter(order__is_claim=1)\
                                            .values("product__group")\
                                            .annotate(number=Sum('count_of_products'))\
                                            .order_by()
        out.update({'analysed_data': orders})
        out.update({'since_date': since_date})
        out.update({'until_date': until_date})
        if not orders.exists():
            out.update({'error': 'В данный период заказов не поступало'})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': 'Анализ продаж групп товаров за период'})
    return render(request, 'analyze_period.html', out)