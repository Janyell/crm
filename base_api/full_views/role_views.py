#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist


def full_add_edit_role(request):
    # строки закомменчены чтобы добавлять новых пользователей при удалении базы
    # if not request.user.is_active:
    #     return HttpResponseRedirect('/login/')
    out = {}
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if 'pk' in request.POST:
            id_role = request.POST['pk']
            username = request.POST['username']
            role = request.POST['role']
            surname = request.POST['surname']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            if Roles.objects.filter(username=username).count() == 0:
                new_author = Roles(id=id_role, username=username, role=role, surname=surname,
                                   name=name, patronymic=patronymic)
                new_author.save(force_update=True)
                return HttpResponseRedirect('/roles/')
            else:
                exist_role = Roles.objects.get(username=username)
                if str(exist_role.id) == id_role:
                    new_author = Roles(id=id_role, username=username, role=role, surname=surname,
                                       name=name, patronymic=patronymic)
                    new_author.save(force_update=True)
                    return HttpResponseRedirect('/roles/')
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

                new_author = Roles.objects.create(username=username,
                                                  is_staff=0, is_active=1, date_joined=datetime.now(),
                                                  role=role, surname=surname, name=name, patronymic=patronymic)
                new_author.set_password(password)
                new_author.save()
                return HttpResponseRedirect('/roles/')
            else:
                username = request.POST['username']
                if Roles.objects.filter(username=username).count() == 0:
                    out.update({"error": 2})
                else:
                    out.update({"error": 1})
                out.update({'page_title': "Добавление роли"})
    else:
        if 'id' in request.GET:
            id_role = request.GET['id']
            out.update({"error": 0})
            author = Roles.objects.get(pk=id_role)
            form = RoleForm({'username': author.username, 'role': author.role, 'surname': author.surname,
                             'name': author.name, 'patronymic': author.patronymic, 'pk': id_role})
            out.update({'page_title': "Редактирование роли"})
        else:
            form = RoleForm()
            out.update({'page_title': "Добавление роли"})
    out.update({'role_form': form})
    return render(request, "add_edit_role.html", out)


def full_delete_roles(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    id = request.GET['id']
    role = Roles.objects.get(pk=id)
    role.delete()
    return HttpResponseRedirect('/roles/')


def full_get_roles(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    roles = Roles.objects.filter(is_deleted=0)
    for r in roles:
        r.full_name = r.surname + ' ' + r.name + ' ' + r.patronymic
        if r.role == 1:
            r.role = "Менеджер"
        elif r.role == 2:
            r.role = "Производство"
    out = {}
    out.update({'page_title': "Роли"})
    out.update({'roles': roles})
    return render(request, 'get_roles.html', out)