#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from base_api.constants import DEFAULT_SORT_TYPE_FOR_CLAIM, SORT_TYPE_FOR_CLAIM, DEFAULT_NUMBER_FOR_PAGE
from base_api.full_views.helper import get_request_param_as_string
from base_api.full_views.order_views import right_money_format
from base_api.form import *
from django.http import *
import random
import string


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
        if 'client-id' in request.GET:
            client_id = request.GET['client-id']
            out.update({'client_id': client_id})
        if 'pk' in request.POST:
            pk = request.POST['pk']
            claim = Orders.objects.get(id=pk)
            source = request.POST['source']
            comment = request.POST['comment']
            try:
                brought_sum = int(request.POST['brought_sum'])
            except Exception:
                brought_sum = None
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
            if 'role' in request.POST:
                role = request.POST['role']
            else:
                role = request.user.id
            if request.POST['client'] != '':
                id_client = int(request.POST['client'])
                client = Clients.objects.get(id=id_client, is_deleted=0)
            else:
                out.update({"error": 1})
                if user_role == 0:
                    ClaimsFormForAdmins.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=False)
                    ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                else:
                    ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=False)
                    ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                if user_role == 0:
                    ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                else:
                    ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                if user_role == 0:
                    form = ClaimsFormForAdmins({'client': request.POST['client'], 'company': company, 'bill': request.POST['bill'],
                                   'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                   'comment': comment, 'role': role, 'brought_sum': brought_sum})
                else:
                    form = ClaimsForm({'client': request.POST['client'], 'company': company, 'bill': request.POST['bill'],
                                   'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                   'comment': comment, 'brought_sum': brought_sum})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        product.count_of_products = count_of_products
                        price_of_pr = 'select-product__price_' + str(product.id)
                        price_of_products = request.POST[price_of_pr]
                        product.price = price_of_products
                    product.price_right_format = right_money_format(product.price)
                out.update({'order_form': form})
                ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                client_form = ClientRelatedForm()
                out.update({'form': client_form})
                out.update({'page_title': "Редактирование заявки"})
                return render(request, 'order_claim/add_edit_order.html', out)
            if request.POST['bill'] != '':
                try:
                    bill = int(request.POST['bill'])
                except Exception:
                    out.update({"error": 1})
                    if user_role == 0:
                        ClaimsFormForAdmins.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                required=False)
                        ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                    else:
                        ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                required=False)
                        ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                    if user_role == 0:
                        ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    else:
                        ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    if user_role == 0:
                        form = ClaimsFormForAdmins({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                       'comment': comment, 'role': role, 'brought_sum': brought_sum})
                    else:
                        form = ClaimsForm({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                       'comment': comment, 'brought_sum': brought_sum})
                    form.products = Products.objects.filter(is_deleted=0)
                    products_list = request.POST.getlist('products[]')
                    for product in form.products:
                        if str(product.id) in products_list:
                            name_of_pr = 'select-product__number_' + str(product.id)
                            count_of_products = request.POST[name_of_pr]
                            product.count_of_products = count_of_products
                            price_of_pr = 'select-product__price_' + str(product.id)
                            price_of_products = request.POST[price_of_pr]
                            product.price = price_of_products
                        product.price_right_format = right_money_format(product.price)
                    out.update({'order_form': form})
                    ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    client_form = ClientRelatedForm()
                    out.update({'form': client_form})
                    out.update({'page_title': "Редактирование заявки"})
                    return render(request, 'order_claim/add_edit_order.html', out)
            else:
                bill = None
            new_claim = Orders.objects.get(id=pk, is_deleted=0, is_claim=1)
            is_comment_my = False
            if new_claim.role_id == request.user.id:
                is_comment_my = True
            new_claim.is_comment_my = is_comment_my
            new_claim.client = client
            new_claim.source = Sources.objects.get(id=source)
            new_claim.company = company
            new_claim.comment = comment
            new_claim.bill = bill
            new_claim.brought_sum = brought_sum
            new_claim.bill_status = bill_status
            new_claim.role = Roles.objects.filter(id=role).first()
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
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    if Products.objects.filter(title=title_of_product, is_deleted=0).count() != 0:
                        out.update({"error": 2})
                        if user_role == 0:
                            ClaimsFormForAdmins.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                    required=False)
                            ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                            ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                        else:
                            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                    required=False)
                            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                        if user_role == 0:
                            ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        else:
                            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        if user_role == 0:
                            form = ClaimsFormForAdmins({'client': client, 'company': company, 'bill': bill, 'source': source,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment, 'role': role, 'brought_sum': brought_sum})
                        else:
                            form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment, 'brought_sum': brought_sum})
                        form.products = Products.objects.filter(is_deleted=0)
                        products_list = request.POST.getlist('products[]')
                        for product in form.products:
                            if str(product.id) in products_list:
                                name_of_pr = 'select-product__number_' + str(product.id)
                                count_of_products = request.POST[name_of_pr]
                                product.count_of_products = count_of_products
                                price_of_pr = 'select-product__price_' + str(product.id)
                                price_of_products = request.POST[price_of_pr]
                                product.price = price_of_products
                            product.price_right_format = right_money_format(product.price)
                        out.update({'order_form': form})
                        ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        client_form = ClientRelatedForm()
                        out.update({'form': client_form})
                        out.update({'page_title': "Редактирование заказа"})
                        return render(request, 'order_claim/add_edit_order.html', out)
                    else:
                        name_of_pr = 'select-product__number_' + id_of_pr
                        count_of_products = request.POST[name_of_pr]
                        price_of_pr = 'select-product__price_' + id_of_pr
                        price_of_products = request.POST[price_of_pr]
                        product.price = price_of_products
                        if int(count_of_products) > 0:
                            product = Products.objects.create(title=title_of_product, price=price_of_products)
                else:
                    name_of_pr = 'select-product__number_' + id_of_pr
                    count_of_products = request.POST[name_of_pr]
                    price_of_pr = 'select-product__price_' + id_of_pr
                    price_of_products = request.POST[price_of_pr]
                    product = Products.objects.get(id=id_of_pr, is_deleted=0)
                    product.price = price_of_products
                    product.save(force_update=True)
                if int(count_of_products) > 0:
                    if Order_Product.objects.filter(product_id=product.id, order_id=pk, is_deleted=0).count() != 0:
                        order_product = Order_Product.objects.get(product_id=product.id, order_id=pk, is_deleted=0)
                        new_order_product_link = Order_Product(id=order_product.id, order=new_claim, product=product,
                                                               order_date=datetime.now(),
                                                               count_of_products=count_of_products,
                                                               price=price_of_products)
                        new_order_product_link.save(force_update=True)
                        client.save(update_fields=["is_interested"])
                    else:
                        new_order_product_link = Order_Product.objects.create(order=new_claim,
                                                                              product=product,
                                                                              order_date=datetime.now(),
                                                                              count_of_products=count_of_products,
                                                                              price=price_of_products)
                        client.save(update_fields=["is_interested"])
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params = '?search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            if displacement == 1:
                get_params = '&'
                get_params += get_request_param_as_string(request)
                return HttpResponseRedirect('/claims/?displacement=1' + get_params)
            else:
                get_params = '?'
                get_params += get_request_param_as_string(request)
                return HttpResponseRedirect('/claims/' + get_params)
        if form.is_valid():
            client = form.cleaned_data['client']
            source = form.cleaned_data['source']
            role = Roles.objects.get(id=request.user.id, is_deleted=0)
            unique_number = id_generator()
            company = form.cleaned_data['company']
            comment = form.cleaned_data['comment']
            bill = form.cleaned_data['bill']
            try:
                brought_sum = int(request.POST['brought_sum'])
            except Exception:
                brought_sum = None
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
                        ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                        ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment, 'brought_sum': brought_sum})
                        form.products = Products.objects.filter(is_deleted=0)
                        products_list = request.POST.getlist('products[]')
                        for product in form.products:
                            if str(product.id) in products_list:
                                name_of_pr = 'select-product__number_' + str(product.id)
                                count_of_products = request.POST[name_of_pr]
                                product.count_of_products = count_of_products
                                price_of_pr = 'select-product__price_' + str(product.id)
                                price_of_products = request.POST[price_of_pr]
                                product.price = price_of_products
                            product.price_right_format = right_money_format(product.price)
                        out.update({'order_form': form})
                        ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        client_form = ClientRelatedForm()
                        out.update({'form': client_form})
                        out.update({'page_title': "Добавление заказа"})
                        return render(request, 'order_claim/add_edit_order.html', out)
                    else:
                        name_of_pr = 'select-product__number_' + id_of_pr
                        count_of_products = request.POST[name_of_pr]
                        price_of_pr = 'select-product__price_' + id_of_pr
                        price_of_products = request.POST[price_of_pr]
                        if not price_of_products:
                            price_of_products = 0
                        if int(count_of_products) > 0:
                            product = Products.objects.create(title=title_of_product, price=price_of_products)
                else:
                    name_of_pr = 'select-product__number_' + id_of_pr
                    count_of_products = request.POST[name_of_pr]
                    price_of_pr = 'select-product__price_' + id_of_pr
                    price_of_products = request.POST[price_of_pr]
                    try:
                        product = Products.objects.get(id=id_of_pr, is_deleted=0)
                        product.price = price_of_products
                        product.save(force_update=True)
                    except Exception:
                        price_of_products = 0
                if int(count_of_products) > 0:
                    is_claim_create = True
                    if new_claim_was_not_created:
                        new_claim_was_not_created = False
                        client.save(update_fields=["is_interested"])
                        new_claim = Orders.objects.create(order_date=datetime.now(), client=client, role=role,
                                              unique_number=unique_number, company=company, bill=bill,
                                              bill_status=bill_status, is_claim=is_claim,
                                              account_number=account_number, comment=comment, source=source,
                                              brought_sum=brought_sum)
                    new_order_product_link = Order_Product.objects.create(order=new_claim, product=product,
                                                                          order_date=datetime.now(),
                                                                          count_of_products=count_of_products,
                                                                          price=price_of_products)
                    client.save(update_fields=["is_interested"])
            if is_claim_create:
                if 'only-save' in form.data:
                    if displacement == 1:
                        get_params = '&'
                        get_params += get_request_param_as_string(request)
                        return HttpResponseRedirect('/claims/?displacement=1' + get_params)
                    else:
                        get_params = '?'
                        get_params += get_request_param_as_string(request)
                        return HttpResponseRedirect('/claims/' + get_params)
                else:
                    return HttpResponseRedirect('/uploads/order/?id=%s' % new_claim.id)
            else:
                ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=False)
                ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                                   'bill_status': bill_status, 'account_number': account_number,
                                   'comment': comment, 'brought_sum': brought_sum})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        product.count_of_products = count_of_products
                        price_of_pr = 'select-product__price_' + str(product.id)
                        price_of_products = request.POST[price_of_pr]
                        product.price = price_of_products
                    product.price_right_format = right_money_format(product.price)
                out.update({'error': 3})
                out.update({'order_form': form})
                ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                client_form = ClientRelatedForm()
                out.update({'form': client_form})
                out.update({'page_title': "Добавление заявки"})
        else:
            client = request.POST['client']
            source = None
            if 'source' in request.POST:
                source = request.POST['source']
            company = request.POST['company']
            comment = request.POST['comment']
            bill = request.POST['bill']
            brought_sum = request.POST['brought_sum']
            bill_status = request.POST['bill_status']
            account_number = request.POST['account_number']
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                               'bill_status': bill_status, 'account_number': account_number,
                               'comment': comment, 'brought_sum': brought_sum})
            form.products = Products.objects.filter(is_deleted=0)
            products_list = request.POST.getlist('products[]')
            for product in form.products:
                if str(product.id) in products_list:
                    name_of_pr = 'select-product__number_' + str(product.id)
                    count_of_products = request.POST[name_of_pr]
                    product.count_of_products = count_of_products
                    price_of_pr = 'select-product__price_' + str(product.id)
                    price_of_products = request.POST[price_of_pr]
                    product.price = price_of_products
                product.price_right_format = right_money_format(product.price)
            out.update({'error': 1})
            out.update({'order_form': form})
            ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_form = ClientRelatedForm()
            out.update({'form': client_form})
            out.update({'page_title': "Добавление заявки"})
    else:
        if 'copy' in request.GET:
            id_order = request.GET['copy']
            out.update({"error": 0})
            claim = Orders.objects.get(pk=id_order, is_deleted=0, is_claim=1)
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm({'company': claim.company, 'bill': claim.bill,
                               'bill_status': claim.bill_status, 'account_number': claim.account_number,
                               'comment': claim.comment, 'source': claim.source, 'brought_sum': claim.brought_sum})
            form.products = Products.objects.filter(is_deleted=0)
            order_products = Order_Product.objects.filter(order_id=id_order, is_deleted=0)
            products_list = []
            for pr in order_products:
                products_list.append(pr.product_id)
            for product in form.products:
                if product.id in products_list:
                    product.count_of_products = Order_Product.objects.get(product_id=product.id,
                                                                          order_id=id_order, is_deleted=0).count_of_products
                    product.price = Order_Product.objects.get(product_id=product.id,
                                                              order_id=id_order, is_deleted=0).price
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_form = ClientRelatedForm()
            out.update({'form': client_form})
            out.update({'page_title': "Добавление заявки"})
        elif 'client-id' in request.GET:
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_id = request.GET['client-id']
            client = Clients.objects.get(id=client_id, is_deleted=0)
            form = ClaimsForm({'client': client})
            form.products = Products.objects.filter(is_deleted=0)
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_form = ClientRelatedForm()
            out.update({'form': client_form})
            out.update({'client_id': client_id})
            out.update({'page_title': "Добавление заявки"})
        elif 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            claim = Orders.objects.get(pk=id_order, is_deleted=0, is_claim=1)
            if user_role == 0:
                ClaimsFormForAdmins.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
                ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                               required=False)
            else:
                ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
                ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            if user_role == 0:
                ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            else:
                ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            if user_role == 0:
                form = ClaimsFormForAdmins({'client': claim.client, 'company': claim.company, 'bill': claim.bill,
                               'bill_status': claim.bill_status, 'account_number': claim.account_number,
                               'comment': claim.comment, 'source': claim.source, 'role': claim.role,
                               'brought_sum': claim.brought_sum})
            else:
                form = ClaimsForm({'client': claim.client, 'company': claim.company, 'bill': claim.bill,
                               'bill_status': claim.bill_status, 'account_number': claim.account_number,
                               'comment': claim.comment, 'source': claim.source, 'brought_sum': claim.brought_sum})
            form.products = Products.objects.filter(is_deleted=0)
            ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_form = ClientRelatedForm()
            order_products = Order_Product.objects.filter(order_id=id_order, is_deleted=0)
            products_list = []
            for pr in order_products:
                products_list.append(pr.product_id)
            for product in form.products:
                if product.id in products_list:
                    product.count_of_products = Order_Product.objects.get(product_id=product.id,
                                                                          order_id=id_order, is_deleted=0).count_of_products
                    product.price = Order_Product.objects.get(product_id=product.id,
                                                              order_id=id_order, is_deleted=0).price
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            out.update({'form': client_form})
            out.update({'page_title': "Редактирование заявки"})
        else:
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm()
            form.products = Products.objects.filter(is_deleted=0)
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_form = ClientRelatedForm()
            out.update({'form': client_form})
            out.update({'page_title': "Добавление заявки"})
    organizations = []
    for organization in Clients.objects.all().order_by('organization'):
        if organization.organization != "":
            organizations.append(organization.organization)
    out.update({'organizations': organizations})
    return render(request, 'order_claim/add_edit_order.html', out)


def full_get_claims(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    out.update({'sources': Sources.objects.filter(is_deleted=0)})
    out.update({'roles': Roles.objects.filter(is_deleted=0).filter(Q(role=1) | Q(role=0)).all()})
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_id = request.user.id
    out.update({'user_id': user_id})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_CLAIM)
    sort = SORT_TYPE_FOR_CLAIM.get(sort_key, DEFAULT_SORT_TYPE_FOR_CLAIM)
    orders = Orders.objects.filter(is_deleted=0, is_claim=1, in_archive=0)
    if 'source' in request.GET:
        source = int(request.GET.get('source'))
        if source != -1:
            orders = orders.filter(source=source)
    if 'managers[]' in request.GET:
        managers = request.GET.getlist('managers[]')
        orders = orders.filter(role__in=managers)
        out.update({'managers': managers})
    try:
        orders = orders.order_by(sort)
    except TypeError:
        orders = orders.order_by(*sort)
    number = request.GET.get('length', DEFAULT_NUMBER_FOR_PAGE)
    orders_pages = Paginator(orders, number)
    page = request.GET.get('page')
    try:
        order_list = orders_pages.page(page)
    except PageNotAnInteger:
        order_list = orders_pages.page(1)
    except EmptyPage:
        order_list = orders_pages.page(orders_pages.num_pages)
    for order in order_list:
        order.related = order.related_orders.all()
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
        elif order.bill_status == 4:
            order.bill_status = 'Устно'
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
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                if order_file.file:
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    order.files.append(order_file)
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': "Заявки"})
    out.update({'claims': order_list})
    out.update({'count': orders.count()})
    return render(request, 'order_claim/get_claims.html', out)


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
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/claims/' + get_params)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))