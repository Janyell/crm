#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from datetime import date
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
        id = request.GET['id']
        claim = Orders.objects.get(pk=id)
        template = KPTemplates.objects.filter(company=claim.company).first()
        if not template:
            out.update({'page_title': "Для данной компании нет шаблона КП"})
            return render(request, 'edit_kp.html', out)
        temp_out = {}
        number = template.number
        template.number += 1
        template.save(update_fields=['number'])
        kp_date = date.today().strftime('%d.%m.%Y')
        products = Order_Product.objects.filter(order_id=claim.id, is_deleted=0).all()
        count = 1
        for product in products:
            product.number = count
            count += 1
            product.total_price = product.count_of_products * product.price
            product.title = product.product.title
        organization_or_full_name = request.POST['organization_or_full_name']
        # TODO
        added_table = ''
        if 'added_table' in request.POST['added_table']:
            added_table = request.POST['added_table']
        temp_out.update({'number': number})
        temp_out.update({'date': kp_date})
        temp_out.update({'organization_name': u'<input type="text" class="organization_name" name="organization_or_full_name" value="{}">'.format(organization_or_full_name)})
        temp_out.update({'added_table': added_table})
        temp_out.update({'products': products})
        temp_out.update({'in_total': claim.bill})
        temp_out.update({'manager': claim.role})
        # html = render_to_response('kp/new_template.html', temp_out)
        html = Template(template.html_text_for_kp.encode('utf-8')).render(Context(temp_out))
        out.update({'page': html})
        # os.remove(form_file.name)
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
        out.update({'filename': filename})
        return render(request, 'edit_kp.html', out)

    format = request.POST['format']
    filename = request.POST['filename']
    if format == 'docx':
        return HttpResponseRedirect('/media/uploads/' + filename + '.docx')
    elif format == 'pdf':
        return HttpResponseRedirect('/media/uploads/' + filename + '.pdf')
