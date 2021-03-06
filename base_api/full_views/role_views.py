#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.full_views.helper import get_request_param_as_string
from base_api.models import *
from base_api.form import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_add_edit_role(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    get_params = '?'
    get_params += get_request_param_as_string(request)
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if 'pk' in request.POST:
            id_role = request.POST['pk']
            username = request.POST['username']
            password = request.POST['password']
            role = request.POST['role']
            surname = request.POST['surname']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            phone = request.POST['phone']
            email = request.POST['email']
            if Roles.objects.filter(username=username).count() == 0:
                new_author = Roles(id=id_role, username=username, role=role, surname=surname,
                                   name=name, patronymic=patronymic, email=email, phone=phone)
                if password != '':
                    new_author.set_password(password)
                    new_author.save()
                else:
                    new_author.save(update_fields=["username", "role", "surname", "name", "patronymic", "email", "phone"])
                return HttpResponseRedirect('/roles/' + get_params)
            else:
                exist_role = Roles.objects.get(username=username)
                if str(exist_role.id) == id_role:
                    new_author = Roles(id=id_role, username=username, role=role, surname=surname,
                                       name=name, patronymic=patronymic, email=email, phone=phone)
                    if password != '':
                        new_author.set_password(password)
                        new_author.save()
                    else:
                        new_author.save(update_fields=["username", "role", "surname", "name", "patronymic", "email", "phone"])
                    return HttpResponseRedirect('/roles/' + get_params)
                else:
                    out.update({"error": 1})
                    out.update({'page_title': "Редактирование роли"})
        else:
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                role = form.cleaned_data['role']
                surname = form.cleaned_data['surname']
                name = form.cleaned_data['name']
                patronymic = form.cleaned_data['patronymic']
                email = form.cleaned_data['email']
                phone = form.cleaned_data['phone']

                new_author = Roles.objects.create(username=username,
                                                  is_staff=1, is_active=1, date_joined=datetime.now(),
                                                  role=role, surname=surname, name=name, patronymic=patronymic,
                                                  is_superuser=True, email=email, phone=phone)
                new_author.set_password(password)
                new_author.save()
                return HttpResponseRedirect('/roles/' + get_params)
            else:
                username = request.POST['username']
                exist_role = Roles.objects.filter(username=username).first()
                if not exist_role:
                    out.update({"error": 2})
                elif exist_role.is_deleted:
                    exist_role.password = form.cleaned_data['password']
                    exist_role.role = form.cleaned_data['role']
                    exist_role.surname = form.cleaned_data['surname']
                    exist_role.name = form.cleaned_data['name']
                    exist_role.patronymic = form.cleaned_data['patronymic']
                    exist_role.email = form.cleaned_data['email']
                    exist_role.phone = form.cleaned_data['phone']
                    exist_role.is_deleted = False
                    password = form.cleaned_data['password']
                    if password != '':
                        exist_role.set_password(password)
                        exist_role.save()
                    else:
                        exist_role.save()
                    return HttpResponseRedirect('/roles/' + get_params)
                else:
                    out.update({"error": 1})
                out.update({'page_title': "Добавление роли"})
    else:
        if 'id' in request.GET:
            id_role = request.GET['id']
            out.update({"error": 0})
            author = Roles.objects.get(pk=id_role)
            form = RoleForm({'username': author.username, 'role': author.role, 'surname': author.surname,
                             'name': author.name, 'patronymic': author.patronymic,
                             'email': author.email, 'phone': author.phone, 'pk': id_role})
            out.update({'page_title': "Редактирование роли"})
        else:
            form = RoleForm()
            out.update({'page_title': "Добавление роли"})
    out.update({'role_form': form})
    return render(request, "role/add_edit_role.html", out)


def full_delete_roles(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    role = Roles.objects.get(pk=id)
    role.is_deleted = 1
    role.username = role.username + str(hash(datetime.now()))
    role.save(update_fields=["is_deleted", "username"])
    get_params = '?'
    get_params += get_request_param_as_string(request)
    return HttpResponseRedirect('/roles/' + get_params)


def full_get_roles(request):
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
    roles = Roles.objects.filter(is_deleted=0)
    for r in roles:
        r.full_name = r.surname + ' ' + r.name + ' ' + r.patronymic
        if r.role == 1:
            r.role = "Менеджер"
        elif r.role == 2:
            r.role = "Производство"
        elif r.role == 0:
            r.role = "Руководство"
        elif r.role == 3:
            r.role = "Старший менеджер"
    out.update({'page_title': "Роли"})
    out.update({'roles': roles})
    out.update({'count': roles.count()})
    return render(request, 'role/get_roles.html', out)