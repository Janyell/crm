#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_analyze_managers(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    managers = Roles.objects.filter(role=1, is_deleted=0)
    for one_manager in managers:
        one_manager.full_name = one_manager.surname + ' ' + one_manager.name + ' ' + one_manager.patronymic
        if one_manager.full_name == '  ':
            one_manager.full_name = User.objects.get(id=one_manager.id).username
    current_time = str(datetime.now())
    current_mounth = current_time[5:]
    current_mounth = current_mounth[:2]
    current_year = current_time[:4]
    if 'graphic' and 'id' and 'period' in request.GET:
        type_of_period = request.GET['period']
        type_of_graphic = request.GET.getlist('graphic[]')
        managers_id = request.GET.getlist('id[]')
        analyzed_managers = []
        for manager_id in managers_id:
            manager = Roles.objects.get(id=1)
            if manager_id == 'all':
                manager.full_name = 'всех менеджерах'
            else:
                manager = Roles.objects.get(id=manager_id)
                manager.full_name = manager.surname + ' ' + manager.name + ' ' + manager.patronymic
                if manager.full_name == '  ':
                    manager.full_name = User.objects.get(id=manager.id).username
            period = []
            sum_bill_data_count = []
            sum_shipped_data_count = []
            number_call_data_count = []
            number_shipped_data_count = []
            number_bill_data_count = []
            if type_of_period == 'month':
                long_mounths = ['01', '03', '05', '07', '08', '10', '12']
                for i in range(28):
                    period.append(i+1)
                    sum_bill_data_count.append(0)
                    sum_shipped_data_count.append(0)
                    number_call_data_count.append(0)
                    number_shipped_data_count.append(0)
                    number_bill_data_count.append(0)
                if current_mounth != 02:
                    period.append(29)
                    period.append(30)
                    sum_bill_data_count.append(0)
                    sum_bill_data_count.append(0)
                    sum_shipped_data_count.append(0)
                    sum_shipped_data_count.append(0)
                    number_call_data_count.append(0)
                    number_call_data_count.append(0)
                    number_shipped_data_count.append(0)
                    number_shipped_data_count.append(0)
                    number_bill_data_count.append(0)
                    number_bill_data_count.append(0)
                    if current_mounth in long_mounths:
                        period.append(31)
                        sum_bill_data_count.append(0)
                        sum_shipped_data_count.append(0)
                        number_call_data_count.append(0)
                        number_shipped_data_count.append(0)
                        number_bill_data_count.append(0)
                if manager_id == 'all':
                    clients_orders = Clients.objects.filter(is_deleted=0, is_interested=1)
                    calls_orders = Orders.objects.filter(client__is_interested=0, is_deleted=0, is_claim=0)
                    shipped_orders = Orders.objects.filter(is_deleted=0, is_claim=0, order_status=1)
                    bill_orders = Orders.objects.filter(is_deleted=0, is_claim=1)
                else:
                    clients_orders = Clients.objects.filter(is_deleted=0, is_interested=1)
                    calls_orders = Orders.objects.filter(role_id=manager.id, client__is_interested=0, is_deleted=0, is_claim=0)
                    shipped_orders = Orders.objects.filter(role_id=manager.id, is_deleted=0, is_claim=0, order_status=1)
                    bill_orders = Orders.objects.filter(role_id=manager.id, is_deleted=0, is_claim=1)
                for order in clients_orders:
                    data = str(order.creation_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_day = data[8:]
                    data_day = data_day[:2]
                    data_year = data[:4]
                    if data_year == current_year and data_mounth == current_mounth:
                        number_call_data_count[int(data_day) - 1] += 1
                for order in calls_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_day = data[8:]
                    data_day = data_day[:2]
                    data_year = data[:4]
                    if data_year == current_year and data_mounth == current_mounth:
                        number_call_data_count[int(data_day) - 1] += 1
                for order in bill_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_day = data[8:]
                    data_day = data_day[:2]
                    data_year = data[:4]
                    if data_year == current_year and data_mounth == current_mounth:
                        number_bill_data_count[int(data_day) - 1] += 1
                        if order.bill is not None:
                            sum_bill_data_count[int(data_day) - 1] += int(order.bill)
                for order in shipped_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_day = data[8:]
                    data_day = data_day[:2]
                    data_year = data[:4]
                    if data_year == current_year and data_mounth == current_mounth:
                        number_shipped_data_count[int(data_day) - 1] += 1
                        if order.bill is not None:
                            sum_shipped_data_count[int(data_day) - 1] += int(order.bill)
                period_str = period
            elif type_of_period == 'year':
                for i in range(12):
                    period.append(i+1)
                    sum_bill_data_count.append(0)
                    sum_shipped_data_count.append(0)
                    number_call_data_count.append(0)
                    number_shipped_data_count.append(0)
                    number_bill_data_count.append(0)
                if manager_id == 'all':
                    clients_orders = Clients.objects.filter(is_deleted=0, is_interested=1)
                    calls_orders = Orders.objects.filter(client__is_interested=0, is_deleted=0, is_claim=0)
                    shipped_orders = Orders.objects.filter(is_deleted=0, is_claim=0, order_status=1)
                    bill_orders = Orders.objects.filter(is_deleted=0, is_claim=1)
                else:
                    clients_orders = Clients.objects.filter(is_deleted=0, is_interested=1)
                    calls_orders = Orders.objects.filter(role_id=manager.id, client__is_interested=0, is_deleted=0, is_claim=0)
                    shipped_orders = Orders.objects.filter(role_id=manager.id, is_deleted=0, is_claim=0, order_status=1)
                    bill_orders = Orders.objects.filter(role_id=manager.id, is_deleted=0, is_claim=1)
                for order in clients_orders:
                    data = str(order.creation_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_year = data[:4]
                    if data_year == current_year:
                        number_call_data_count[int(data_mounth) - 1] += 1
                for order in calls_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_year = data[:4]
                    if data_year == current_year:
                        number_call_data_count[int(data_mounth) - 1] += 1
                for order in bill_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_year = data[:4]
                    if data_year == current_year:
                        number_bill_data_count[int(data_mounth) - 1] += 1
                        if order.bill is not None:
                            sum_bill_data_count[int(data_mounth) - 1] += int(order.bill)
                for order in shipped_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_year = data[:4]
                    if data_year == current_year:
                        number_shipped_data_count[int(data_mounth) - 1] += 1
                        if order.bill is not None:
                            sum_shipped_data_count[int(data_mounth) - 1] += int(order.bill)
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
                # if manager_id == 'all':
                #     first_manager_id = Roles.objects.all().filter(role=1)
                user = User.objects.all().order_by('date_joined')[0]
                # user = User.objects.get(id=manager.user_ptr_id)
                all_date_of_orders = user.date_joined
                first_data = str(all_date_of_orders)
                first_data_mounth = first_data[5:]
                first_data_mounth = first_data_mounth[:2]
                first_data_year = first_data[:4]
                amount_of_period = (int(current_year) - int(first_data_year)) * 12 + int(current_mounth)\
                                   - int(first_data_mounth) + 2
                for i in range(amount_of_period):
                    period.append(i+1)
                    sum_bill_data_count.append(0)
                    sum_shipped_data_count.append(0)
                    number_call_data_count.append(0)
                    number_shipped_data_count.append(0)
                    number_bill_data_count.append(0)
                if manager_id == 'all':
                    clients_orders = Clients.objects.filter(is_deleted=0, is_interested=1)
                    calls_orders = Orders.objects.filter(client__is_interested=0, is_deleted=0, is_claim=0)
                    shipped_orders = Orders.objects.filter(is_deleted=0, is_claim=0, order_status=1)
                    bill_orders = Orders.objects.filter(is_deleted=0, is_claim=1)
                else:
                    clients_orders = Clients.objects.filter(role_id=manager.id, is_deleted=0, is_interested=1)
                    calls_orders = Orders.objects.filter(role_id=manager.id, client__is_interested=0, is_deleted=0, is_claim=0)
                    shipped_orders = Orders.objects.filter(role_id=manager.id, is_deleted=0, is_claim=0, order_status=1)
                    bill_orders = Orders.objects.filter(role_id=manager.id, is_deleted=0, is_claim=1)
                for order in clients_orders:
                    if order.creation_date is not None:
                        data = str(order.creation_date)
                        data_mounth = data[5:]
                        data_mounth = data_mounth[:2]
                        data_year = data[:4]
                        data_year_and_mounth = data[:7]
                        current_year_and_mounth = current_year + '-' + current_mounth
                        i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                        number_call_data_count[i] += 1
                for order in calls_orders:
                    if order.order_date is not None:
                        data = str(order.order_date)
                        data_mounth = data[5:]
                        data_mounth = data_mounth[:2]
                        data_year = data[:4]
                        data_year_and_mounth = data[:7]
                        current_year_and_mounth = current_year + '-' + current_mounth
                        i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                        number_call_data_count[i] += 1
                for order in bill_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_year = data[:4]
                    data_year_and_mounth = data[:7]
                    current_year_and_mounth = current_year + '-' + current_mounth
                    i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                    number_bill_data_count[i] += 1
                    if order.bill is not None:
                        sum_bill_data_count[i] += int(order.bill)
                for order in shipped_orders:
                    data = str(order.order_date)
                    data_mounth = data[5:]
                    data_mounth = data_mounth[:2]
                    data_year = data[:4]
                    data_year_and_mounth = data[:7]
                    current_year_and_mounth = current_year + '-' + current_mounth
                    i = (int(current_year) - int(data_year)) * 12 + int(current_mounth) - int(data_mounth)
                    number_shipped_data_count[i] += 1
                    if order.bill is not None:
                        sum_shipped_data_count[i] += int(order.bill)
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
                sum_bill_data_count = sum_bill_data_count[::-1]
                sum_shipped_data_count = sum_shipped_data_count[::-1]
                number_call_data_count = number_call_data_count[::-1]
                number_shipped_data_count = number_shipped_data_count[::-1]
                number_bill_data_count = number_bill_data_count[::-1]
            sum_bill_data_count_str = str(sum_bill_data_count)[1:-1]
            sum_shipped_data_count_str = str(sum_shipped_data_count)[1:-1]
            number_call_data_count_str = str(number_call_data_count)[1:-1]
            number_shipped_data_count_str = str(number_shipped_data_count)[1:-1]
            number_bill_data_count_str = str(number_bill_data_count)[1:-1]
            if 'sum-bill' in type_of_graphic:
                manager.sum_bill_data = sum_bill_data_count_str
            if 'number-bill' in type_of_graphic:
                manager.number_bill_data = number_bill_data_count_str
            if 'sum-shipped' in type_of_graphic:
                manager.sum_shipped_data = sum_shipped_data_count_str
            if 'number-shipped' in type_of_graphic:
                manager.number_shipped_data = number_shipped_data_count_str
            if 'number-call' in type_of_graphic:
                manager.number_call_data = number_call_data_count_str
            analyzed_managers.append(manager)
            out.update({'select_period': period_str})
        out.update({'period': type_of_period})
        out.update({'analyzed_managers': analyzed_managers})
        out.update({'graphic': type_of_graphic})
        out.update({'id': managers_id})
    out.update({'page_title': "Анализ работы менеджеров"})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'managers': managers})
    return render(request, 'analyze_managers.html', out)