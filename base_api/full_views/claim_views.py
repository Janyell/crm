#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.forms.models import modelform_factory
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
    no_our_product_id = Products.objects.filter(title='Другое')
    if not no_our_product_id:
        no_our_product_id = -1
    else:
        no_our_product_id = no_our_product_id.first().id
    out.update({'no_our_product_id': no_our_product_id})
    TaskForm.base_fields['type'] = TaskTypeChoiceField(queryset=TaskTypes.objects.filter(is_deleted=0))
    out.update({'task_form': TaskForm(initial={'is_important': False})})
    if request.method == 'POST':
        form = ClaimsForm(request.POST)
        if 'client-id' in request.GET:
            client_id = request.GET['client-id']
            out.update({'client_id': client_id})
        if 'pk' in request.POST:
            pk = request.POST['pk']
            claim = Orders.objects.get(id=pk)
            source = request.POST['source']
            transport_campaign = request.POST['transport_campaign']
            comment = request.POST['comment']
            factory_comment = None
            if 'factory_comment' in request.POST:
                factory_comment = request.POST['factory_comment']
            try:
                brought_sum = int(request.POST['brought_sum'])
            except Exception:
                brought_sum = None
            if request.POST['payment_date'] != '':
                payment_date = request.POST['payment_date']
                payment_date = datetime.strptime(payment_date, '%Y-%m-%d %H:%M:%S')
            else:
                payment_date = None
            city = request.POST['city']
            if city:
                city = Cities.objects.get(pk=city)
            else:
                city = None
            if 'newCity' in request.POST:
                newCity = request.POST['newCity']
                if newCity:
                    city = Cities.objects.create(name=newCity)
            if 'company' in request.POST and request.POST['company'] != '':
                id_company = int(request.POST['company'])
                company = Companies.objects.get(id=id_company, is_deleted=0)
            else:
                company = None
            if request.POST['bill_status'] != '':
                bill_status = int(request.POST['bill_status'])
            else:
                bill_status = None
            order_status = None
            if bill_status == 1 or bill_status == 2:
                order_status = 0
            if request.POST['ready_date'] != '':
                ready_date = request.POST['ready_date']
                ready_date = datetime.strptime(ready_date, '%Y-%m-%d %H:%M:%S')
            else:
                ready_date = None
            account_number = request.POST['account_number']
            # if account_number:
            #     bill_status = 0
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
                                                                            required=True)
                    ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    ClaimsFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                else:
                    ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=True)
                    ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                    ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                    ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                if user_role == 0:
                    ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                else:
                    ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                if user_role == 0:
                    form = ClaimsFormForAdmins({'client': request.POST['client'], 'company': company, 'bill': request.POST['bill'],
                                   'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                   'comment': comment, 'role': role, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign,
                                   'ready_date': ready_date, 'city': city, 'payment_date': payment_date,
                                   'order_status': order_status})
                else:
                    form = ClaimsForm({'client': request.POST['client'], 'company': company, 'bill': request.POST['bill'],
                                   'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                   'comment': comment, 'brought_sum': brought_sum, 'factory_comment': factory_comment,
                                   'transport_campaign': transport_campaign, 'ready_date': ready_date, 'city': city,
                                   'payment_date': payment_date, 'order_status': order_status})
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
                                                                                required=True)
                        ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        ClaimsFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                        ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                    else:
                        ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                required=True)
                        ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                        ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                    if user_role == 0:
                        ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    else:
                        ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                    if user_role == 0:
                        form = ClaimsFormForAdmins({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                       'comment': comment, 'role': role, 'brought_sum': brought_sum,
                                       'factory_comment': factory_comment, 'transport_campaign': transport_campaign,
                                       'ready_date': ready_date, 'city': city, 'payment_date': payment_date,
                                       'order_status': order_status})
                    else:
                        form = ClaimsForm({'client': client, 'company': company, 'bill': request.POST['bill'],
                                       'bill_status': bill_status, 'account_number': account_number, 'source': source,
                                       'comment': comment, 'brought_sum': brought_sum,
                                       'factory_comment': factory_comment, 'transport_campaign': transport_campaign,
                                       'ready_date': ready_date, 'city': city, 'payment_date': payment_date,
                                       'order_status': order_status})
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
            new_claim.transport_campaign = None
            if transport_campaign:
                new_claim.transport_campaign = TransportCampaigns.objects.get(id=transport_campaign)
            new_claim.company = company
            new_claim.comment = comment
            new_claim.factory_comment = factory_comment
            new_claim.city = city
            new_claim.bill = bill
            new_claim.ready_date = ready_date
            new_claim.payment_date = payment_date
            new_claim.brought_sum = brought_sum
            new_claim.bill_status = bill_status
            new_claim.role = Roles.objects.filter(id=role).first()
            displacement = 0
            if bill_status == 1 or bill_status == 2:
                new_claim.is_claim = 0
                new_claim.became_claim_date = datetime.now()
                displacement = 1
                client.is_interested = 0
                new_claim.order_status = 0
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
                                                                                    required=True)
                            ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                            ClaimsFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                            ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                        else:
                            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                                    required=True)
                            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                            ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                        if user_role == 0:
                            ClaimsFormForAdmins.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        else:
                            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        if user_role == 0:
                            form = ClaimsFormForAdmins({'client': client, 'company': company, 'bill': bill, 'source': source,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment, 'role': role, 'brought_sum': brought_sum,
                                           'factory_comment': factory_comment,
                                           'transport_campaign': transport_campaign, 'ready_date': ready_date,
                                           'city': city, 'payment_date': payment_date, 'order_status': order_status})
                        else:
                            form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment, 'brought_sum': brought_sum,
                                           'factory_comment': factory_comment,
                                           'transport_campaign': transport_campaign, 'ready_date': ready_date,
                                           'city': city, 'payment_date': payment_date, 'order_status': order_status})
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
            if 'items[]' in request.POST:
                tasks_list = int(request.POST.get('items[]')) * -1
                for task_id in range(1, tasks_list+1):
                    task_id = str(task_id)
                    task_comment = request.POST.get('task_comment', '')
                    # task_comment = request.POST['task_comment_-' + task_id]
                    task_type_id = request.POST['type_-' + task_id]
                    if task_type_id:
                        task_type = TaskTypes.objects.get(id=task_type_id)
                        task_date = request.POST.get('date', datetime.now())
                        # task_date = request.POST['date_-' + task_id]
                        task_date = datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S')
                        task_is_important = False
                        if 'is_important_-' + task_id in request.POST:
                            task_is_important = True
                        task = Tasks.objects.create(comment=task_comment, type=task_type, date=task_date,
                                                    is_important=task_is_important, order=new_claim,
                                                    role=Roles.objects.get(id=request.user.id))
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
            transport_campaign = form.cleaned_data['transport_campaign']
            role = Roles.objects.get(id=request.user.id, is_deleted=0)
            unique_number = id_generator()
            company = form.cleaned_data['company']
            comment = form.cleaned_data['comment']
            factory_comment = None
            if 'factory_comment' in form.data:
                factory_comment = form.cleaned_data['factory_comment']
            city = None
            if 'city' in form.data:
                city = form.cleaned_data['city']
                if 'newCity' in form.cleaned_data:
                    newCity = form.cleaned_data['newCity']
                    if newCity:
                        city = Cities.objects.create(name=newCity)
            ready_date = None
            if 'ready_date' in form.data:
                if form.cleaned_data['ready_date'] != '' and form.cleaned_data['ready_date']:
                    ready_date = form.cleaned_data['ready_date']
                else:
                    ready_date = None
            payment_date = None
            if 'payment_date' in form.data:
                payment_date = form.cleaned_data['payment_date']
            bill = form.cleaned_data['bill']
            try:
                brought_sum = int(request.POST['brought_sum'])
            except Exception:
                brought_sum = None
            bill_status = form.cleaned_data['bill_status']
            displacement = 0
            order_status = None
            became_claim_date = None
            if bill_status == 1 or bill_status == 2:
                is_claim = 0
                became_claim_date = datetime.now()
                client.is_interested = 0
                displacement = 1
                order_status = 0
                if bill_status == 2:
                    brought_sum = bill
            else:
                is_claim = 1
            account_number = form.cleaned_data['account_number']
            # if account_number:
            #     bill_status = 0
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
                                                                                    required=True)
                        ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                        ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                        ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                        ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                        form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                                           'bill_status': bill_status, 'account_number': account_number,
                                           'comment': comment, 'brought_sum': brought_sum,
                                           'factory_comment': factory_comment,
                                           'transport_campaign': transport_campaign, 'ready_date': ready_date,
                                           'city': city, 'payment_date': payment_date, 'order_status': order_status})
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
                                              brought_sum=brought_sum, factory_comment=factory_comment,
                                              transport_campaign=transport_campaign, ready_date=ready_date, city=city,
                                              payment_date=payment_date, order_status=order_status,
                                              became_claim_date=became_claim_date)
                    new_order_product_link = Order_Product.objects.create(order=new_claim, product=product,
                                                                          order_date=datetime.now(),
                                                                          count_of_products=count_of_products,
                                                                          price=price_of_products)
                    client.save(update_fields=["is_interested"])
            if 'items[]' in request.POST:
                tasks_list = int(request.POST.get('items[]')) * -1
                for task_id in range(1, tasks_list+1):
                    task_id = str(task_id)
                    task_comment = request.POST.get('task_comment', '')
                    # task_comment = request.POST['task_comment_-' + task_id]
                    task_type_id = request.POST['type_-' + task_id]
                    if task_type_id:
                        task_type = TaskTypes.objects.get(id=task_type_id)
                        task_date = request.POST.get('date', datetime.now())
                        # task_date = request.POST['date_-' + task_id]
                        task_date = datetime.strptime(task_date, '%Y-%m-%d %H:%M:%S')
                        task_is_important = False
                        if 'is_important_-' + task_id in request.POST:
                            task_is_important = True
                        task = Tasks.objects.create(comment=task_comment, type=task_type, date=task_date,
                                                    is_important=task_is_important, order=new_claim,
                                                    role=Roles.objects.get(id=request.user.id))
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
                elif 'save-and-generate-kp' in form.data:
                    get_params = '&'
                    if 'set-via-kp' in form.data:
                        get_params += 'set_via_kp&'
                    get_params += get_request_param_as_string(request)
                    return HttpResponseRedirect('/claims/kp/edit/?id=%s' % new_claim.id + get_params)
                elif 'save-and-bind' in form.data:
                    get_params = '&'
                    get_params += get_request_param_as_string(request)
                    return HttpResponseRedirect('/related/claim/?id=%s' % new_claim.id + get_params)
                else:
                    return HttpResponseRedirect('/uploads/order/?id=%s' % new_claim.id)
            else:
                ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                            required=True)
                ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
                ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
                form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                                   'bill_status': bill_status, 'account_number': account_number,
                                   'comment': comment, 'brought_sum': brought_sum,
                                   'factory_comment': factory_comment, 'transport_campaign': transport_campaign,
                                   'ready_date': ready_date, 'city': city, 'payment_date': payment_date,
                                   'order_status': order_status})
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
            transport_campaign = None
            if 'source' in request.POST:
                source = request.POST['source']
            if 'transport_campaign' in request.POST:
                transport_campaign = request.POST['transport_campaign']
            company = None
            if 'company' in request.POST:
                company = request.POST['company']
            comment = request.POST['comment']
            factory_comment = None
            if 'factory_comment' in request.POST:
                factory_comment = request.POST['factory_comment']
            city = None
            if 'city' in request.POST:
                city = request.POST['city']
                if city:
                    city = Cities.objects.get(pk=city)
                if 'newCity' in request.POST:
                    newCity = request.POST['newCity']
                    if newCity:
                        city = Cities.objects.create(name=newCity)
            payment_date = None
            if 'payment_date' in request.POST:
                if request.POST['payment_date'] != '':
                    payment_date = request.POST['payment_date']
                    payment_date = datetime.strptime(payment_date, '%Y-%m-%d %H:%M:%S')
            bill = request.POST['bill']
            brought_sum = request.POST['brought_sum']
            bill_status = None
            if 'bill_status' in request.POST:
                bill_status = request.POST['bill_status']
            order_status = None
            if bill_status == 1 or bill_status == 2:
                order_status = 0
                if bill_status == 2:
                    brought_sum = bill
            account_number = request.POST['account_number']
            if 'ready_date' in request.POST and request.POST['ready_date'] != '':
                ready_date = request.POST['ready_date']
                ready_date = datetime.strptime(ready_date, '%Y-%m-%d %H:%M:%S')
            else:
                ready_date = None
            # if account_number:
            #     bill_status = 0
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm({'client': client, 'company': company, 'bill': bill, 'source': source,
                               'bill_status': bill_status, 'account_number': account_number,
                               'comment': comment, 'brought_sum': brought_sum,
                               'factory_comment': factory_comment, 'transport_campaign': transport_campaign,
                               'ready_date': ready_date, 'city': city, 'payment_date': payment_date,
                               'order_status': order_status})
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
        CloseClaimForm.base_fields['reason'] = CloseReasonsModelChoiceField(queryset=CloseReasons.objects.filter(
                                                                                    is_deleted=0),
                                                                           required=True)
        CloseClaimForm.base_fields['task_form'] = TaskForm(initial={'is_important': False})
        close_claim_form = CloseClaimForm()
        out.update({'close_claim_form': close_claim_form})
        out.update({'close_claim_form_task_form': TaskForm(initial={'is_important': False})})
        if 'copy' in request.GET:
            id_order = request.GET['copy']
            out.update({"error": 0})
            claim = Orders.objects.get(pk=id_order, is_deleted=0, is_claim=1)
            ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
            ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
            ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
            ClaimsForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                                   required=False)
            ClaimsForm.base_fields['client'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
            form = ClaimsForm({'company': claim.company, 'bill': claim.bill,
                               'bill_status': claim.bill_status, 'account_number': claim.account_number,
                               'comment': claim.comment, 'source': claim.source, 'brought_sum': claim.brought_sum,
                               'factory_comment': claim.factory_comment, 'transport_campaign': claim.transport_campaign,
                               'ready_date': claim.ready_date, 'city': claim.city, 'payment_date': claim.payment_date,
                               'order_status': claim.order_status})
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
            ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
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
            if claim.bill_status == 6:
                out.update({'is_closed': True})
            if user_role == 0:
                ClaimsFormForAdmins.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
                ClaimsFormForAdmins.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                ClaimsFormForAdmins.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
                ClaimsFormForAdmins.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects,
                                                                               required=False)
            else:
                ClaimsForm.base_fields['company'] = CompanyModelChoiceField(queryset=Companies.objects.filter(is_deleted=0),
                                                                        required=False)
                ClaimsForm.base_fields['source'] = SourceModelChoiceField(
                                                    queryset=Sources.objects.filter(is_active=1, is_deleted=0), required=True)
                ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
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
                               'brought_sum': claim.brought_sum, 'factory_comment': claim.factory_comment,
                               'transport_campaign': claim.transport_campaign, 'ready_date': claim.ready_date,
                               'city': claim.city, 'order_status': claim.order_status})
            else:
                form = ClaimsForm({'client': claim.client, 'company': claim.company, 'bill': claim.bill,
                               'bill_status': claim.bill_status, 'account_number': claim.account_number,
                               'comment': claim.comment, 'source': claim.source, 'brought_sum': claim.brought_sum,
                               'factory_comment': claim.factory_comment,
                               'transport_campaign': claim.transport_campaign, 'ready_date': claim.ready_date,
                               'city': claim.city, 'payment_date': claim.payment_date,
                               'order_status': claim.order_status})
            form.products = Products.objects.filter(is_deleted=0)
            TaskForm.base_fields['type'] = TaskTypeChoiceField(queryset=TaskTypes.objects.filter(is_active=1,
                                                                                                 is_deleted=0),
                                                               required=False)
            form.task = TaskForm(initial={'is_important': False})
            # print modelform_factory(Tasks, form=TaskForm)
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
            ClaimsForm.base_fields['transport_campaign'] = TransportCampaignsModelChoiceField(
                                                    queryset=TransportCampaigns.objects.filter(is_active=1, is_deleted=0), required=False)
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
            organizations.append(organization.organization.strip())
    out.update({'organizations': organizations})
    return render(request, 'order_claim/add_edit_order.html', out)


def full_get_claims(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    out.update({'sources': Sources.objects.filter(is_deleted=0)})
    out.update({'roles': Roles.objects.filter(is_deleted=0).filter(Q(role=1) | Q(role=0) | Q(role=3)).all()})
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
        elif order.bill_status == 5:
            order.bill_status = 'Подбор'
        elif order.bill_status == 6:
            order.bill_status = 'ЗАКРЫТА'
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
        order.reason = CloseClaims.objects.filter(order=order).first()
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


def full_bind_claims(request):
    out = {}
    out.update({'page_title': 'Связывание заявок'})
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    out.update({'user_role': Roles.objects.get(id=request.user.id).role})
    if 'id' in request.GET:
        order_id = request.GET['id']
        is_claim = int(Orders.objects.get(id=order_id).is_claim)
        out.update({'is_claim': is_claim})
    else:
        return HttpResponseRedirect('/oops/')
    ClientRelatedForm.base_fields['client_related_with'] = ClientModelChoiceField(queryset=Clients.objects.filter(is_deleted=0).extra(select={'org_or_name': "SELECT CASE WHEN organization = '' THEN CONCAT(last_name, name, patronymic) ELSE organization END"}, order_by=["org_or_name"]))
    client_form = ClientRelatedForm()
    out.update({'form': client_form})
    return render(request, "order_claim/related_claims.html", out)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))