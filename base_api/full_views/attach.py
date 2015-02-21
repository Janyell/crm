#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from base_api.form import FileForm, ProductForm, UploadFileForm
from base_api.models import Order_Files, Orders


def upload_file(request):
    out = {}
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
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    out.update({'form': form})
    out.update({'page_title': 'Добавление файла'})
    print(form.errors)
    return render(request, 'files.html', out)