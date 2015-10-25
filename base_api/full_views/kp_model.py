#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect


def get_kp(request):
    format = request.POST['format']
    filename = request.POST['filename']
    if format == 'docx':
        return HttpResponseRedirect('/media/uploads/' + filename + '.docx')
    elif format == 'pdf':
        return HttpResponseRedirect('/media/uploads/' + filename + '.pdf')
