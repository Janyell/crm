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
        sort = int(request.GET['sort'])
        get_params += 'sort=' + str(sort) + '&'
    return get_params