#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout


def add_edit_role(request):
    out = {}
    form = RoleForm()
    out.update({'role_form': form})
    out.update({'page_title': "Добавление роли"})
    return render(request, "add_edit_role.html", out)


def get_roles(request):
    out = {}
    out.update({'page_title': "Роли"})
    return render(request, 'get_roles.html', out)


def add_edit_company(request):
    out = {}
    form = CompanyForm()
    out.update({'company_form': form})
    out.update({'page_title': "Добавление компании"})
    return render(request, 'add_edit_company.html', out)


def get_companies(request):
    out = {}
    out.update({'page_title': "Компании"})
    return render(request, 'get_companies.html', out)


def add_edit_client(request):
    out = {}
    form = ClientForm()
    out.update({'client_form': form})
    out.update({'page_title': "Добавление клиента"})
    return render(request, 'add_edit_client.html', out)


def get_clients(request):
    return render(request, 'get_clients.html')


def add_edit_order(request):
    return render(request, 'add_edit_order.html')


def get_orders(request):
    return render(request, 'get_orders.html')


def analyst(request):
    return render(request, 'index.html')


def log_in(request):
    out = {}
    form = LoginForm()
    out.update({'login_form': form})
    out.update({'page_title': "Авторизация"})
    return render(request, 'log_in.html', out)


def log_out(request):
    return render(request, 'log_out.html')


def page_not_found(request):
    out = {}
    out.update({'page_title': "Страница не найдена"})
    return render(request, 'page_not_found.html', out)