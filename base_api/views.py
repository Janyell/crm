#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout

# add_edit_role {
#     page_title
#     role_form
# }
def add_edit_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']
            surname = form.cleaned_data['surname']
            name = form.cleaned_data['name']
            patronymic = form.cleaned_data['patronymic']

            new_author = Roles.objects.create(username=username,
                                              is_staff=0, is_active=1, date_joined=datetime.now(),
                                              role=role, surname=surname, name=name, patronymic=patronymic)
            new_author.set_password(password)
            new_author.save()
            return HttpResponseRedirect('/')
    else:
        form = RoleForm()
    out = {}
    out.update({'role_form': form})
    out.update({'page_title': "Добавление роли"})
    return render(request, "add_edit_role.html", out)


def get_roles(request):
    roles = Roles.objects.filter(is_deleted=0)
    for r in roles:
        r.full_name = r.surname + ' ' + r.name + ' ' + r.patronymic
    out = {}
    out.update({'page_title': "Роли"})
    out.update({'roles': roles})
    return render(request, 'get_roles.html', out)


def add_edit_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            last_name = form.cleaned_data['last_name']
            name = form.cleaned_data['name']
            patronymic = form.cleaned_data['patronymic']

            new_company = Companies.objects.create(title=title, last_name=last_name, name=name, patronymic=patronymic)
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
    else:
        # сделать выбор - если есть id в параметрах, отрисовывать поля, если нет - пустую форму
        form = CompanyForm()
    out = {}
    out.update({'company_form': form})
    out.update({'page_title': "Добавление компании"})
    return render(request, 'add_edit_company.html', out)


def get_companies(request):
    companies = Companies.objects.filter(is_deleted=0)
    for c in companies:
        c.full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out = {}
    out.update({'page_title': "Компании"})
    out.update({'companies': companies})
    return render(request, 'get_companies.html', out)


def add_edit_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            organization = form.cleaned_data['organization']
            last_name = form.cleaned_data['last_name']
            name = form.cleaned_data['name']
            patronymic = form.cleaned_data['patronymic']
            person_phone = form.cleaned_data['person_phone']
            organization_phone = form.cleaned_data['organization_phone']
            email = form.cleaned_data['email']

            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                patronymic=patronymic, person_phone=person_phone,
                                                organization_phone=organization_phone, email=email)
            if 'save-and-add-order' in form.data:
                return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
            elif 'only-save' in form.data:
                return HttpResponseRedirect('/clients/')
            return HttpResponseRedirect('/')
        else:
            print(form.errors)
    else:
        form = ClientForm()
    out = {}
    out.update({'client_form': form})
    out.update({'page_title': "Добавление клиента"})
    return render(request, 'add_edit_client.html', out)


def get_clients(request):
    clients = Clients.objects.filter(is_deleted=0)
    for c in clients:
        c.person_full_name = c.last_name + ' ' + c.name + ' ' + c.patronymic
    out = {}
    out.update({'page_title': "Клиенты"})
    out.update({'clients': clients})
    return render(request, 'get_clients.html', out)


def add_edit_order(request):
    return render(request, 'add_edit_order.html')


def get_orders(request):
    return render(request, 'get_orders.html')


def analyst(request):
    return render(request, 'index.html')


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
                return HttpResponseRedirect('/')
            else:
                out.update({"error": 1})
        else:
            form = LoginForm()
        out.update({'login_form': form})
        out.update({'page_title': "Авторизация"})
        return render(request, 'log_in.html', out)
    else:
        return HttpResponseRedirect('/')


def log_out(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    logout(request)
    return HttpResponseRedirect("/")


def page_not_found(request):
    out = {}
    out.update({'page_title': "Страница не найдена"})
    return render(request, 'page_not_found.html', out)