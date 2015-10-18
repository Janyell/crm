#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import date
import os
from django.http import HttpResponseRedirect
from subprocess import Popen
from django.shortcuts import render_to_response
from api.settings import MEDIA_ROOT, BASE_DIR
from base_api.models import *


def full_generate_kp(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    if 'page' in request.GET and 'length' in request.GET:
        page = int(request.GET['page'])
        length = int(request.GET['length'])
        start = (page - 1) * length
        out.update({'start': start})
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role == 2:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    temp_out = {}
    # accompanying_text = request.POST['accompanying_text']
    # organization_or_full_name = request.POST['organization_or_full_name']
    added_table = ''
    if 'added_table' in request.POST:
        added_table = request.POST['added_table']
    # page = request.POST['page']
    # temp_out.update({'accompanying_text': accompanying_text})
    # temp_out.update({'organization_name': organization_or_full_name})
    temp_out.update({'added_table': added_table})
    template = KPTemplates.objects.first()
    page = template.html_text

    form_file = open('templates/kp/random.html', 'wb')
    form_file.write(page.encode('utf-8'))
    form_file.close()
    html = render_to_response('kp/new_template.html', temp_out)
    form_file = open('templates/kp/kp.html', 'wb')
    form_file.write(html.content)
    form_file.close()

    filename = os.path.join(BASE_DIR, 'templates') + '/' + str('kp/kp.html')
    out_filename = MEDIA_ROOT + '/' + str('uploads/kp.docx')
    out_filename_pdf = MEDIA_ROOT + '/' + str('uploads/kp.pdf')
    Popen(['pandoc', filename, '-f', 'html', '-t', 'docx', '-s', '-o', out_filename])
    Popen(['pandoc', filename, '-f', 'html', '-s', '-o', out_filename_pdf])
    format = request.POST['format']
    if format == 'docx':
        Popen(['pandoc', filename, '-f', 'html', '-t', 'docx', '-s', '-o', out_filename])
        return HttpResponseRedirect('/media/uploads/kp.docx')
    elif format == 'pdf':
        Popen(['pandoc', filename, '-f', 'html', '-s', '-o', out_filename_pdf])
        return HttpResponseRedirect('/media/uploads/kp.pdf')
    return HttpResponseRedirect('/')