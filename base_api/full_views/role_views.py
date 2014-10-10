#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from datetime import datetime
from base_api.models import *
from base_api.forms import *
from django.http import *
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ObjectDoesNotExist
from confirm import *


def full_add_edit_role(request):
    # строки закомменчены чтобы добавлять новых пользователей при удалении базы
    # if not request.user.is_active:
    #     return HttpResponseRedirect('/login/')
    action = request.GET['']
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if action == 'edit':
            username = request.POST['username']
            password = request.POST['password']
            role = request.POST['role']
            surname = request.POST['surname']
            name = request.POST['name']
            patronymic = request.POST['patronymic']
            new_author = Roles(id=id, username=username, role=role, surname=surname,
                               name=name, patronymic=patronymic)
            new_author.set_password(password)
            new_author.save(force_update=True)
            return HttpResponseRedirect('/roles/')
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
        if action == 'edit':
            author = Roles.objects.get(pk=id)
            form = RoleForm({'username': author.username, 'role': author.role, 'surname': author.surname,
                             'name': author.name, 'patronymic': author.patronymic})
        else:
            form = RoleForm()
    out = {}
    out.update({'role_form': form})
    out.update({'page_title': "Добавление роли"})
    return render(request, "add_edit_role.html", out)


def remove_file_context(request):
    id = request.GET['id']
    role = Roles.objects.get(pk=id)
    return RequestContext(request, {'file': role})


@confirm_required('remove_file_confirm.html', remove_file_context)
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
    out = {}
    out.update({'page_title': "Роли"})
    out.update({'roles': roles})
    return render(request, 'get_roles.html', out)