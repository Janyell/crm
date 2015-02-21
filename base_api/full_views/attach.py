#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from base_api.form import FileForm, ProductForm, UploadFileForm
from base_api.models import Order_Files, Orders, Roles


def upload_file(request):
    out = {}
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    order_id = request.GET['order-id']
    files = []
    if Order_Files.objects.filter(order_id=order_id).all() is not None:
        for order_file in Order_Files.objects.filter(order_id=order_id).all():
            order_file.name = order_file.title
            order_file.url = order_file.file.url
            files.append(order_file)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        order_id = request.GET['order']
        if form.is_valid():
            # file is saved
            obj = form.save(commit=False)
            obj.order = Orders.objects.get(id=order_id)
            obj.title = request.FILES['file'].name
            try:
                obj.save()
            except Exception as e:
                print e.message
            return render(request, 'files.html', out)
    else:
        form = UploadFileForm()
    out.update({'form': form})
    out.update({'page_title': 'Добавление файла'})
    print(form.errors)
    return render(request, 'files.html', out)


def delete_file(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order_file = Order_Files.objects.get(pk=id)
    order_file.delete()
    return HttpResponseRedirect('/orders/')