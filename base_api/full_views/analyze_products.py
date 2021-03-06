#!/usr/bin/python
# -*- coding: utf-8 -*-
from calendar import monthrange
from django.shortcuts import render, render_to_response
from datetime import datetime, timedelta
from base_api.full_views.order_views import right_money_format
from base_api.form import *
from django.http import *
from django.db.models import Q


def full_analyze_products(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0 and user_role != 3:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    products = Products.objects.filter(is_deleted=0)
    out.update({'products': products})
    out.update({'page_title': "Анализ продаж продукта"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyst/analyze_products.html', out)


def full_view_analyzed_product(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0 and user_role != 3:
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
        i = request.POST['i']
        out.update({'i': i})
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
        start_period_time = datetime.strptime(start_period, "%Y-%m-%d").date()
        end_period_time = datetime.strptime(end_period, "%Y-%m-%d").date()
        # по часам
        if start_period == end_period:
            for i in range(24):
                period.append(str(i+1) + ':00')
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
                if order and order.order_status == -1:
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
                        sum_of_pr[int(data_hour) - 1] = int(sum_of_pr[int(data_hour) - 1] + pr.count_of_products * pr.price)
                        all_sum = all_sum + pr.count_of_products * pr.price
                        all_amount = all_amount + pr.count_of_products
            period_str = period

        # по дням
        elif (end_period_time - start_period_time).days < 61:
            for i in range((end_period_time - start_period_time).days + 1):
                period.append(start_period_time + timedelta(days=i))
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
                if order and order.order_status == -1:
                    data = order.order_date.date()
                    if start_period_time <= data and data <= end_period_time:
                        amount[(data - start_period_time).days] = int(amount[(data - start_period_time).days] + pr.count_of_products)
                        sum_of_pr[(data - start_period_time).days] = int(sum_of_pr[(data - start_period_time).days] + pr.count_of_products * pr.price)
                        all_sum = all_sum + pr.count_of_products * pr.price
                        all_amount = all_amount + pr.count_of_products
            period_str = period
        else:
            end_year = str(end_period_time)[:4]
            start_year = str(start_period_time)[:4]
            end_month = str(end_period_time)[:7][-2:]
            start_month = str(start_period_time)[:7][-2:]
            month_count = (int(end_year) - int(start_year))*12 + int(end_month) - int(start_month) + 1
            for i in range(month_count):
                period.append(str(month_delta(start_period_time, i))[:-3])
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                order = Orders.objects.filter(id=pr.order_id, is_deleted=0).first()
                if order and order.order_status == -1:
                    data = order.order_date.date()
                    now_year = str(data)[:4]
                    now_month = str(data)[:7][-2:]
                    if start_period_time <= data and data <= end_period_time:
                        count = (int(now_year) - int(start_year))*12 + int(now_month) - int(start_month)
                        amount[count] = int(amount[count] + pr.count_of_products)
                        sum_of_pr[count] = int(sum_of_pr[count] + pr.count_of_products * pr.price)
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
    return render(request, 'analyst/view_analyzed_product.html', out)


def full_analyze_products_groups(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0 and user_role != 3:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    product_groups = ProductGroups.objects.filter(is_deleted=0)
    out.update({'product_groups': product_groups})
    out.update({'page_title': "Анализ продаж групп продуктов"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    return render(request, 'analyst/analyze_product_groups.html', out)


def full_view_analyzed_product_groups(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0 and user_role != 3:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    product_group_id = request.GET['id']
    analyzed_product_group = ProductGroups.objects.get(id=product_group_id)
    product_group_name = analyzed_product_group.title
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
        i = request.POST['i']
        out.update({'i': i})
        current_time = str(end_period)
        current_day = current_time[-2:]
        current_mounth = current_time[5:]
        current_mounth = current_mounth[:2]
        current_year = current_time[:4]
        start_period_time = datetime.strptime(start_period, "%Y-%m-%d").date()
        end_period_time = datetime.strptime(end_period, "%Y-%m-%d").date()
        product_in_orders = Order_Product.objects.filter(product__group__id=product_group_id, is_deleted=0)\
                                                 .filter(order__order_date__gte=start_period_time)\
                                                 .filter(order__order_date__lte=end_period_time)\
                                                 .filter(Q(order__order_status=-1) | Q(order__order_status=2))\
                                                 .filter(Q(order__is_deleted=0))
        period = []
        period_str = ''
        amount = []
        sum_of_pr = []
        all_sum = 0
        all_amount = 0
        # по часам
        if start_period == end_period:
            for i in range(24):
                period.append(str(i+1) + ':00')
                amount.append(0)
                sum_of_pr.append(0)
            end_period_time = (datetime.strptime(start_period, "%Y-%m-%d") + timedelta(days=1)).date()
            product_in_orders = Order_Product.objects.filter(product__group__id=product_group_id, is_deleted=0)\
                                         .filter(order__order_date__gte=start_period_time)\
                                         .filter(order__order_date__lte=end_period_time)\
                                         .filter(Q(order__order_status=-1) | Q(order__order_status=2))\
                                         .filter(Q(order__is_deleted=0))
            for pr in product_in_orders:
                data = str(pr.order_date)
                data_mounth = data[5:]
                data_mounth = data_mounth[:2]
                data_day = data[8:]
                data_day = data_day[:2]
                data_year = data[:4]
                data_hour = data[:13]
                data_hour = data_hour[-2:]
                # if data_year == current_year and data_mounth == current_mounth and data_day == current_day:
                amount[int(data_hour) - 1] = int(amount[int(data_hour) - 1] + pr.count_of_products)
                sum_of_pr[int(data_hour) - 1] = int(sum_of_pr[int(data_hour) - 1] + pr.count_of_products * pr.price)
                all_sum = all_sum + pr.count_of_products * pr.price
                all_amount = all_amount + pr.count_of_products
            period_str = period

        # по дням
        elif (end_period_time - start_period_time).days < 61:
            for i in range((end_period_time - start_period_time).days + 1):
                period.append(start_period_time + timedelta(days=i))
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                data = pr.order_date.date()
                amount[(data - start_period_time).days] = int(amount[(data - start_period_time).days] + pr.count_of_products)
                sum_of_pr[(data - start_period_time).days] = int(sum_of_pr[(data - start_period_time).days] + pr.count_of_products * pr.price)
                all_sum = all_sum + pr.count_of_products * pr.price
                all_amount = all_amount + pr.count_of_products
            period_str = period
        else:
            end_year = str(end_period_time)[:4]
            start_year = str(start_period_time)[:4]
            end_month = str(end_period_time)[:7][-2:]
            start_month = str(start_period_time)[:7][-2:]
            month_count = (int(end_year) - int(start_year))*12 + int(end_month) - int(start_month) + 1
            for i in range(month_count):
                period.append(str(month_delta(start_period_time, i))[:-3])
                amount.append(0)
                sum_of_pr.append(0)
            for pr in product_in_orders:
                data = pr.order_date.date()
                now_year = str(data)[:4]
                now_month = str(data)[:7][-2:]
                count = (int(now_year) - int(start_year))*12 + int(now_month) - int(start_month)
                amount[count] = int(amount[count] + pr.count_of_products)
                sum_of_pr[count] = int(sum_of_pr[count] + pr.count_of_products * pr.price)
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
    out.update({'page_title': "Анализ продаж группы товаров"})
    out.update({'product_name': product_group_name})
    out.update({'user_role': user_role})
    return render(request, 'analyst/view_analyzed_product.html', out)


def month_diff(d1, d2):
    delta = 0
    while True:
        mdays = monthrange(d1.year, d1.month)[1]
        d1 += timedelta(days=mdays)
        if d1 <= d2:
            delta += 1
        else:
            break
    return delta


def month_delta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31,
        29 if y%4==0 and not y%400==0 else 28,31,30,31,30,31,31,30,31,30,31][m-1])
    return date.replace(day=d,month=m, year=y)
