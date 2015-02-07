#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
import random
import string


def full_get_claims(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_id = request.user.id
    out.update({'user_id': user_id})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    orders = Orders.objects.filter(is_deleted=0, in_archive=0, is_claim=1)
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
        if order.bill_status == 0:
            order.bill_status = 'Выставлен'
        elif order.bill_status == 1:
            order.bill_status = 'Нужна доплата'
        elif order.bill_status == 2:
            order.bill_status = 'Оплачен'
        else:
            order.bill_status = ''
        if order.bill != None:
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
            order.bill = orders_count_str
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': "Заявки"})
    out.update({'claims': orders})
    return render(request, 'get_claims.html', out)


def full_add_edit_claim(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    out.update({'modal_title': 'Добавление человека'})
    if request.method == 'POST':
        form = ClaimsForm(request.POST)
        if 'pk' in request.POST:
            pk = request.POST['pk']
            comment = request.POST['comment']
            if request.POST['company'] != '':
                id_company = int(request.POST['company'])
                company = Companies.objects.get(id=id_company, is_deleted=0)
            else:
                company = None
            if request.POST['bill_status'] != '':
                bill_status = int(request.POST['bill_status'])
            else:
                bill_status = None
            account_number = request.POST['account_number']
            if request.POST['client'] != '':
                id_client = int(request.POST['client'])
                client = Clients.objects.get(id=id_client, is_deleted=0)
            else:
                out.update({"error": 1})
                ClaimsForm.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                form = ClaimsForm({'client': request.POST['client'], 'company': company, 'bill': request.POST['bill'],
                                   'bill_status': bill_status, 'account_number': account_number,
                                   'comment': comment})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        product.count_of_products = count_of_products
                out.update({'order_form': form})
                out.update({'page_title': "Редактирование заявки"})
                return render(request, 'add_edit_order.html', out)
            if request.POST['bill'] != '':
                try:
                    bill = int(request.POST['bill'])
                except Exception:
                    out.update({"error": 1})
                    ClaimsForm.base_fields['company'] = CompanyModelChoiceField(
                        queryset=Companies.objects.filter(is_deleted=0), required=False)
                    ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    form = ClaimsForm({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'bill_status': bill_status, 'account_number': account_number,
                                       'comment': comment})
                    form.products = Products.objects.filter(is_deleted=0)
                    products_list = request.POST.getlist('products[]')
                    for product in form.products:
                        if str(product.id) in products_list:
                            name_of_pr = 'select-product__number_' + str(product.id)
                            count_of_products = request.POST[name_of_pr]
                            product.count_of_products = count_of_products
                    out.update({'order_form': form})
                    out.update({'page_title': "Редактирование заявки"})
                    return render(request, 'add_edit_order.html', out)
            else:
                bill = None
            new_claim = Orders.objects.get(id=pk, is_deleted=0, is_claim=1)
            is_comment_my = False
            if new_claim.role_id == request.user.id:
                is_comment_my = True
            new_claim.is_comment_my = is_comment_my
            new_claim.client = client
            new_claim.company = company
            new_claim.comment = comment
            new_claim.bill = bill
            new_claim.bill_status = bill_status
            displacement = 0
            if bill_status == 1 or bill_status == 2:
                new_claim.is_claim = 0
                displacement = 1
                client.is_interested = 0
            new_claim.account_number = account_number
            new_claim.save(force_update=True)
            old_products = Order_Product.objects.filter(order_id=pk)
            for old_product in old_products:
                old_product.is_deleted = 1
                old_product.save(update_fields=["is_deleted"])
            products_list = request.POST.getlist('products[]')
            for id_of_pr in products_list:
                print(int(id_of_pr))
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    if Products.objects.filter(title=title_of_product, is_deleted=0).count() != 0:
                        out.update({"error": 2})
                        ClaimsForm.base_fields['company'] = CompanyModelChoiceField(
                            queryset=Companies.objects.filter(is_deleted=0), required=False)
                        ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        form = ClaimsForm({'client': client, 'company': company, 'bill': bill,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment})
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
                        new_order_product_link = Order_Product(id=order_product.id, order=new_claim, product=product,
                                                               order_date=datetime.now(),
                                                               count_of_products=count_of_products)
                        new_order_product_link.save(force_update=True)
                        client.save(update_fields=["is_interested"])
                    else:
                        new_order_product_link = Order_Product.objects.create(order=new_claim,
                                                                              product=product,
                                                                              order_date=datetime.now(),
                                                                              count_of_products=count_of_products)
                        client.save(update_fields=["is_interested"])
            if displacement == 1:
                return HttpResponseRedirect('/claims/?displacement=1')
            else:
                return HttpResponseRedirect('/claims/')
        if form.is_valid():
            client = form.cleaned_data['client']
            role = Roles.objects.get(id=request.user.id, is_deleted=0)
            unique_number = id_generator()
            company = form.cleaned_data['company']
            comment = form.cleaned_data['comment']
            bill = form.cleaned_data['bill']
            bill_status = form.cleaned_data['bill_status']
            displacement = 0
            if bill_status == 1 or bill_status == 2:
                is_claim = 0
                client.is_interested = 0
                displacement = 1
            else:
                is_claim = 1
            account_number = form.cleaned_data['account_number']
            products_list = request.POST.getlist('products[]')
            is_claim_create = False
            new_claim_was_not_created = True
            for id_of_pr in products_list:
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    if Products.objects.filter(title=title_of_product, is_deleted=0).count() != 0:
                        out.update({"error": 2})
                        ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                    required=False)
                        ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        form = ClaimsForm({'client': client, 'company': company, 'bill': bill,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment})
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
                    is_claim_create = True
                    if new_claim_was_not_created:
                        new_claim_was_not_created = False
                        client.save(update_fields=["is_interested"])
                        new_claim = Orders.objects.create(order_date=datetime.now(), client=client, role=role,
                                              unique_number=unique_number, company=company, bill=bill,
                                              bill_status=bill_status, is_claim=is_claim,
                                              account_number=account_number, comment=comment)
                    new_order_product_link = Order_Product.objects.create(order=new_claim, product=product,
                                                                          order_date=datetime.now(),
                                                                          count_of_products=count_of_products)
                    client.save(update_fields=["is_interested"])
            if is_claim_create:
                if displacement == 1:
                    return HttpResponseRedirect('/claims/?displacement=1')
                else:
                    return HttpResponseRedirect('/claims/')
            else:
                ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=False)
                ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                form = ClaimsForm({'client': client, 'company': company, 'bill': bill,
                                   'bill_status': bill_status, 'account_number': account_number,
                                   'comment': comment})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        product.count_of_products = count_of_products
                out.update({'error': 3})
                out.update({'order_form': form})
                out.update({'page_title': "Добавление заявки"})
        else:
            print(form.errors)
            client = request.POST['client']
            company = request.POST['company']
            comment = request.POST['comment']
            bill = request.POST['bill']
            bill_status = request.POST['bill_status']
            account_number = request.POST['account_number']
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm({'client': client, 'company': company, 'bill': bill,
                               'bill_status': bill_status, 'account_number': account_number,
                               'comment': comment})
            form.products = Products.objects.filter(is_deleted=0)
            products_list = request.POST.getlist('products[]')
            for product in form.products:
                if str(product.id) in products_list:
                    name_of_pr = 'select-product__number_' + str(product.id)
                    count_of_products = request.POST[name_of_pr]
                    product.count_of_products = count_of_products
            out.update({'error': 1})
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заявки"})
    else:
        if 'client-id' in request.GET:
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_id = request.GET['client-id']
            client = Clients.objects.get(id=client_id, is_deleted=0, is_interested=1)
            form = ClaimsForm({'client': client})
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заявки"})
        elif 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            claim = Orders.objects.get(pk=id_order, is_deleted=0, is_claim=1)
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm({'client': claim.client, 'company': claim.company, 'bill': claim.bill,
                               'bill_status': claim.bill_status, 'account_number': claim.account_number,
                               'comment': claim.comment})
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
            out.update({'page_title': "Редактирование заявки"})
        else:
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm()
            form.products = Products.objects.filter(is_deleted=0)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заявки"})
    organizations = []
    for organization in Clients.objects.all().order_by('organization'):
        if organization.organization != "":
            organizations.append(organization.organization)
    out.update({'organizations': organizations})
    return render(request, 'add_edit_order.html', out)


def full_delete_claim(request):
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
    return HttpResponseRedirect('/claims/')


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))