#!/usr/bin/python
# -*- coding: utf-8 -*- #
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render
from base_api.full_views.order_views import right_money_format
from base_api.models import Roles, Orders, ContactFaces, ContactEmail, ContactPhone


def full_analyze_debtors(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    out = {}
    user_role = Roles.objects.get(id=request.user.id).role
    if user_role != 0 and user_role != 1:
        return HttpResponseRedirect('/oops/')
    else:
        out.update({'user_role': user_role})
    orders = Orders.objects.exclude(bill_status=2)
    orders = orders.filter(is_deleted=0, is_claim=0, brought_sum__isnull=False).exclude(bill__lt=F('brought_sum'))
    for order in orders:
        if order.client.organization == '':
            order.client.organization_or_full_name = order.client.last_name + ' ' + order.client.name + ' ' + order.client.patronymic
        else:
            order.client.organization_or_full_name = order.client.organization
        order.client.full_name = ''
        order.client.email = ''
        order.client.person_phone = ''
        contact_faces = ContactFaces.objects.filter(organization=order.client.id, is_deleted=0).all()
        for contact_face in contact_faces:
            if order.client.full_name != '':
                order.client.full_name += ', '
            order.client.full_name = order.client.full_name + contact_face.last_name + ' ' \
                                 + contact_face.name + ' ' + contact_face.patronymic
            for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                if email.email:
                    if order.client.email:
                        order.client.email += ', '
                    order.client.email = order.client.email + email.email + ' (' + contact_face.last_name + ' ' \
                                         + contact_face.name + ' ' + contact_face.patronymic + ')'
            for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                if phone.phone:
                    if order.client.person_phone:
                        order.client.person_phone += ', '
                    order.client.person_phone = order.client.person_phone + ', ' + phone.phone + ' (' + \
                                                contact_face.last_name + ' ' + contact_face.name + ' ' + \
                                                contact_face.patronymic + ')'
        order.debt_right_format = 0
        if order.brought_sum is not None and order.bill is not None:
            order.debt_right_format = right_money_format(int(order.bill) - int(order.brought_sum))
    out.update({'page_title': "Должники"})
    out.update({'debts': orders})
    return render(request, 'analyst/analyze_debtors.html', out)