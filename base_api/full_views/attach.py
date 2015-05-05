#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from media_tree.models import FileNode
from media_tree.utils import multi_splitext
from base_api.form import ProductForm, UploadFileForOrderForm, UploadFileForClientForm
from base_api.models import Order_Files, Orders, Roles, Client_Files, Clients
from django.template.defaultfilters import slugify


def upload_order_file(request):
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
            if order_file.file:
                order_file.url = order_file.file.url
                files.append(order_file)
    out.update({'files': files})
    if request.method == 'POST':
        form = UploadFileForOrderForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            obj = form.save(commit=False)
            obj.order = Orders.objects.get(id=order_id)
            if obj.file is not None and str(obj.file) != '':
                if obj.title is None or obj.title == '':
                    obj.title = request.FILES['file'].name
                obj.save()
                save_file_in_node(obj)
            form_new = UploadFileForOrderForm()
            out.update({'form': form_new})
            order_files = Order_Files.objects.filter(order_id=order_id).all()
            files = []
            if order_files is not None:
                for order_file in order_files:
                    order_file.name = order_file.title
                    if order_file.file:
                        order_file.url = order_file.file.url
                        files.append(order_file)
            out.update({'files': files})
            return render(request, 'files.html', out)
    else:
        form = UploadFileForOrderForm()
    out.update({'form': form})
    return render(request, 'files.html', out)


def delete_order_file(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    order_file = Order_Files.objects.get(pk=id)
    id = order_file.order.id
    order_file_node = FileNode.objects.get(pk=order_file.file_node.id)
    order_file.delete()
    order_file_node.delete()
    return HttpResponseRedirect('/uploads/order/?id=%s' % id)


def upload_client_file(request):
    out = {}
    out.update({'page_title': 'Управление файлами'})
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    out.update({'user_role': Roles.objects.get(id=request.user.id).role})
    if 'id' in request.GET:
        client_id = request.GET['id']
        is_interested = int(Clients.objects.get(id=client_id).is_interested)
        out.update({'is_interested': is_interested})
    else:
        return HttpResponseRedirect('/oops/')
    client_files = Client_Files.objects.filter(client_id=client_id).all()
    files = []
    if client_files is not None:
        for client_file in client_files:
            client_file.name = client_file.title
            if client_file.file:
                client_file.url = client_file.file.url
                files.append(client_file)
    out.update({'files': files})
    if request.method == 'POST':
        form = UploadFileForClientForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            obj = form.save(commit=False)
            obj.client = Clients.objects.get(id=client_id)
            if obj.file is not None and str(obj.file) != '':
                if obj.title is None or obj.title == '':
                    obj.title = request.FILES['file'].name
                obj.save()
                save_file_in_node(obj)
            form_new = UploadFileForClientForm()
            out.update({'form': form_new})
            client_files = Client_Files.objects.filter(client_id=client_id).all()
            files = []
            if client_files is not None:
                for client_file in client_files:
                    client_file.name = client_file.title
                    if client_file.file:
                        client_file.url = client_file.file.url
                        files.append(client_file)
            out.update({'files': files})
            return render(request, 'files.html', out)
    else:
        form = UploadFileForClientForm()
    out.update({'form': form})
    return render(request, 'files.html', out)


def delete_client_file(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role == 2:
        return HttpResponseRedirect('/oops/')
    id = request.GET['id']
    client_file = Client_Files.objects.get(pk=id)
    id = client_file.client.id
    client_file_node = FileNode.objects.get(pk=client_file.file_node.id)
    client_file.delete()
    client_file_node.delete()
    return HttpResponseRedirect('/uploads/client/?id=%s' % id)


def save_file_in_node(obj):
    new_file_node = FileNode(file=obj.file, node_type=FileNode.FILE, has_metadata=True)

    new_file_node.name = os.path.basename(new_file_node.file.name)
    # using os.path.splitext(), foo.tar.gz would become foo.tar_2.gz instead of foo_2.tar.gz
    split = multi_splitext(new_file_node.name)
    new_file_node.make_name_unique_numbered(split[0], split[1])

    # Determine various file parameters
    # new_file_node.size = new_file_node.file.size
    new_file_node.extension = split[2].lstrip('.').lower()
    new_file_node.width, new_file_node.height = (None, None)

    new_file_node.media_type = FileNode.mimetype_to_media_type(new_file_node.name)

    new_file_node.slug = slugify(new_file_node.name)
    new_file_node.has_metadata = new_file_node.check_minimal_metadata()

    new_file_node.title = obj.title

    new_file_node.file = str(obj.file)

    super(FileNode, new_file_node).save()

    obj.file_node = new_file_node
    obj.save()
