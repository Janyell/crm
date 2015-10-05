#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db.models import Q, Sum, Count
from django.shortcuts import render
from base_api.models import *
from base_api.form import *
from django.http import *


def full_analyze_city(request):
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
            out.update({'page_title': 'Анализ продаж по городам за период'})
            return render(request, 'analyze_city_period.html.html', out)
        if count_for == 'shipped':
            orders = Orders.objects.filter(is_deleted=0)\
                                            .filter(order_date__gte=since_date)\
                                            .filter(order_date__lte=until_date)\
                                            .filter(Q(order_status=-1) | Q(order_status=2))\
                                            .values("city__name")\
                                            .annotate(number=Count('id'))\
                                            .order_by()
        elif count_for == 'made-claims':
            orders = Orders.objects.filter(is_deleted=0)\
                                            .filter(order_date__gte=since_date)\
                                            .filter(order_date__lte=until_date)\
                                            .filter(is_claim=1)\
                                            .values("city__name")\
                                            .annotate(number=Count('id'))\
                                            .order_by()
        out.update({'analysed_data': orders})
        out.update({'since_date': since_date})
        out.update({'until_date': until_date})
        if not orders.exists():
            out.update({'error': 'В данный период заказов не поступало'})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': 'Анализ продаж по городам за период'})
    return render(request, 'analyze_city_period.html', out)