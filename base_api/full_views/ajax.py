#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db.models import Q
from django.forms.models import modelform_factory
from django.shortcuts import render
from base_api.constants import DEFAULT_SORT_TYPE_FOR_CLAIM, SORT_TYPE_FOR_CLAIM, DEFAULT_NUMBER_FOR_PAGE
from base_api.full_views.helper import get_request_param_as_string
from base_api.full_views.order_views import right_money_format
from base_api.form import *
from django.http import *
from django.core import serializers
import random
import string
import json


def get_clients(request):
    data = []
    search_word = request.GET['search']
    client_list = list(Clients.objects.filter(organization__icontains=search_word).filter(is_deleted=0))
    contact_faces_list = list(ContactFaces.objects.filter(
        Q(name__icontains=search_word) |
        Q(last_name__icontains=search_word) |
        Q(patronymic__icontains=search_word)
    ).filter(is_deleted=0))
    contact_faces_list_ids = [object.organization_id for object in contact_faces_list]
    client_list += list(Clients.objects.filter(pk__in=contact_faces_list_ids, is_deleted=0))
    client_list = list(set(client_list))
    for client in client_list:
        data.append(
            {
                'id': client.id,
                'title': client_label_from_instance(client)
            }
        )
    return HttpResponse(json.dumps(data), content_type="application/json; charset=utf-8")
