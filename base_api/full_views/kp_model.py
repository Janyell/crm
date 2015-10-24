#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import Template, Context
from api.settings import MEDIA_ROOT
from base_api.models import *
import pypandoc


def get_kp(request):
    if 'format' not in request.POST:
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
        out.update({'page_title': "Создание КП"})
        temp_out = {}
        organization_name = request.POST['organization_name']
        accompanying_text = request.POST['accompanying_text']
        table__total_kp = request.POST['table__total_kp']
        added_table__total_kp = request.POST['added_table__total_kp']
        added_table__total = request.POST['added_table__total']
        table__total = request.POST['table__total']
        added_table = ''
        if 'added_table' in request.POST:
            added_table = request.POST['added_table']
            added_table_out = {}
            added_table_out.update({'added_table__total_kp ': added_table__total_kp })
            added_table = Template(added_table).render(Context(added_table_out))
        page = request.POST['page']
        temp_out.update({'organization_name': u'<input type="text" class="organization_name" name="organization_name" value="{}">'.format(organization_name)})
        temp_out.update({'accompanying_text': accompanying_text})
        temp_out.update({'added_table': added_table})
        temp_out.update({'table__total_kp': table__total_kp})
        temp_out.update({'added_table__total_kp': added_table__total_kp})
        temp_out.update({'organization_name': organization_name})
        html = Template(page).render(Context(temp_out))
        out.update({'page': html})
        out.update({'added_table__total': added_table__total})
        out.update({'table__total': table__total})
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
        out.update({'filename': filename})
        return render(request, 'edit_kp.html', out)

    format = request.POST['format']
    filename = request.POST['filename']
    if format == 'docx':
        return HttpResponseRedirect('/media/uploads/' + filename + '.docx')
    elif format == 'pdf':
        return HttpResponseRedirect('/media/uploads/' + filename + '.pdf')


def full_generate_kp(request):
    if 'format' not in request.POST:
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
        out.update({'page_title': "Создание КП"})
        temp_out = {}
        organization_name = request.POST['organization_name']
        accompanying_text = request.POST['accompanying_text']
        table__total_kp = request.POST['table__total_kp']
        table__total = request.POST['table__total']
        added_table = ''
        added_table__total_kp = ''
        added_table__total = ''
        if 'added_table' in request.POST:
            added_table__total_kp = request.POST['added_table__total_kp']
            added_table__total = request.POST['added_table__total']
            added_table = request.POST['added_table']
            added_table_out = {}
            added_table_out.update({'added_table__total_kp ': added_table__total_kp })
            added_table = Template(added_table).render(Context(added_table_out))
        page = request.POST['page']
        temp_out.update({'organization_name': u'<input type="text" class="organization_name" name="organization_name" value="{}">'.format(organization_name)})
        temp_out.update({'accompanying_text': accompanying_text})
        temp_out.update({'added_table': added_table})
        temp_out.update({'table__total_kp': table__total_kp})
        temp_out.update({'added_table__total_kp': added_table__total_kp})
        temp_out.update({'organization_name': organization_name})
        html = Template(page).render(Context(temp_out))
        out.update({'page': html})
        out.update({'added_table__total': added_table__total})
        out.update({'table__total': table__total})
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
        out.update({'filename': filename})
        return render(request, 'edit_kp.html', out)

    format = request.POST['format']
    filename = request.POST['filename']
    if format == 'docx':
        return HttpResponseRedirect('/media/uploads/' + filename + '.docx')
    elif format == 'pdf':
        return HttpResponseRedirect('/media/uploads/' + filename + '.pdf')
