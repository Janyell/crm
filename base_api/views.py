#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, render_to_response
from datetime import datetime
import djangosphinx
from djangosphinx.apis.api275 import SPH_MATCH_EXTENDED
from api.settings import MEDIA_ROOT
from base_api.full_views.analyze_debtors import full_analyze_debtors
from base_api.full_views.attach import *
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from base_api.full_views.company_views import *
from base_api.full_views.role_views import *
from base_api.full_views.client_views import *
from base_api.full_views.order_views import *
from base_api.full_views.analyze_products import *
from base_api.full_views.analyze_managers import *
from base_api.full_views.analyze_sales_by_managers import *
from base_api.full_views.analyze_total_sales import *
from base_api.full_views.analyze_period import *
from base_api.full_views.product_views import *
from base_api.full_views.claim_views import *
# for excel
import openpyxl


def add_edit_role(request):
    return full_add_edit_role(request)


def delete_role(request):
    return full_delete_roles(request)


def get_roles(request):
    return full_get_roles(request)


def add_edit_company(request):
    return full_add_edit_company(request)


def delete_company(request):
    return full_delete_company(request)


def get_companies(request):
    return full_get_companies(request)


def add_edit_client(request):
    return full_add_edit_client(request)


def delete_client(request):
    return full_delete_clients(request)


def get_clients(request):
    return full_get_clients(request)


def add_edit_order(request):
    return full_add_edit_order(request)


def delete_order(request):
    return full_delete_order(request)


def get_orders(request):
    return full_get_orders(request)


def edit_order_for_factory(request):
    return full_edit_order_for_factory(request)


def analyst(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
        out.update({'page_title': "Аналитика"})
    return render(request, 'index.html', out)


def log_in(request):
    if not request.user.is_active:
        out = {}
        if request.method == 'POST':
            form = LoginForm(request.POST)
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if Roles.objects.get(id=request.user.id).role != 0:
                    return HttpResponseRedirect('/orders/')
                else:
                    return HttpResponseRedirect('/')
            else:
                out.update({"error": 1})
        else:
            form = LoginForm()
        out.update({'login_form': form})
        out.update({'page_title': "Авторизация"})
        return render(request, 'log_in.html', out)
    else:
        if Roles.objects.get(id=request.user.id).role != 0:
            return HttpResponseRedirect('/orders/')
        else:
            return HttpResponseRedirect('/')


def log_out(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    logout(request)
    return HttpResponseRedirect("/login/")


def page_not_found(request):
    out = {}
    try:
        user_role = Roles.objects.get(id=request.user.id).role
        out = {'user_role': user_role}
        out.update({'page_title': "Страница не найдена"})
        return render(request, 'page_not_found.html', out)
    except ObjectDoesNotExist:
        return HttpResponseRedirect("/login/")


def permission_deny(request):
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'page_title': "К сожалению, у вас нет доступа к данной странице"})
    return render(request, 'page_not_found.html', out)


def get_old_orders(request):
    return full_get_old_orders(request)


def add_in_archive(request):
    return full_add_in_archive(request)


def get_interested_clients(request):
    return full_get_interested_clients(request)


def analyze_products(request):
    return full_analyze_products(request)


def view_analyzed_product(request):
    return full_view_analyzed_product(request)


def analyze_managers(request):
    return full_analyze_managers(request)


def analyze_total_sales(request):
    return full_analyze_total_sales(request)


def analyze_sales_by_managers(request):
    return full_analyze_sales_by_managers(request)


def analyze_period(request):
    return full_analyze_period(request)


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % ('func', data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator


@json_response
def give_order_status(request):
    order_unic = request.GET['id']
    result = {}
    try:
        order = Orders.objects.get(unique_number=order_unic)
        result['order_status'] = order.order_status
        result['order_date'] = str(order.order_date)
        result['payment_date'] = str(order.payment_date)
        result['bill_status'] = order.bill_status
        result['ready_date'] = str(order.ready_date)
    except ObjectDoesNotExist:
        result['error'] = u'order_is_not_exist'
    return result


def get_products(request):
    return full_get_products(request)


def delete_product(request):
    return full_delete_product(request)


def edit_order_for_other_managers(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        if 'pk' in request.POST:
            pk = request.POST['pk']
            comment = request.POST['comment']
            new_order = Orders.objects.get(id=pk, is_deleted=0)
            is_comment_my = False
            if new_order.role_id == request.user.id:
                is_comment_my = True
            new_order.is_comment_my = is_comment_my
            new_order.comment = comment
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
            return HttpResponseRedirect('/orders/' + get_params)
    else:
        if 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0)
            form = OrdersForm({'comment': order.comment})
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заказа"})
        else:
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/orders/' + get_params)
    return render(request, 'edit_order_for_other_managers.html', out)


def edit_claim_for_other_managers(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    if request.method == 'POST':
        if 'pk' in request.POST:
            pk = request.POST['pk']
            comment = request.POST['comment']
            new_order = Orders.objects.get(id=pk, is_deleted=0, is_claim=1)
            new_order.comment = comment
            is_comment_my = False
            if new_order.role_id == request.user.id:
                is_comment_my = True
            new_order.is_comment_my = is_comment_my
            new_order.save(force_update=True)
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/claims/' + get_params)
        else:
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/claims/' + get_params)
    else:
        if 'id' in request.GET:
            id_order = request.GET['id']
            out.update({"error": 0})
            order = Orders.objects.get(pk=id_order, is_deleted=0, is_claim=1)
            form = OrdersForm({'comment': order.comment})
            out.update({'order_form': form})
            out.update({'page_title': "Редактирование заявки"})
        else:
            get_params = '?'
            if 'search' in request.GET:
                search = request.GET.get('search')
                get_params += 'search=' + unicode(search)
                return HttpResponseRedirect('/search/' + get_params)
            get_params += get_request_param_as_string(request)
            return HttpResponseRedirect('/claims/' + get_params)
    return render(request, 'edit_order_for_other_managers.html', out)


def get_claims(request):
    return full_get_claims(request)


def add_edit_claim(request):
    return full_add_edit_claim(request)


def delete_claim(request):
    return full_delete_claim(request)


def delete_from_archive(request):
    return full_delete_from_archive(request)


def upload_order_files(request):
    return upload_order_file(request)


def delete_order_files(request):
    return delete_order_file(request)


def upload_client_files(request):
    return upload_client_file(request)


def delete_client_files(request):
    return delete_client_file(request)


def fix_bd_org_type(request):
    clients = Clients.objects.all()
    for client in clients:
        if u'ИП' in client.organization:
            client.organization_type = u'ИП'
            client.organization = client.organization[3:]
        elif u'ООО' in client.organization:
            client.organization_type = u'ООО'
            client.organization = client.organization[4:]
        elif u'ЗАО' in client.organization:
            client.organization_type = u'ЗАО'
            client.organization = client.organization[4:]
        elif u'ОАО' in client.organization:
            client.organization_type = u'ОАО'
            client.organization = client.organization[4:]
        elif u'НКО' in client.organization:
            client.organization_type = u'НКО'
            client.organization = client.organization[4:]
        elif u'ТСЖ' in client.organization:
            client.organization_type = u'ТСЖ'
            client.organization = client.organization[4:]
        elif u'ОП' in client.organization:
            client.organization_type = u'ОП'
            client.organization = client.organization[3:]
        client.save(update_fields=["organization", "organization_type"])
    return HttpResponseRedirect('/clients/interested/')


def made_excel(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    filename = MEDIA_ROOT + '/' + str(Order_Files.objects.get(id=1).file)
    wb = openpyxl.load_workbook(filename=filename)
    sheet = wb['test']
    clients = Clients.objects.filter(is_deleted=0).all()
    row_index = 1
    sheet.cell(row=row_index, column=1).value = "Email"
    sheet.cell(row=row_index, column=2).value = "Организация"
    sheet.cell(row=row_index, column=3).value = "Контактное лицо"
    for client in clients:
        row_index += 1
        column_index = 1
        sheet.cell(row=row_index, column=column_index).value = client.email
        column_index += 1
        if client.organization_type == "" or client.organization_type is None:
            sheet.cell(row=row_index, column=column_index).value = client.organization
        else:
            sheet.cell(row=row_index, column=column_index).value = client.organization + ', ' + client.organization_type
        column_index += 1
        sheet.cell(row=row_index, column=column_index).value = client.last_name + ' ' + client.name + ' ' + \
                                                               client.patronymic
    # сохраняем данные
    wb.save(filename)
    return HttpResponseRedirect(Order_Files.objects.get(id=1).file.url)


def analyze_debtors(request):
    return full_analyze_debtors(request)


def edit_product(request):
    return full_edit_product(request)


def get_documents(request):
    return render(request, 'get_documents.html')


def search(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_role = Roles.objects.get(id=request.user.id).role
    out.update({'user_role': user_role})
    out.update({'user': Roles.objects.get(id=request.user.id)})
    if 'search' in request.GET:
        search_word = request.GET['search'] + '*'
    else:
        search_word = u'*'
    order_list = list(Orders.search.query(search_word).filter(is_deleted=0, is_claim=0, in_archive=0))
    all_clients = list(Clients.search.query(search_word))
    orders_from_fk = []
    for client in all_clients:
        for order in Orders.objects.filter(client=client.id, is_deleted=0, is_claim=0, in_archive=0).all():
            orders_from_fk.append(order)
    all_companies = list(Companies.search.query(search_word))
    for company in all_companies:
        for order in Orders.objects.filter(company=company.id, is_deleted=0, is_claim=0, in_archive=0).all():
            orders_from_fk.append(order)
    order_list += orders_from_fk
    for order in order_list:
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

    archive_order_list = list(Orders.search.query(search_word).filter(is_deleted=0, is_claim=0, in_archive=1))
    all_clients = list(Clients.search.query(search_word))
    orders_from_fk = []
    for client in all_clients:
        for order in Orders.objects.filter(client=client.id, is_deleted=0, is_claim=0, in_archive=1).all():
            orders_from_fk.append(order)
    all_companies = list(Companies.search.query(search_word))
    for company in all_companies:
        for order in Orders.objects.filter(company=company.id, is_deleted=0, is_claim=0, in_archive=1).all():
            orders_from_fk.append(order)
    archive_order_list += orders_from_fk
    for order in archive_order_list:
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
        if order.is_full_pay:
            order.is_in_debt = False
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                if order_file.file is not None and order_file.file != '':
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    order.files.append(order_file)

    claim_list = list(Orders.search.query(search_word).filter(is_deleted=0, is_claim=1, in_archive=0))
    all_clients = list(Clients.search.query(search_word))
    orders_from_fk = []
    for client in all_clients:
        for order in Orders.objects.filter(client=client.id, is_deleted=0, is_claim=1, in_archive=0).all():
            orders_from_fk.append(order)
    all_companies = list(Companies.search.query(search_word))
    for company in all_companies:
        for order in Orders.objects.filter(company=company.id, is_deleted=0, is_claim=1, in_archive=0).all():
            orders_from_fk.append(order)
    claim_list += orders_from_fk
    for order in claim_list:
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
        order.files = []
        if Order_Files.objects.filter(order_id=order.id).all() is not None:
            for order_file in Order_Files.objects.filter(order_id=order.id).all():
                if order_file.file:
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    order.files.append(order_file)

    client_list = list(Clients.search.query(search_word).filter(is_deleted=0, is_interested=0))
    for c in client_list:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
        c.files = []
        if Client_Files.objects.filter(client_id=c.id).all() is not None:
            for client_file in Client_Files.objects.filter(client_id=c.id).all():
                if client_file.file is not None and client_file.file != '':
                    client_file.name = client_file.title
                    client_file.url = client_file.file.url
                    c.files.append(client_file)

    interested_client_list = list(Clients.search.query(search_word).filter(is_deleted=0, is_interested=1))
    for c in interested_client_list:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
        c.files = []
        if Client_Files.objects.filter(client_id=c.id).all() is not None:
            for client_file in Client_Files.objects.filter(client_id=c.id).all():
                if client_file.file is not None and client_file.file != '':
                    client_file.name = client_file.title
                    client_file.url = client_file.file.url
                    c.files.append(client_file)
    if client_list or interested_client_list or order_list or archive_order_list or claim_list:
        out.update({'search_results': 1})
    out.update({'page_title': "Клиенты"})
    out.update({'clients': client_list})
    out.update({'interested_clients': interested_client_list})
    out.update({'orders': order_list})
    out.update({'old_orders': archive_order_list})
    out.update({'claims': claim_list})
    return render(request, 'search.html', out)


def fix_file_nodes(request):
    files = Order_Files.objects.all()
    for file in files:
        if file.title != 'Emails_of_clients.xlsx':
            save_file_in_node(file)
    files = Client_Files.objects.all()
    for file in files:
        save_file_in_node(file)
    return HttpResponseRedirect('/')