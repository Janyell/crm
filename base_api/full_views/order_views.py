#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.shortcuts import render
from datetime import date
from base_api.constants import SORT_TYPE_FOR_ORDER, DEFAULT_SORT_TYPE_FOR_ORDER, DEFAULT_SORT_TYPE_FOR_ORDER_IN_ARCHIVE, \
    DEFAULT_NUMBER_FOR_PAGE
from base_api.full_views.helper import get_request_param_as_string
from base_api.form import *
from django.http import *
import random
import string


def full_add_edit_order(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    # хак, чтобы отсутствие этого поля не вызывало 500 (фронт пока не добавил это поле)
    # transport_campaign = None
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    out.update({'modal_title': 'Добавление клиента'})
    # флаг, указывающий на то что статус "Отгружено" поставлен, а даты отгрузки нет
    is_date_for_status_exist = True
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
        if 'pk' in request.POST:
            pk = request.POST['pk']
            order = Orders.objects.get(id=pk)
            files = []
            if Order_Files.objects.filter(order_id=order.id).all() is not None:
                for order_file in Order_Files.objects.filter(order_id=order.id).all():
                    if order_file.file is not None and order_file.file != '':
                        order_file.name = order_file.title
                        order_file.url = order_file.file.url
                        files.append(order_file)
            out.update({'files': files})
            source = request.POST['source']
            transport_campaign = None
            if 'transport_campaign' in request.POST:
                transport_campaign = request.POST['transport_campaign']
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
            shipped_date = None
            if request.POST['order_status'] != '':
                order_status = int(request.POST['order_status'])
            else:
                order_status = None
            # if 'shipped_date' in request.POST and \
            #     request.POST['shipped_date'] is not None and \
            #     request.POST['shipped_date'] != '':
            #     order_status = -1
            # if 'ready_date' in request.POST and \
            #     request.POST['ready_date'] is not None and \
            #     request.POST['ready_date'] != '':
            #     order_status = 2
            if order_status == -1:
                shipped_date = request.POST['shipped_date']
                if shipped_date is None or shipped_date == '':
                    is_date_for_status_exist = False
                    shipped_date = datetime.now()
                else:
                    shipped_date = datetime.strptime(shipped_date, '%Y-%m-%d').date()
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
            factory_comment = None
            if 'factory_comment' in request.POST:
                factory_comment = request.POST['factory_comment']
            city = request.POST['city']
            if city:
                city = Cities.objects.get(pk=city)
            else:
                city = None
            if 'newCity' in request.POST:
                newCity = request.POST['newCity']
                if newCity:
                    city = Cities.objects.create(name=newCity)
            try:
                brought_sum = int(request.POST['brought_sum'])
            except Exception:
                brought_sum = None
            account_number = request.POST['account_number']
            if 'role' in request.POST:
                role = request.POST['role']
            else:
                role = request.user.id

            if not city:
                out.update({"error": 101})
                if user_role == 0:
                    OrdersFormForAdmins.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    OrdersFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    OrdersFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                else:
                    OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                          required=False)
                if order.shipped_date is not None:
                    shipped_day_month = order.shipped_date
                else:
                    shipped_day_month = None
                if user_role == 0:
                    form = OrdersFormForAdmins({'client': request.POST['client_id_value'] , 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'shipped_date': shipped_day_month, 'role': role, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                else:
                    form = OrdersForm({'client': request.POST['client_id_value'] , 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        price_of_pr = 'select-product__price_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        price_of_products = request.POST[price_of_pr]
                        product.count_of_products = count_of_products
                        product.price = price_of_products
                    product.price_right_format = right_money_format(product.price)
                out.update({'order_form': form})
                out.update({'page_title': "Редактирование заказа"})
                return render(request, 'order_claim/add_edit_order.html', out)

            if request.POST['client_id_value'] != '' and is_date_for_status_exist:
                id_client = int(request.POST['client_id_value'])
                client = Clients.objects.get(id=id_client, is_deleted=0)
            else:
                if not is_date_for_status_exist:
                    # код ошибки когда нет даты отгрузки, а статус - есть
                    out.update({"error": 100})
                else:
                    out.update({"error": 1})
                if user_role == 0:
                    OrdersFormForAdmins.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    OrdersFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    OrdersFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                else:
                    OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                          required=False)
                # if user_role == 0:
                #     OrdersFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                # else:
                #     OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                if order.shipped_date is not None:
                    shipped_day_month = order.shipped_date
                else:
                    shipped_day_month = None
                if user_role == 0:
                    form = OrdersFormForAdmins({'client': request.POST['client_id_value'] , 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'shipped_date': shipped_day_month, 'role': role, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                else:
                    form = OrdersForm({'client': request.POST['client_id_value'] , 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        price_of_pr = 'select-product__price_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        price_of_products = request.POST[price_of_pr]
                        product.count_of_products = count_of_products
                        product.price = price_of_products
                    product.price_right_format = right_money_format(product.price)
                out.update({'order_form': form})
                out.update({'page_title': "Редактирование заказа"})
                return render(request, 'order_claim/add_edit_order.html', out)
            if request.POST['bill'] != '':
                try:
                    bill = int(request.POST['bill'])
                except Exception:
                    out.update({"error": 1})
                    if user_role == 0:
                        OrdersFormForAdmins.base_fields['company'] = CompanyModelChoiceField(
                                                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                        OrdersFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        OrdersFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                        OrdersFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                    else:
                        OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                        OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                        OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                    # if user_role == 0:
                    #     OrdersFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    # else:
                    #     OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    if order.shipped_date is not None:
                        shipped_day_month = order.shipped_date
                    else:
                        shipped_day_month = None
                    if user_role == 0:
                        form = OrdersFormForAdmins({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'payment_date': payment_date, 'order_status': order_status,
                                       'bill_status': bill_status, 'city': city, 'comment': comment,
                                       'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                       'shipped_date': shipped_day_month, 'role': role, 'brought_sum': brought_sum,
                                       'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                    else:
                        form = OrdersForm({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'payment_date': payment_date, 'order_status': order_status,
                                       'bill_status': bill_status, 'city': city, 'comment': comment,
                                       'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                       'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                                       'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
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
                    out.update({'page_title': "Редактирование заказа"})
                    return render(request, 'order_claim/add_edit_order.html', out)
            else:
                bill = None
            if bill_status == 2:
                brought_sum = bill
            new_order = Orders.objects.get(id=pk, is_deleted=0)
            is_comment_my = False
            if new_order.role_id == request.user.id:
                is_comment_my = True
            new_order.is_comment_my = is_comment_my
            new_order.client = client
            new_order.source = Sources.objects.get(id=source)
            new_order.transport_campaign = None
            if transport_campaign:
                new_order.transport_campaign = TransportCampaigns.objects.get(id=transport_campaign)
            new_order.company = company
            new_order.bill = bill
            if brought_sum:
                new_order.brought_sum = brought_sum
            new_order.payment_date = payment_date
            new_order.order_status = order_status
            if shipped_date is not None and shipped_date != '':
                new_order.order_status = -1
            if ready_date is not None and ready_date != '':
                order_status = 2
            new_order.bill_status = bill_status
            new_order.shipped_date = shipped_date
            new_order.ready_date = ready_date
            new_order.comment = comment
            new_order.factory_comment = factory_comment
            new_order.city = city
            new_order.role = Roles.objects.filter(id=role).first()
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
                        if user_role == 0:
                            OrdersFormForAdmins.base_fields['company'] = CompanyModelChoiceField(
                                                        queryset=Companies.objects.filter(is_deleted=0), required=False)
                            OrdersFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=False)
                            OrdersFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                            OrdersFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                        else:
                            OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                                        queryset=Companies.objects.filter(is_deleted=0), required=False)
                            OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                            OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                            OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                        # if user_role == 0:
                        #     OrdersFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        # else:
                        #     OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        if order.shipped_date is not None:
                            shipped_day_month = order.shipped_date
                        else:
                            shipped_day_month = None
                        if user_role == 0:
                            form = OrdersFormForAdmins({'client': client, 'company': company, 'bill': bill,
                                           'payment_date': payment_date, 'order_status': order_status,
                                           'bill_status': bill_status, 'city': city, 'comment': comment,
                                           'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                           'shipped_date': shipped_day_month, 'role': role, 'brought_sum': brought_sum,
                                           'factory_comment': factory_comment,
                                           'transport_campaign': transport_campaign})
                        else:
                            form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                                           'payment_date': payment_date, 'order_status': order_status,
                                           'bill_status': bill_status, 'city': city, 'comment': comment,
                                           'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                           'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                                           'factory_comment': factory_comment,
                                           'transport_campaign': transport_campaign})
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
                        out.update({'page_title': "Редактирование заказа"})
                        return render(request, 'order_claim/add_edit_order.html', out)
                    else:
                        name_of_pr = 'select-product__number_' + id_of_pr
                        count_of_products = request.POST[name_of_pr]
                        price_of_pr = 'select-product__price_' + id_of_pr
                        price_of_products = request.POST[price_of_pr]
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
                        order_product = Order_Product.objects.get(product_id=product.id, order_id=pk, is_deleted=0,
                                                                  price=price_of_products)
                        new_order_product_link = Order_Product(id=order_product.id, order=new_order, product=product,
                                                               order_date=datetime.now(),
                                                               count_of_products=count_of_products,
                                                               price=price_of_products)
                        new_order_product_link.save(force_update=True)
                    else:
                        new_order_product_link = Order_Product.objects.create(order=new_order,
                                                                              product=product,
                                                                              order_date=datetime.now(),
                                                                              count_of_products=count_of_products,
                                                                              price=price_of_products)
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            if new_order.in_archive == 1:
                return HttpResponseRedirect('/orders/archive/' + get_params)
            return HttpResponseRedirect('/orders/' + get_params)
        form.is_valid()
        if request.POST['client_id_value']:
            client = Clients.objects.get(pk=int(request.POST['client_id_value']))
        else:
            client = Clients.objects\
                .filter(is_deleted=0)\
                .filter(client_label_from_instance__icontains=request.POST['client']).first()
        if form and \
                (form.cleaned_data['order_status'] != -1 or \
                    form.cleaned_data['order_status'] == -1 and form.cleaned_data['shipped_date']) and \
                    client:
            source = form.cleaned_data['source']
            transport_campaign = form.cleaned_data['transport_campaign']
            unique_number = id_generator()
            company = form.cleaned_data['company']
            bill = form.cleaned_data['bill']
            payment_date = form.cleaned_data['payment_date']
            order_status = form.cleaned_data['order_status']
            bill_status = form.cleaned_data['bill_status']
            try:
                brought_sum = int(request.POST['brought_sum'])
            except Exception:
                brought_sum = None
            if bill_status == 2:
                brought_sum = bill
            shipped_date = None
            # if 'shipped_date' in request.POST and \
            #     request.POST['shipped_date'] is not None and \
            #     request.POST['shipped_date'] != '':
            #     order_status = -1
            # if 'ready_date' in request.POST and \
            #     request.POST['ready_date'] is not None and \
            #     request.POST['ready_date'] != '':
            #     order_status = 2
            if order_status == -1:
                shipped_date = form.cleaned_data['shipped_date']
                if shipped_date is None:
                    shipped_date = datetime.now()
            ready_date = form.cleaned_data['ready_date']
            comment = form.cleaned_data['comment']
            factory_comment = None
            if 'factory_comment' in form.data:
                factory_comment = form.cleaned_data['factory_comment']
            city = form.cleaned_data['city']
            if 'newCity' in form.cleaned_data:
                newCity = form.cleaned_data['newCity']
                if newCity:
                    city = Cities.objects.create(name=newCity)
            account_number = form.cleaned_data['account_number']
            role = Roles.objects.get(id=request.user.id, is_deleted=0)
            if not city:
                out.update({"error": 101})
                if user_role == 0:
                    OrdersFormForAdmins.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    OrdersFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    OrdersFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                else:
                    OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                    queryset=Companies.objects.filter(is_deleted=0), required=False)
                    OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                          required=False)
                if user_role == 0:
                    form = OrdersFormForAdmins({'client': request.POST['client_id_value'] , 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'role': role, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                else:
                    form = OrdersForm({'client': request.POST['client_id_value'] , 'company': company, 'bill': request.POST['bill'],
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
                form.products = Products.objects.filter(is_deleted=0)
                products_list = request.POST.getlist('products[]')
                for product in form.products:
                    if str(product.id) in products_list:
                        name_of_pr = 'select-product__number_' + str(product.id)
                        price_of_pr = 'select-product__price_' + str(product.id)
                        count_of_products = request.POST[name_of_pr]
                        price_of_products = request.POST[price_of_pr]
                        product.count_of_products = count_of_products
                        product.price = price_of_products
                    product.price_right_format = right_money_format(product.price)
                out.update({'order_form': form})
                out.update({'page_title': "Редактирование заказа"})
                return render(request, 'order_claim/add_edit_order.html', out)
            products_list = request.POST.getlist('products[]')
            is_order_create = False
            new_order_was_not_created = True
            for id_of_pr in products_list:
                if int(id_of_pr) < 0:
                    name_of_pr = 'select-product__title_' + id_of_pr
                    title_of_product = request.POST[name_of_pr]
                    if Products.objects.filter(title=title_of_product, is_deleted=0).count() != 0:
                        out.update({"error": 2})
                        OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                                        queryset=Companies.objects.filter(is_deleted=0), required=False)
                        OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        OrdersForm.base_fields['transport_campaign'] = SourceModelChoiceField(
                                                    queryset=TransportCaTransportCampaignsmpaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                        OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                        # OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        if shipped_date is not None:
                            shipped_day_month = shipped_date
                        else:
                            shipped_day_month = None
                        form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                                           'payment_date': payment_date, 'order_status': order_status,
                                           'bill_status': bill_status, 'city': city, 'comment': comment,
                                           'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                           'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                                           'factory_comment': factory_comment,
                                           'transport_campaign': transport_campaign})
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
                        out.update({'page_title': "Добавление заказа"})
                        return render(request, 'order_claim/add_edit_order.html', out)
                    else:
                        name_of_pr = 'select-product__number_' + id_of_pr
                        count_of_products = request.POST[name_of_pr]
                        price_of_pr = 'select-product__price_' + id_of_pr
                        price_of_products = request.POST[price_of_pr]
                        product.price = price_of_products
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
                    is_order_create = True
                    if new_order_was_not_created:
                        new_order_was_not_created = False
                        new_order = Orders.objects.create(order_date=datetime.now(), client=client, role=role, source=source,
                                              unique_number=unique_number, company=company, bill=bill,
                                              payment_date=payment_date, order_status=order_status, city=city,
                                              bill_status=bill_status, ready_date=ready_date, comment=comment,
                                              account_number=account_number, shipped_date=shipped_date,
                                              brought_sum=brought_sum,
                                              factory_comment=factory_comment, transport_campaign=transport_campaign)
                    new_order_product_link = Order_Product.objects.create(order=new_order, product=product,
                                                                          order_date=datetime.now(),
                                                                          count_of_products=count_of_products,
                                                                          price=price_of_products)
            if is_order_create:
                if 'only-save' in form.data:
                    get_params = '?'
                    get_params += get_request_param_as_string(request)
                    return HttpResponseRedirect('/orders/' + get_params)
                else:
                    get_params = '&'
                    get_params += get_request_param_as_string(request)
                    return HttpResponseRedirect('/uploads/order/?id=%s' % new_order.id + get_params)
            else:
                OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                                queryset=Companies.objects.filter(is_deleted=0), required=False)
                OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
                # OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                if shipped_date is not None:
                    shipped_day_month = shipped_date
                else:
                    shipped_day_month = None
                form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                                   'payment_date': payment_date, 'order_status': order_status,
                                   'bill_status': bill_status, 'city': city, 'comment': comment,
                                   'source': source, 'ready_date': ready_date, 'account_number': account_number,
                                   'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
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
                out.update({'error': 3})
                for product in form.products:
                    product.price_right_format = right_money_format(product.price)
                out.update({'order_form': form})
                out.update({'page_title': "Добавление заказа"})
        else:
            client = request.POST['client_id_value'] 
            source = None
            transport_campaign = None
            if 'source' in request.POST:
                source = request.POST['source']
            if 'transport_campaign' in request.POST:
                transport_campaign = request.POST['transport_campaign']
            company = request.POST['company']
            bill = request.POST['bill']
            brought_sum = request.POST['brought_sum']
            if 'role' in request.POST:
                role = request.POST['role']
            else:
                role = request.user.id
            payment_date = request.POST['payment_date']
            order_status = request.POST['order_status']
            # if 'shipped_date' in request.POST and \
            #     request.POST['shipped_date'] is not None and \
            #     request.POST['shipped_date'] != '':
            #     order_status = -1
            # if 'ready_date' in request.POST and \
            #     request.POST['ready_date'] is not None and \
            #     request.POST['ready_date'] != '':
            #     order_status = 2
            bill_status = request.POST['bill_status']
            if bill_status == 2:
                brought_sum = bill
            ready_date = request.POST['ready_date']
            shipped_date = request.POST['shipped_date']
            comment = request.POST['comment']
            factory_comment = None
            if 'factory_comment' in request.POST:
                factory_comment = request.POST['factory_comment']
            city = request.POST['city']
            if 'newCity' in request.POST:
                newCity = request.POST['newCity']
                if newCity:
                    city = Cities.objects.create(name=newCity)
            account_number = request.POST['account_number']
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                            queryset=Companies.objects.filter(is_deleted=0), required=False)
            OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
            OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
            # OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            if shipped_date:
                # shipped_day_month = shipped_date[:7]
                shipped_day_month = shipped_date
            else:
                shipped_day_month = None
            form = OrdersForm({'client': client, 'company': company, 'bill': bill,
                               'payment_date': payment_date, 'order_status': order_status,
                               'bill_status': bill_status, 'city': city, 'comment': comment,
                               'source': source, 'ready_date': ready_date, 'account_number': account_number,
                               'shipped_date': shipped_day_month, 'brought_sum': brought_sum,
                               'factory_comment': factory_comment, 'transport_campaign': transport_campaign})
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
            out.update({'error': 1})
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
    else:
        if 'copy' in request.GET:
            id_order = request.GET['copy']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0)
            client = order.client
            out.update({'client_id': client.id})
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                            queryset=Companies.objects.filter(is_deleted=0), required=False)
            OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
            OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
            # OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            if order.shipped_date is not None:
                shipped_day_month = order.shipped_date
            else:
                shipped_day_month = None
            form = OrdersForm({'company': order.company, 'bill': order.bill,
                               'payment_date': order.payment_date, 'order_status': order.order_status,
                               'bill_status': order.bill_status, 'city': order.city, 'comment': order.comment,
                               'source': order.source, 'ready_date': order.ready_date,
                               'account_number': order.account_number, 'shipped_date': shipped_day_month,
                               'brought_sum': order.brought_sum, 'factory_comment': order.factory_comment,
                               'transport_campaign': order.transport_campaign})
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
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
        elif 'client-id' in request.GET:
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                            queryset=Companies.objects.filter(is_deleted=0), required=False)
            OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
            OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
            # OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            client_id = request.GET['client-id']
            client = Clients.objects.get(id=client_id, is_deleted=0)
            form = OrdersForm({'client': client_label_from_instance(client)})
            out.update({'claim_client_id': client.id})
            form.products = Products.objects.filter(is_deleted=0)
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            out.update({'client_id': client_id})
            out.update({'page_title': "Добавление заказа"})
        elif 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0)
            client = order.client
            out.update({'client_id': client.id})
            out.update({'claim_client_id': client.id})
            if user_role == 0:
                OrdersFormForAdmins.base_fields['company'] = CompanyModelChoiceField(
                                            queryset=Companies.objects.filter(is_deleted=0), required=False)
                OrdersFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                OrdersFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                OrdersFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
            else:
                OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                            queryset=Companies.objects.filter(is_deleted=0), required=False)
                OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
            # if user_role == 0:
            #     OrdersFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            # else:
            #     OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            if order.shipped_date is not None:
                shipped_day_month = order.shipped_date
            else:
                shipped_day_month = None
            order_client = client_label_from_instance(order.client)
            if user_role == 0:
                form = OrdersFormForAdmins({'client': order_client, 'company': order.company, 'bill': order.bill,
                               'payment_date': order.payment_date, 'order_status': order.order_status,
                               'bill_status': order.bill_status, 'city': order.city, 'comment': order.comment,
                               'source': order.source, 'ready_date': order.ready_date,
                               'account_number': order.account_number, 'shipped_date': shipped_day_month,
                               'role': order.role, 'brought_sum': order.brought_sum,
                               'factory_comment': order.factory_comment,
                               'transport_campaign': order.transport_campaign})
            else:
                form = OrdersForm({'client': order_client, 'company': order.company, 'bill': order.bill,
                               'payment_date': order.payment_date, 'order_status': order.order_status,
                               'bill_status': order.bill_status, 'city': order.city, 'comment': order.comment,
                               'source': order.source, 'ready_date': order.ready_date,
                               'account_number': order.account_number, 'shipped_date': shipped_day_month,
                               'brought_sum': order.brought_sum, 'factory_comment': order.factory_comment,
                               'transport_campaign': order.transport_campaign})
            form.products = Products.objects.filter(is_deleted=0)
            order_products = Order_Product.objects.filter(order_id=id_order, is_deleted=0)
            products_list = []
            for pr in order_products:
                products_list.append(pr.product_id)
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
                if product.id in products_list:
                    product.count_of_products = Order_Product.objects.get(product_id=product.id,
                                                                          order_id=id_order, is_deleted=0).count_of_products
                    product.price = Order_Product.objects.get(product_id=product.id,
                                                                          order_id=id_order, is_deleted=0).price
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заказа"})
        else:
            OrdersForm.base_fields['company'] = CompanyModelChoiceField(
                                            queryset=Companies.objects.filter(is_deleted=0), required=False)
            OrdersForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            OrdersForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
            OrdersForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name"),
                                                                                   required=False)
            # OrdersForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = OrdersForm()
            form.products = Products.objects.filter(is_deleted=0)
            for product in form.products:
                product.price_right_format = right_money_format(product.price)
            out.update({'order_form': form})
            out.update({'page_title': "Добавление заказа"})
    organizations = []
    for organization in Clients.objects.all().order_by('organization'):
        if organization.organization != "":
            organizations.append(organization.organization.strip())
    out.update({'organizations': organizations})
    return render(request, 'order_claim/add_edit_order.html', out)


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
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    if order.in_archive:
        return HttpResponseRedirect('/orders/archive/' + get_params)
    return HttpResponseRedirect('/orders/' + get_params)


def full_get_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    out.update({'sources': Sources.objects.filter(is_deleted=0)})
    out.update({'transport_campaigns': TransportCampaigns.objects.filter(is_deleted=0)})
    out.update({'roles': Roles.objects.filter(is_deleted=0).filter(Q(role=1) | Q(role=0) | Q(role=3)).all()})
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
        out.update({'page': page})
        out.update({'length': length})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_ORDER)
    if Roles.objects.get(id=request.user.id).role == 2:
        sort_key = 'factory'
    sort = SORT_TYPE_FOR_ORDER.get(sort_key, DEFAULT_SORT_TYPE_FOR_ORDER)
    orders = Orders.objects.filter(is_deleted=0, is_claim=0)
    if 'source' in request.GET:
        source = int(request.GET.get('source'))
        if source != -1:
            orders = orders.filter(source=source)
    if 'managers[]' in request.GET:
        managers = request.GET.getlist('managers[]')
        orders = orders.filter(role__in=managers)
        out.update({'managers': managers})
    if 'client-id' in request.GET:
        client_id = request.GET['client-id']
        if Clients.objects.filter(id=client_id, is_deleted=0).count() != 1:
            out.update({'page_title': "Данного клиента не существует!"})
            return render(request, 'order_claim/get_orders.html', out)
        client = Clients.objects.get(id=client_id, is_deleted=0)
        try:
            orders = orders.filter(client=client).order_by(sort)
        except TypeError:
            orders = orders.filter(client=client).order_by(*sort)
        out.update({'page_title': "История заказов "})
        out.update({'client_id': client_id})
        if client.organization == '':
            client.organization_or_full_name = client.last_name + ' ' + client.name + ' ' + client.patronymic
        else:
            client.organization_or_full_name = client.organization
        out.update({'organization_or_full_name': client.organization_or_full_name})
        out.update({'client_id': client.id})
    else:
        try:
            orders = orders.filter(in_archive=0).order_by(sort)
        except TypeError:
            orders = orders.filter(in_archive=0).order_by(*sort)
        out.update({'page_title': "Заказы"})
    if Roles.objects.get(id=request.user.id).role != 2:
        number = request.GET.get('length', DEFAULT_NUMBER_FOR_PAGE)
        orders_pages = Paginator(orders, number)
        page = request.GET.get('page')
        try:
            order_list = orders_pages.page(page)
        except PageNotAnInteger:
            order_list = orders_pages.page(1)
        except EmptyPage:
            order_list = orders_pages.page(orders_pages.num_pages)
        ready_orders = None
    else:
        orders = orders.exclude(order_status=-1)
        ready_orders = orders.filter(order_status=2)
        orders = orders.exclude(order_status=2)
        order_list = orders.all()
        ready_order_list = ready_orders.all()
    for order in order_list:
        if order.client.organization == '':
            order.client.organization_or_full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        else:
            order.client.organization_or_full_name = order.client.organization
        order.client.full_name = ''
        order.client.email = ''
        order.client.person_phone = ''
        contact_faces = ContactFaces.objects.filter(organization=order.client.id, is_deleted=0).all()
        for contact_face in contact_faces:
            order.client.full_name = order.client.full_name + contact_face.last_name + ' ' \
                                 + contact_face.name + ' ' + contact_face.patronymic
            for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                if email.email:
                    if order.client.email:
                        order.client.email += ', '
                    order.client.email = order.client.email + email.email + ' (' + contact_face.last_name + ' ' \
                                         + contact_face.name + ' ' + contact_face.patronymic + ')'
            for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                if phone.phone:
                    if order.client.person_phone:
                        order.client.person_phone += ', '
                    order.client.person_phone = order.client.person_phone + phone.phone + ' (' + \
                                                contact_face.last_name + ' ' + contact_face.name + ' ' + \
                                                contact_face.patronymic + ')'
        prs = Order_Product.objects.filter(order_id=order.id, is_deleted=0)
        products_list = []
        for pr in prs:
            products_list.append(pr)
        order.products = products_list
        if order.order_status == 0:
            order.order_status = 'В производстве'
            if user_role == 2:
                order.order_status = 'Пр-во'
                if order.ready_date:
                    order.is_ready = 1
                    order.ready_date = date(order.ready_date.year, order.ready_date.month, order.ready_date.day)
        elif order.order_status == -1:
            order.order_status = 'Отгружен'
            if order.shipped_date is not None:
                order.is_shipped = 1
                order.shipped_date = date(order.shipped_date.year, order.shipped_date.month, order.shipped_date.day)
        elif order.order_status == 2:
            order.order_status = 'Готов'
        else:
            order.order_status = ''
        if order.bill is not None:
            order.bill_right_format = right_money_format(order.bill)
        order.brought_sum_right_format = 0
        order.debt_right_format = 0
        order.is_in_debt = False
        if order.bill_status == 2:
            order.is_full_pay = True
        else:
            order.is_full_pay = False
        if order.brought_sum is not None and order.bill is not None:
            if (order.bill - order.brought_sum) > 0:
                order.is_in_debt = True
            else:
                order.is_in_debt = False
            order.brought_sum_right_format = right_money_format(order.brought_sum)
            order.debt_right_format = right_money_format(int(order.bill) - int(order.brought_sum))
        if order.is_full_pay or order.bill_status == 3:
            order.is_in_debt = False
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                if order_file.file is not None and order_file.file != '':
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    order.files.append(order_file)
        if order.payment_date:
            order.payment_date = order.payment_date.date()
    if ready_orders:
        for order in ready_order_list:
            if order.client.organization == '':
                order.client.organization_or_full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
            else:
                order.client.organization_or_full_name = order.client.organization
            order.client.full_name = ''
            order.client.email = ''
            order.client.person_phone = ''
            contact_faces = ContactFaces.objects.filter(organization=order.client.id, is_deleted=0).all()
            for contact_face in contact_faces:
                order.client.full_name = order.client.full_name + contact_face.last_name + ' ' \
                                     + contact_face.name + ' ' + contact_face.patronymic
                for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                    if email.email:
                        if order.client.email:
                            order.client.email += ', '
                        order.client.email = order.client.email + email.email + ' (' + contact_face.last_name + ' ' \
                                             + contact_face.name + ' ' + contact_face.patronymic + ')'
                for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                    if phone.phone:
                        if order.client.person_phone:
                            order.client.person_phone += ', '
                        order.client.person_phone = order.client.person_phone + phone.phone + ' (' + \
                                                    contact_face.last_name + ' ' + contact_face.name + ' ' + \
                                                    contact_face.patronymic + ')'
            prs = Order_Product.objects.filter(order_id=order.id, is_deleted=0)
            products_list = []
            for pr in prs:
                products_list.append(pr)
            order.products = products_list
            if order.order_status == 0:
                order.order_status = 'В производстве'
                if user_role == 2:
                    order.order_status = 'Пр-во'
                    if order.ready_date:
                        order.is_ready = 1
                        order.ready_date = date(order.ready_date.year, order.ready_date.month, order.ready_date.day)
            elif order.order_status == -1:
                order.order_status = 'Отгружен'
                if order.shipped_date is not None:
                    order.is_shipped = 1
                    order.shipped_date = date(order.shipped_date.year, order.shipped_date.month, order.shipped_date.day)
            elif order.order_status == 2:
                order.order_status = 'Готов'
            else:
                order.order_status = ''
            if order.bill is not None:
                order.bill_right_format = right_money_format(order.bill)
            order.brought_sum_right_format = 0
            order.debt_right_format = 0
            order.is_in_debt = False
            if order.bill_status == 2:
                order.is_full_pay = True
            else:
                order.is_full_pay = False
            if order.brought_sum is not None and order.bill is not None:
                if (order.bill - order.brought_sum) > 0:
                    order.is_in_debt = True
                else:
                    order.is_in_debt = False
                order.brought_sum_right_format = right_money_format(order.brought_sum)
                order.debt_right_format = right_money_format(int(order.bill) - int(order.brought_sum))
            if order.is_full_pay or order.bill_status == 3:
                order.is_in_debt = False
            order.files = []
            if Order_Files.objects.filter(order_id=order.id).all() is not None:
                for order_file in Order_Files.objects.filter(order_id=order.id).all():
                    if order_file.file is not None and order_file.file != '':
                        order_file.name = order_file.title
                        order_file.url = order_file.file.url
                        order.files.append(order_file)
            if order.payment_date:
                order.payment_date = order.payment_date.date()
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'orders': order_list})
    out.update({'count': orders.count()})
    if ready_orders:
        out.update({'ready_orders': ready_order_list})
        out.update({'count': orders.count() + ready_orders.count()})
    # IN_PRODUCTION status = 0
    out.update({'count_in_production': orders.filter(order_status=0).count()})
    out.update({'now': datetime.now()})
    if Roles.objects.get(id=request.user.id).role == 2:
        return render(request, 'order_claim/get_orders_for_factory.html', out)
    return render(request, 'order_claim/get_orders.html', out)


def full_get_old_orders(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    out.update({'sources': Sources.objects.filter(is_deleted=0)})
    out.update({'transport_campaigns': TransportCampaigns.objects.filter(is_deleted=0)})
    out.update({'roles': Roles.objects.filter(is_deleted=0).filter(Q(role=1) | Q(role=0) | Q(role=3)).all()})
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
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_ORDER_IN_ARCHIVE)
    sort = SORT_TYPE_FOR_ORDER.get(sort_key, DEFAULT_SORT_TYPE_FOR_ORDER_IN_ARCHIVE)
    orders = Orders.objects.filter(is_deleted=0, is_claim=0, in_archive=1)
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
        if order.client.organization == '':
            order.client.organization_or_full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        else:
            order.client.organization_or_full_name = order.client.organization
        order.client.full_name = ''
        order.client.email = ''
        order.client.person_phone = ''
        contact_faces = ContactFaces.objects.filter(organization=order.client.id, is_deleted=0).all()
        for contact_face in contact_faces:
            order.client.full_name = order.client.full_name + ', ' + contact_face.last_name + ' ' \
                                 + contact_face.name + ' ' + contact_face.patronymic
            for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                if email.email:
                    if order.client.email:
                        order.client.email += ', '
                    order.client.email = order.client.email + email.email + ' (' + contact_face.last_name + ' ' \
                                         + contact_face.name + ' ' + contact_face.patronymic + ')'
            for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                if phone.phone:
                    if order.client.person_phone:
                        order.client.person_phone += ', '
                    order.client.person_phone = order.client.person_phone + phone.phone + ' (' + \
                                                contact_face.last_name + ' ' + contact_face.name + ' ' + \
                                                contact_face.patronymic + ')'
        prs = Order_Product.objects.filter(order_id=order.id, is_deleted=0)
        products_list = []
        for pr in prs:
            products_list.append(pr)
        order.products = products_list
        if order.order_status == 0:
            order.order_status = 'В производстве'
        elif order.order_status == -1:
            order.order_status = 'Отгружен'
            if order.shipped_date is not None:
                order.is_shipped = 1
                order.shipped_date = date(order.shipped_date.year, order.shipped_date.month, order.shipped_date.day)
        elif order.order_status == 2:
            order.order_status = 'Готов'
        else:
            order.order_status = ''
        if order.bill is not None:
            order.bill_right_format = right_money_format(order.bill)
        order.brought_sum_right_format = 0
        order.debt_right_format = 0
        order.is_in_debt = False
        if order.bill_status == 2:
            order.is_full_pay = True
        else:
            order.is_full_pay = False
        if order.brought_sum is not None and order.bill is not None:
            if (order.bill - order.brought_sum) > 0:
                order.is_in_debt = True
            else:
                order.is_in_debt = False
            order.brought_sum_right_format = right_money_format(order.brought_sum)
            order.debt_right_format = right_money_format(int(order.bill) - int(order.brought_sum))
        if order.is_full_pay or order.bill_status == 3:
            order.is_in_debt = False
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                if order_file.file is not None and order_file.file != '':
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    order.files.append(order_file)
    out.update({'page_title': "Архив заказов"})
    out.update({'orders': order_list})
    out.update({'count': orders.count()})
    return render(request, 'order_claim/get_orders.html', out)


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
            # if 'shipped_date' in request.POST and \
            #                 request.POST['shipped_date'] is not None and \
            #                 request.POST['shipped_date'] != '':
            #     order_status = -1
            # if 'ready_date' in request.POST and \
            #     request.POST['ready_date'] is not None and \
            #     request.POST['ready_date'] != '':
            #     order_status = 2
            if order_status == -1:
                shipped_date = request.POST['shipped_date']
                if shipped_date is None or shipped_date == '':
                    new_order.shipped_date = datetime.now()
                else:
                    new_order.shipped_date = datetime.strptime(shipped_date, '%Y-%m-%d').date()
            new_order.order_status = order_status
            new_order.ready_date = ready_date
            new_order.save(force_update=True)
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/orders/' + get_params)
        else:
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/orders' + get_params)
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
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/orders/' + get_params)
    return render(request, 'order_claim/edit_order_for_factory.html', out)


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
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/orders/' + get_params)


def full_delete_from_archive(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order = Orders.objects.get(pk=id, is_deleted=0)
    order.in_archive = 0
    order.save(update_fields=["in_archive"])
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    if 'client-id' in request.GET:
        return HttpResponseRedirect('/orders/' + get_params)
    return HttpResponseRedirect('/orders/archive/' + get_params)


def full_make_claim(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order = Orders.objects.get(pk=id, is_deleted=0)
    if str(request.user.username) != str(order.role) and Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    order.is_claim = 1
    order.save(update_fields=["is_claim"])
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/orders/' + get_params)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def right_money_format(bill):
    if bill != 0:
        orders_count_str = str(bill)
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
        return orders_count_str
    return ''