#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import random
import string


def full_add_edit_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            client = form.cleaned_data['client']
            role = Roles.objects.get(id=request.user.id)
            source = form.cleaned_data['source']
            unique_number = id_generator()
            company = form.cleaned_data['company']
            bill = form.cleaned_data['bill']
            payment_date = form.cleaned_data['payment_date']
            order_status = form.cleaned_data['order_status']
            bill_status = form.cleaned_data['bill_status']
            ready_date = form.cleaned_data['ready_date']
            comment = form.cleaned_data['comment']
            new_order = Orders.objects.create(order_date=datetime.now(), client=client, role=role, source=source,
                                              unique_number=unique_number, company=company, bill=bill,
                                              payment_date=payment_date, order_status=order_status,
                                              bill_status=bill_status, ready_date=ready_date, comment=comment)
            products_list = request.POST['select-product__number_']
            print(products_list)
            new_order_product_link = Order_Product.objects.create(order=new_order, product=product,
                                                                  order_date=datetime.now(),
                                                                  count_of_products=count_of_products)
            return HttpResponseRedirect('/orders/')
        else:
            out.update({'page_title': "Добавление заказа"})
    else:
        OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.all(), required=False)
        OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.all())
        form = OrdersForm()

        all_products = Products.objects.filter()
        form.products = all_products

        out.update({'order_form': form})
        out.update({'page_title': "Добавление заказа"})
    return render(request, 'add_edit_order.html', out)


def full_get_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    orders = Orders.objects.filter(is_deleted=0)

    # idid = 2
    # str_idd_add = 'ererer_' + str(idid)
    # print(str_idd_add)

    out = {}
    out.update({'page_title': "Заказы"})
    out.update({'orders': orders})
    return render(request, 'get_orders.html', out)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
