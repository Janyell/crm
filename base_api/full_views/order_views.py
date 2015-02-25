#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import render, render_to_response, redirect
from datetime import datetime
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import random
import string


def full_add_edit_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    out.update({'modal_title': 'Добавление клиента'})
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'page': page})
        out.update({'length': length})
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if 'client-id' in request.GET:
            client_id = request.GET['client-id']
            out.update({'client_id': client_id})
            # out.update({'rt': ghg})
        if 'pk' in request.POST:
            pk = request.POST['pk']
            order = Orders.objects.get(id=pk)
            files = []
            if Order_Files.objects.filter(order_id=order.id).all() is not None:
                for order_file in Order_Files.objects.filter(order_id=order.id).all():
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    files.append(order_file)
            out.update({'files': files})
            source = request.POST['source']
            if request.POST['company'] != '':
                id_company = int(request.POST['company'])
                company = Companies.objects.get(id=id_company, is_deleted=0)
            else:
                company = None
            if request.POST['payment_date'] != '':
                payment_date = request.POST['payment_date']
                payment_date = datetime.strptime(payment_date, '%Y-%m-%d %H:%M:%S')
            else:
                payment_date = None
            if request.POST['order_status'] != '':
                order_status = int(request.POST['order_status'])
            else:
                order_status = None
            if request.POST['bill_status'] != '':
                bill_status = int(request.POST['bill_status'])
            else:
                bill_status = None
            if request.POST['ready_date'] != '':
                ready_date = request.POST['ready_date']
                ready_date = datetime.strptime(ready_date, '%Y-%m-%d %H:%M:%S')
            else:
                ready_date = None
            comment = request.POST['comment']
            city = request.POST['city']
            account_number = request.POST['account_number']
            if request.POST['client'] != '':
                id_client = int(request.POST['client'])
                client = Clients.objects.get(id=id_client, is_deleted=0)
            else:
                out.update({"error": 1})
                OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                form = OrdersForm({'client': request.POST['client'], 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        product.count_of_products = count_of_products
                out.update({'order_form': form})
                out.update({'page_title': "Редактирование заказа"})
                return render(request, 'add_edit_order.html', out)
            if request.POST['bill'] != '':
                try:
                    bill = int(request.POST['bill'])
                except Exception:
                    out.update({"error": 1})
                    OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                        queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    form = OrdersForm({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'payment_date': payment_date, 'order_status': order_status,
                                       'bill_status': bill_status, 'city': city, 'comment': comment,
                                       'source': source, 'ready_date': ready_date, 'account_number': account_number})
                    form.products = Products.objects.filter(is_deleted=0)
                    products_list = request.POST.getlist('products[]')
                    for product in form.products:
                        if str(product.id) in products_list:
                            name_of_pr = 'select-product__number_' + str(product.id)
                            count_of_products = request.POST[name_of_pr]
                            product.count_of_products = count_of_products
                    out.update({'order_form': form})
                    out.update({'page_title': "Редактирование заказа"})
                    return render(request, 'add_edit_order.html', out)
            else:
                bill = None
            new_order = Orders.objects.get(id=pk, is_deleted=0)
            is_comment_my = False
            if new_order.role_id == request.user.id:
                is_comment_my = True
            new_order.is_comment_my = is_comment_my
            new_order.client = client
            new_order.source = source
            new_order.company = company
            new_order.bill = bill
            new_order.payment_date = payment_date
            new_order.order_status = order_status
            new_order.bill_status = bill_status
            new_order.ready_date = ready_date
            new_order.comment = comment
            new_order.city = city
            new_order.account_number = account_number
            new_order.save(force_update=True)
            old_products = Order_Product.objects.filter(order_id=pk)
            for old_product in old_products:
                old_product.is_deleted = 1
                old_product.save(update_fields=["is_deleted"])
            products_list = request.POST.getlist('products[]')
            for id_of_pr in products_list:
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    if Products.objects.filter(title=title_of_product, is_deleted=0).count() != 0:
                        out.update({"error": 2})
                        OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                            queryset=Companies.objects.filter(is_deleted=0), required=False)
                        OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                                           'payment_date': payment_date, 'order_status': order_status,
                                           'bill_status': bill_status, 'city': city, 'comment': comment,
                                           'source': source, 'ready_date': ready_date, 'account_number': account_number})
                        form.products = Products.objects.filter(is_deleted=0)
                        products_list = request.POST.getlist('products[]')
                        for product in form.products:
                            if str(product.id) in products_list:
                                name_of_pr = 'select-product__number_' + str(product.id)
                                count_of_products = request.POST[name_of_pr]
                                product.count_of_products = count_of_products
                        out.update({'order_form': form})
                        out.update({'page_title': "Редактирование заказа"})
                        return render(request, 'add_edit_order.html', out)
                    else:
                        name_of_pr = 'select-product__number_' + id_of_pr
                        count_of_products = request.POST[name_of_pr]
                        if int(count_of_products) > 0:
                            product = Products.objects.create(title=title_of_product)
                else:
                    name_of_pr = 'select-product__number_' + id_of_pr
                    count_of_products = request.POST[name_of_pr]
                    product = Products.objects.get(id=id_of_pr, is_deleted=0)
                if int(count_of_products) > 0:
                    if Order_Product.objects.filter(product_id=product.id, order_id=pk, is_deleted=0).count() != 0:
                        order_product = Order_Product.objects.get(product_id=product.id, order_id=pk, is_deleted=0)
                        new_order_product_link = Order_Product(id=order_product.id, order=new_order, product=product,
                                                               order_date=datetime.now(),
                                                               count_of_products=count_of_products)
                        new_order_product_link.save(force_update=True)
                    else:
                        new_order_product_link = Order_Product.objects.create(order=new_order,
                                                                              product=product,
                                                                              order_date=datetime.now(),
                                                                              count_of_products=count_of_products)
            if new_order.in_archive == 1:
                return HttpResponseRedirect('/orders/archive/')
            return HttpResponseRedirect('/orders/')
        if form.is_valid():
            client = form.cleaned_data['client']
            role = Roles.objects.get(id=request.user.id, is_deleted=0)
            source = form.cleaned_data['source']
            unique_number = id_generator()
            company = form.cleaned_data['company']
            bill = form.cleaned_data['bill']
            payment_date = form.cleaned_data['payment_date']
            order_status = form.cleaned_data['order_status']
            bill_status = form.cleaned_data['bill_status']
            ready_date = form.cleaned_data['ready_date']
            comment = form.cleaned_data['comment']
            city = form.cleaned_data['city']
            account_number = form.cleaned_data['account_number']
            products_list = request.POST.getlist('products[]')
            is_order_create = False
            new_order_was_not_created = True
            for id_of_pr in products_list:
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    if Products.objects.filter(title=title_of_product, is_deleted=0).count() != 0:
                        out.update({"error": 2})
                        OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                    required=False)
                        OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                                           'payment_date': payment_date, 'order_status': order_status,
                                           'bill_status': bill_status, 'city': city, 'comment': comment,
                                           'source': source, 'ready_date': ready_date, 'account_number': account_number})
                        form.products = Products.objects.filter(is_deleted=0)
                        products_list = request.POST.getlist('products[]')
                        for product in form.products:
                            if str(product.id) in products_list:
                                name_of_pr = 'select-product__number_' + str(product.id)
                                count_of_products = request.POST[name_of_pr]
                                product.count_of_products = count_of_products
                        out.update({'order_form': form})
                        out.update({'page_title': "Добавление заказа"})
                        return render(request, 'add_edit_order.html', out)
                    else:
                        name_of_pr = 'select-product__number_' + id_of_pr
                        count_of_products = request.POST[name_of_pr]
                        if int(count_of_products) > 0:
                            product = Products.objects.create(title=title_of_product)
                else:
                    name_of_pr = 'select-product__number_' + id_of_pr
                    count_of_products = request.POST[name_of_pr]
                    product = Products.objects.get(id=id_of_pr, is_deleted=0)
                if int(count_of_products) > 0:
                    is_order_create = True
                    if new_order_was_not_created:
                        new_order_was_not_created = False
                        new_order = Orders.objects.create(order_date=datetime.now(), client=client, role=role, source=source,
                                              unique_number=unique_number, company=company, bill=bill,
                                              payment_date=payment_date, order_status=order_status, city=city,
                                              bill_status=bill_status, ready_date=ready_date, comment=comment,
                                              account_number=account_number)
                    new_order_product_link = Order_Product.objects.create(order=new_order, product=product,
                                                                          order_date=datetime.now(),
                                                                          count_of_products=count_of_products)
            if is_order_create:
                if 'only-save' in form.data:
                    return HttpResponseRedirect('/orders/')
                else:
                    print(new_order.id)
                    return HttpResponseRedirect('/uploads/?id=%s' % new_order.id)
            else:
                OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=False)
                OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        product.count_of_products = count_of_products
                out.update({'error': 3})
                out.update({'order_form': form})
                out.update({'page_title': "Добавление заказа"})
        else:
            print(form.errors)
            client = request.POST['client']
            source = request.POST['source']
            company = request.POST['company']
            bill = request.POST['bill']
            payment_date = request.POST['payment_date']
            order_status = request.POST['order_status']
            bill_status = request.POST['bill_status']
            ready_date = request.POST['ready_date']
            comment = request.POST['comment']
            city = request.POST['city']
            account_number = request.POST['account_number']
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                               'payment_date': payment_date, 'order_status': order_status,
                               'bill_status': bill_status, 'city': city, 'comment': comment,
                               'source': source, 'ready_date': ready_date, 'account_number': account_number})
            form.products = Products.objects.filter(is_deleted=0)
            products_list = request.POST.getlist('products[]')
            for product in form.products:
                if str(product.id) in products_list:
                    name_of_pr = 'select-product__number_' + str(product.id)
                    count_of_products = request.POST[name_of_pr]
                    product.count_of_products = count_of_products
            out.update({'error': 1})
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
    else:
        if 'client-id' in request.GET:
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_id = request.GET['client-id']
            client = Clients.objects.get(id=client_id, is_deleted=0)
            form = OrdersForm({'client': client})
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'client_id': client_id})
            out.update({'page_title': "Добавление заказа"})
        elif 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0)
            client = order.client
            out.update({'client_id': client.id})
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = OrdersForm({'client': order.client, 'company': order.company, 'bill': order.bill,
                               'payment_date': order.payment_date, 'order_status': order.order_status,
                               'bill_status': order.bill_status, 'city': order.city, 'comment': order.comment,
                               'source': order.source, 'ready_date': order.ready_date, 'account_number': order.account_number})
            form.products = Products.objects.filter(is_deleted=0)
            order_products = Order_Product.objects.filter(order_id=id_order, is_deleted=0)
            products_list = []
            for pr in order_products:
                products_list.append(pr.product_id)
            for product in form.products:
                if product.id in products_list:
                    product.count_of_products = Order_Product.objects.get(product_id=product.id,
                                                                          order_id=id_order, is_deleted=0).count_of_products
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заказа"})
        else:
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = OrdersForm()
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
    organizations = []
    for organization in Clients.objects.all().order_by('organization'):
        if organization.organization != "":
            organizations.append(organization.organization)
    out.update({'organizations': organizations})
    return render(request, 'add_edit_order.html', out)


def full_delete_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order = Orders.objects.get(pk=id, is_deleted=0)
    if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    order.is_deleted = 1
    order.save(update_fields=["is_deleted"])
    return HttpResponseRedirect('/orders/')


def full_get_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
        out.update({'page': page})
        out.update({'length': length})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    if 'client-id' in request.GET:
        client_id = request.GET['client-id']
        if Clients.objects.filter(id=client_id, is_deleted=0).count() != 1:
            out.update({'page_title': "Данного клиента не существует!"})
            return render(request, 'get_orders.html', out)
        client = Clients.objects.get(id=client_id, is_deleted=0)
        orders = Orders.objects.filter(is_deleted=0, client=client, is_claim=0).order_by('-order_status')
        out.update({'page_title': "История заказов "})
        out.update({'client_id': client_id})
        if client.organization == '':
            client.organization_or_full_name = client.last_name + ' ' + client.name + ' ' + client.patronymic
        else:
            client.organization_or_full_name = client.organization
        out.update({'organization_or_full_name': client.organization_or_full_name})
        out.update({'client_id': client.id})
    else:
        orders = Orders.objects.filter(is_deleted=0, in_archive=0, is_claim=0).order_by('-order_status')
        out.update({'page_title': "Заказы"})
    for order in orders:
        if order.client.organization == '':
            order.client.organization_or_full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        else:
            order.client.organization_or_full_name = order.client.organization
        order.client.full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        prs = Order_Product.objects.filter(order_id=order.id, is_deleted=0)
        products_list = []
        for pr in prs:
            products_list.append(pr)
        order.products = products_list
        if order.order_status == 0:
            order.order_status = 'В производстве'
        elif order.order_status == 1:
            order.order_status = 'Отгружен'
        elif order.order_status == 2:
            order.order_status = 'Готов'
        else:
            order.order_status = ''
        if order.bill is not None:
            orders_count_str = str(order.bill)
            orders_count_str_reverse = orders_count_str[::-1]
            orders_count_str_right_format = ''
            for i in range(0, len(orders_count_str)/3 + 1):
                j = 3
                if i != (len(orders_count_str)/3):
                    orders_count_str_right_format = orders_count_str_right_format + orders_count_str_reverse[i*j] + \
                                                    orders_count_str_reverse[i*j+1] + orders_count_str_reverse[i*j+2] + ' '
                else:
                    if (len(orders_count_str) % 3) == 2:
                        orders_count_str_right_format = orders_count_str_right_format + orders_count_str_reverse[i*j] + \
                                                        orders_count_str_reverse[i*j+1]
                    elif (len(orders_count_str) % 3) == 1:
                        orders_count_str_right_format = orders_count_str_right_format + orders_count_str_reverse[i*j]
            orders_count_str = orders_count_str_right_format[::-1]
            order.bill_right_format = orders_count_str
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                order_file.name = order_file.title
                order_file.url = order_file.file.url
                order.files.append(order_file)
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'orders': orders})
    print(out)
    return render(request, 'get_orders.html', out)


def full_get_old_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    orders = Orders.objects.filter(is_deleted=0, in_archive=1, is_claim=0)
    for order in orders:
        if order.client.organization == '':
            order.client.organization_or_full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        else:
            order.client.organization_or_full_name = order.client.organization
        order.client.full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        prs = Order_Product.objects.filter(order_id=order.id, is_deleted=0)
        products_list = []
        for pr in prs:
            products_list.append(pr)
        order.products = products_list
        # if order.order_status == 0:
        #     order.order_status = 'В производстве'
        # elif order.order_status == 1:
        #     order.order_status = 'Отгружен'
        # elif order.order_status  == 2:
        #     order.order_status = 'Готов'
        # else:
        #     order.order_status = ''
        order.order_status = 'Отгружен'
        if order.bill is not None:
            orders_count_str = str(order.bill)
            orders_count_str_reverse = orders_count_str[::-1]
            orders_count_str_right_format = ''
            for i in range(0, len(orders_count_str)/3 + 1):
                j = 3
                if i != (len(orders_count_str)/3):
                    orders_count_str_right_format = orders_count_str_right_format + orders_count_str_reverse[i*j] + \
                                                    orders_count_str_reverse[i*j+1] + orders_count_str_reverse[i*j+2] + ' '
                else:
                    if (len(orders_count_str) % 3) == 2:
                        orders_count_str_right_format = orders_count_str_right_format + orders_count_str_reverse[i*j] + \
                                                        orders_count_str_reverse[i*j+1]
                    elif (len(orders_count_str) % 3) == 1:
                        orders_count_str_right_format = orders_count_str_right_format + orders_count_str_reverse[i*j]
            orders_count_str = orders_count_str_right_format[::-1]
            order.bill_right_format = orders_count_str
            order.bill = order.bill_right_format
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                order_file.name = order_file.title
                order_file.url = order_file.file.url
                order.files.append(order_file)
    out.update({'page_title': "Архив заказов"})
    out.update({'orders': orders})
    return render(request, 'get_orders.html', out)


def full_edit_order_for_factory(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        if 'pk' in request.POST:
            pk = request.POST['pk']
            if request.POST['order_status'] != '':
                order_status = int(request.POST['order_status'])
            else:
                order_status = None
            if request.POST['ready_date'] != '':
                ready_date = request.POST['ready_date']
                ready_date = datetime.strptime(ready_date, '%Y-%m-%d %H:%M:%S')
            else:
                ready_date = None
            new_order = Orders.objects.get(id=pk, is_deleted=0)
            new_order.order_status = order_status
            new_order.ready_date = ready_date
            new_order.save(force_update=True)
            return HttpResponseRedirect('/orders/')
        else:
            return HttpResponseRedirect('/orders')
    else:
        if 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0)
            form = OrdersForm({'order_status': order.order_status,
                               'ready_date': order.ready_date})
            out.update({'order_form': form})
            out.update({'unique_number': order.unique_number})
            out.update({'page_title': "Редактирование заказа"})
        else:
            return HttpResponseRedirect('/orders/')
    return render(request, 'edit_order_for_factory.html', out)


def full_add_in_archive(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order = Orders.objects.get(pk=id, is_deleted=0)
    if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    order.in_archive = 1
    order.save(update_fields=["in_archive"])
    return HttpResponseRedirect('/orders/')


def full_delete_from_archive(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order = Orders.objects.get(pk=id, is_deleted=0)
    order.in_archive = 0
    order.save(update_fields=["in_archive"])
    return HttpResponseRedirect('/orders/archive/')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
