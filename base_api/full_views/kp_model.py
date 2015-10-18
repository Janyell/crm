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
    id = request.GET['id']
    claim = Orders.objects.get(pk=id)
    template = KPTemplates.objects.filter(company=claim.company).first()
    temp_out = {}
    organization_or_full_name = request.POST['organization_or_full_name']
    accompanying_text = request.POST['accompanying_text']
    added_table = ''
    if 'added_table' in request.POST:
        added_table = request.POST['added_table']
    number = template.numder
    template.numder += 1
    template.save(update_fields=['number'])
    kp_date = date.today().strftime('%d.%m.%Y')
    temp_out.update({'number': number})
    temp_out.update({'date': kp_date})
    temp_out.update({'accompanying_text': accompanying_text})
    temp_out.update({'organization_or_full_name': organization_or_full_name})
    temp_out.update({'added_table': added_table})

    # form_file = open('templates/kp/random.html', 'wb')
    # form_file.write(template.html_text)
    # form_file.close()
    # html = render_to_response('kp/new_template.html', temp_out)

    # filename = os.path.join(BASE_DIR, 'templates') + '/' + str('kp/kp.html')
    # out_filename = os.path.join(BASE_DIR, 'templates') + '/' + str('kp/kp.docx')
    # out_filename_pdf = os.path.join(BASE_DIR, 'templates') + '/' + str('kp/kp.pdf')
    # # out_filename = MEDIA_ROOT + '/' + str('uploads/ttt1.docx')
    # # out_filename_pdf = MEDIA_ROOT + '/' + str('uploads/ttt1.pdf')
    # Popen(['pandoc', filename, '-f', 'html', '-t', 'docx', '-s', '-o', out_filename])
    # Popen(['pandoc', filename, '-f', 'html', '-s', '-o', out_filename_pdf])
    if template:
        out.update({'page': template.html_text})
    return HttpResponseRedirect('/')