#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from base_api.form import ProductForm, UploadFileForm
from base_api.models import Order_Files, Orders, Roles


def upload_file(request):
    out = {}
    out.update({'page_title': 'Управление файлами'})
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
    order_files = Order_Files.objects.filter(order_id=order_id).all()
    files = []
    if order_files is not None:
        for order_file in order_files:
            order_file.name = order_file.title
            order_file.url = order_file.file.url
            files.append(order_file)
    out.update({'files': files})
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            obj = form.save(commit=False)
            obj.order = Orders.objects.get(id=order_id)
            if obj.title is None or obj.title == '':
                obj.title = request.FILES['file'].name
            if obj.file is not None and obj.file != '':
                obj.save()
            form_new = UploadFileForm()
            out.update({'form': form_new})
            order_files = Order_Files.objects.filter(order_id=order_id).all()
            files = []
            if order_files is not None:
                for order_file in order_files:
                    order_file.name = order_file.title
                    order_file.url = order_file.file.url
                    files.append(order_file)
            out.update({'files': files})
            return render(request, 'files.html', out)
    else:
        form = UploadFileForm()
    out.update({'form': form})
    print(form.errors)
    return render(request, 'files.html', out)


def delete_file(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order_file = Order_Files.objects.get(pk=id)
    id = order_file.order.id
    order_file.delete()
    return HttpResponseRedirect('/uploads/?id=%s' % id)
