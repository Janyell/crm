#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_request_param_as_string(request):
    get_params = ''
    if 'page' in request.GET:
        page = int(request.GET['page'])
        get_params += 'page=' + str(page) + '&'
    if 'length' in request.GET:
        length = int(request.GET['length'])
        get_params += 'length=' + str(length) + '&'
    if 'sort' in request.GET:
        sort = request.GET['sort']
        get_params += 'sort=' + str(sort) + '&'
    if 'managers[]' in request.GET:
        managers = request.GET.getlist('managers[]')
        for manager in managers:
            get_params += 'managers[]=' + manager + '&'
    if 'source' in request.GET:
        source = int(request.GET.get('source'))
        get_params += 'source=' + str(source) + '&'
    return get_params