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
        if 'pk' in request.POST:
            print("grfhjbafhjb")
        payment_date = request.POST['payment_date']
        print(payment_date)
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
            products_list = request.POST.getlist('products[]')
            for id_of_pr in products_list:
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    name_of_pr = 'select-product__number_' + id_of_pr
                    count_of_products = request.POST[name_of_pr]
                    product = Products.objects.create(title=title_of_product)
                else:
                    name_of_pr = 'select-product__number_' + id_of_pr
                    count_of_products = request.POST[name_of_pr]
                    product = Products.objects.get(id=id_of_pr)
                new_order_product_link = Order_Product.objects.create(order=new_order, product=product,
                                                                      order_date=datetime.now(),
                                                                      count_of_products=count_of_products)
            return HttpResponseRedirect('/orders/')
        else:
            print(form.errors)
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0))
            form = OrdersForm()
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'error': 1})
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
    else:
        if 'client-id' in request.GET:
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0))
            client_id = request.GET['client-id']
            client = Clients.objects.get(id=client_id)
            form = OrdersForm({'client': client})
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
        elif 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order)
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0))
            form = OrdersForm({'client': order.client, 'company': order.company, 'bill': order.bill,
                               'payment_date': order.payment_date, 'order_status': order.order_status,
                               'bill_status': order.bill_status, 'city': order.city, 'comment': order.comment,
                               'source': order.source, 'ready_date': order.ready_date})
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заказа"})
        else:
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0))
            form = OrdersForm()
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
    return render(request, 'add_edit_order.html', out)


def full_delete_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    id = request.GET['id']
    order = Orders.objects.get(pk=id)
    order.is_deleted = 1
    order.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/orders/')


def full_get_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    orders = Orders.objects.filter(is_deleted=0)
    for order in orders:
        prs = Order_Product.objects.filter(order_id=order.id)
        print(order.id)
        products_list = []
        for pr in prs:
            products_list.append(pr)
        order.products = products_list
        for product in order.products:
            print(product.product_id, product.count_of_products)
    out = {}
    out.update({'page_title': "Заказы"})
    out.update({'orders': orders})
    return render(request, 'get_orders.html', out)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
