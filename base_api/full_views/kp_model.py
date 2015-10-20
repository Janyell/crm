#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.http import HttpResponseRedirect
from django.template import Template, Context
from api.settings import MEDIA_ROOT
from base_api.models import *
import pypandoc


def fulll_generate_kp(request):
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
    accompanying_text = request.POST['accompanying_text']
    # organization_or_full_name = request.POST['organization_or_full_name']
    added_table = ''
    if 'added_table' in request.POST:
        added_table = request.POST['added_table']
    page = request.POST['page']
    temp_out.update({'accompanying_text': accompanying_text})
    temp_out.update({'added_table': added_table})

    html = Template(page).render(Context(temp_out))
    filename = str(hash(datetime.now()))
    out_filename = MEDIA_ROOT + '/' + str('uploads/') + filename + '.docx'
    out_filename_pdf = MEDIA_ROOT + '/' + str('uploads/') + filename + '.pdf'
    os.environ['PATH'] += ':/usr/texbin'
    pdoc_args = ['--latex-engine=xelatex',
                 '--variable',
                 'mainfont=Georgia',
                 '-t',
                 'latex+escaped_line_breaks',
                 '-V',
                 'geometry:margin=1in']
    pypandoc.convert(html, 'docx', format='html', outputfile=out_filename)
    os.environ['PATH'] += ':/usr/texbin'
    pypandoc.convert(out_filename, 'pdf', format='docx', outputfile=out_filename_pdf, extra_args=pdoc_args)
    return HttpResponseRedirect('/')


def full_generate_kp(request):
    format = request.POST['format']
    filename = request.POST['filename']
    if format == 'docx':
        return HttpResponseRedirect('/media/uploads/' + filename + '.docx')
    elif format == 'pdf':
        return HttpResponseRedirect('/media/uploads/' + filename + '.pdf')
