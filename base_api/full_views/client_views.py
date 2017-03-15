#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import *
from django.core.exceptions import ObjectDoesNotExist
from base_api.constants import SORT_TYPE_FOR_CLIENT, DEFAULT_SORT_TYPE_FOR_CLIENT, DEFAULT_NUMBER_FOR_PAGE

from base_api.form import *
from base_api.full_views.helper import get_request_param_as_string


logger = logging.getLogger(__name__)


def full_add_edit_client(request):
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
    ClientForm.base_fields['city'] = CityModelChoiceField(queryset=Cities.objects.order_by("name").order_by("name"), required=False)
    ClientForm.base_fields['city'].widget.attrs = {'id': "id_client_city"}
    if request.method == 'POST':
        logger.info(u'New client: {}'.format(request.POST))
        form = ClientForm(request.POST)
        if 'pk' in request.POST:
            is_interested = 0
            if 'is_interested' in request.POST:
                is_interested = 1
            id_client = request.POST['pk']
            organization = request.POST['organization']
            organization_phone = request.POST['organization_phone']
            comment = request.POST['comment']
            city = request.POST['city']
            if city:
                city = Cities.objects.get(pk=city)
            else:
                city = None
            if 'newCity' in request.POST:
                newCity = request.POST['newCity']
                if newCity:
                    city = Cities.objects.create(name=newCity)
            items = request.POST.getlist('items[]')
            contact_faces = []
            for item in items:
                contact_face = {}
                contact_face.update({'id': 0})
                contact_face.update({'is_deleted': 0})
                flag_is_deleted = 0
                not_add_item = 0
                if int(item) > 0:
                    contact_face.update({'id': int(item)})
                    if not 'last_name_{}'.format(item) in request.POST and \
                            not 'name_{}'.format(item) in request.POST and \
                            not 'patronymic_{}'.format(item) in request.POST:
                        contact_face.update({'is_deleted': 1})
                        flag_is_deleted = 1
                if not flag_is_deleted:
                    last_name = request.POST.get('last_name_{}'.format(item), '')
                    name = request.POST.get('name_{}'.format(item), '')
                    patronymic = request.POST.get('patronymic_{}'.format(item), '')
                    if last_name == '' and name == '' and patronymic == '':
                        not_add_item = 1
                    emails = []
                    phones = []
                    email_ids = request.POST.getlist('emails_{}[]'.format(item))
                    for email_id in email_ids:
                        emails.append(request.POST.get('email_{}'.format(email_id)))
                    phone_ids = request.POST.getlist('phones_{}[]'.format(item))
                    for phone_id in phone_ids:
                        phones.append(request.POST.get('person_phone_{}'.format(phone_id)))
                    if organization == '' and last_name == '' and name == '' and patronymic == '':
                        out.update({"error": 3})
                        out.update({'client_form': form})
                        out.update({'page_title': "Редактирование клиента"})
                        return render(request, 'client/add_edit_client.html', out)
                    if ''.join(phones) == '' and organization_phone == '' and ''.join(emails) == '':
                        out.update({"error": 2})
                        out.update({'client_form': form})
                        out.update({'page_title': "Редактирование клиента"})
                        return render(request, 'client/add_edit_client.html', out)
                    contact_face.update({'last_name': last_name})
                    contact_face.update({'name': name})
                    contact_face.update({'patronymic': patronymic})
                    contact_face.update({'emails': emails})
                    contact_face.update({'phones': phones})
                if not not_add_item:
                    contact_faces.append(contact_face)
            last_name = ''
            name = ''
            patronymic = ''
            person_phone = ''
            email = ''
            type = request.POST['organization-type']
            if 'ip' == type:
                organization_type = u'ИП'
            elif 'ooo' == type:
                organization_type = u'ООО'
            elif 'zao' == type:
                organization_type = u'ЗАО'
            elif 'oao' == type:
                organization_type = u'ОАО'
            elif 'nko' == type:
                organization_type = u'НКО'
            elif 'tszh' == type:
                organization_type = u'ТСЖ'
            elif 'op' == type:
                organization_type = u'ОП'
            elif 'ao' == type:
                organization_type = u'АО'
            elif 'too' == type:
                organization_type = u'ТОО'
            elif 'mp' == type:
                organization_type = u'МП'
            elif 'pao' == type:
                organization_type = u'ПАО'
            else:
                organization_type = u''
            # if organization != '':
            #     if Clients.objects.filter(organization=organization).count() == 0:
            #         if 'save-and-add-order' in form.data:
            #             new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                  patronymic=patronymic, person_phone=person_phone,
            #                                  organization_phone=organization_phone, email=email,
            #                                  organization_type=organization_type, is_interested=is_interested)
            #             new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                            "person_phone", "organization_phone", "email", "is_interested",
            #                                            "organization_type"])
            #             if is_interested == 1:
            #                 return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
            #             return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
            #         elif 'only-save' in form.data:
            #             new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                  patronymic=patronymic, person_phone=person_phone,
            #                                  organization_phone=organization_phone, email=email,
            #                                  organization_type=organization_type, is_interested=is_interested)
            #             new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                            "person_phone", "organization_phone", "email", "is_interested",
            #                                            "organization_type"])
            #             if is_interested == 1:
            #                 return HttpResponseRedirect('/clients/interested/')
            #         return HttpResponseRedirect('/clients/')
            #     else:
            #         exist_org = Clients.objects.get(organization=organization)
            #         if str(exist_org.id) == id_client:
            #             if 'save-and-add-order' in form.data:
            #                 new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                      patronymic=patronymic, person_phone=person_phone,
            #                                      organization_phone=organization_phone, email=email,
            #                                      organization_type=organization_type, is_interested=is_interested)
            #                 new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                                "person_phone", "organization_phone", "email",
            #                                                "organization_type", "is_interested"])
            #                 if is_interested == 1:
            #                     return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
            #                 return HttpResponseRedirect('/orders/add/?client-id=' + str(new_client.pk))
            #             elif 'only-save' in form.data:
            #                 new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
            #                                      patronymic=patronymic, person_phone=person_phone,
            #                                      organization_phone=organization_phone, email=email,
            #                                      organization_type=organization_type, is_interested=is_interested)
            #                 new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
            #                                            "person_phone", "organization_phone", "email", "is_interested",
            #                                            "organization_type"])
            #                 if is_interested == 1:
            #                     return HttpResponseRedirect('/clients/interested/')
            #                 return HttpResponseRedirect('/clients/')
            #             return HttpResponseRedirect('/clients/')
            #         else:
            #             out.update({"error": 1})
            #             out.update({'page_title': "Редактирование компании"})
            # else:
            if 'save-and-add-order' in form.data:
                new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         organization_type=organization_type, is_interested=is_interested,
                                     comment=comment, city=city)
                new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
                                                   "person_phone", "organization_phone", "email", "is_interested",
                                                   "organization_type", "comment", "city"])
                new_client.client_label_from_instance = client_label_from_instance(new_client)
                new_client.save()
                for contact_face in contact_faces:
                    if contact_face['id'] != 0:
                        if contact_face.get('is_deleted'):
                            new_contact_face = ContactFaces(id=contact_face['id'],
                                                            is_deleted=contact_face.get('is_deleted'))
                            new_contact_face.save(update_fields=["is_deleted"])
                        else:
                            new_contact_face = ContactFaces(id=contact_face['id'],
                                                            last_name=contact_face.get('last_name'),
                                                            name=contact_face.get('name'),
                                                            is_deleted=contact_face.get('is_deleted'),
                                                            patronymic=contact_face.get('patronymic'),
                                                            organization=new_client)
                            new_contact_face.save()
                        for email in ContactEmail.objects.filter(face=new_contact_face):
                            email.is_deleted = 1
                            email.save()
                        for phone in ContactPhone.objects.filter(face=new_contact_face):
                            phone.is_deleted = 1
                            phone.save()
                    else:
                        new_contact_face = ContactFaces(last_name=contact_face.get('last_name'),
                                                        name=contact_face.get('name'),
                                                        patronymic=contact_face.get('patronymic'),
                                                        organization=new_client)
                        new_contact_face.save()
                    for email in contact_face.get('emails', []):
                        if email:
                            new_email = ContactEmail(face=new_contact_face, email=email)
                            new_email.save()
                    for phone in contact_face.get('phones', []):
                        if phone:
                            new_phone = ContactPhone(face=new_contact_face, phone=phone)
                            new_phone.save()
                return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
            elif 'save-and-upload-file' in form.data:
                new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         organization_type=organization_type, is_interested=is_interested,
                                     comment=comment, city=city)
                new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
                                                   "person_phone", "organization_phone", "email", "is_interested",
                                                   "organization_type", "comment", "city"])
                for contact_face in contact_faces:
                    if contact_face['id'] != 0:
                        if contact_face.get('is_deleted'):
                            new_contact_face = ContactFaces(id=contact_face['id'],
                                                            is_deleted=contact_face.get('is_deleted'))
                            new_contact_face.save(update_fields=["is_deleted"])
                        else:
                            new_contact_face = ContactFaces(id=contact_face['id'],
                                                            last_name=contact_face.get('last_name'),
                                                            name=contact_face.get('name'),
                                                            is_deleted=contact_face.get('is_deleted'),
                                                            patronymic=contact_face.get('patronymic'),
                                                            organization=new_client)
                            new_contact_face.save()
                        for email in ContactEmail.objects.filter(face=new_contact_face):
                            email.is_deleted = 1
                            email.save()
                        for phone in ContactPhone.objects.filter(face=new_contact_face):
                            phone.is_deleted = 1
                            phone.save()
                    else:
                        new_contact_face = ContactFaces(last_name=contact_face.get('last_name'),
                                                        name=contact_face.get('name'),
                                                        patronymic=contact_face.get('patronymic'),
                                                        organization=new_client)
                        new_contact_face.save()
                    for email in contact_face.get('emails', []):
                        if email:
                            new_email = ContactEmail(face=new_contact_face, email=email)
                            new_email.save()
                    for phone in contact_face.get('phones', []):
                        if phone:
                            new_phone = ContactPhone(face=new_contact_face, phone=phone)
                            new_phone.save()
                new_client.client_label_from_instance = client_label_from_instance(new_client)
                new_client.save()
                return HttpResponseRedirect('/uploads/client/?id=%s' % new_client.id)
            else:
                new_client = Clients(id=id_client, organization=organization, last_name=last_name, name=name,
                                         patronymic=patronymic, person_phone=person_phone,
                                         organization_phone=organization_phone, email=email,
                                         organization_type=organization_type, is_interested=is_interested,
                                     comment=comment, city=city)
                new_client.save(update_fields=["organization", "last_name", "name", "patronymic",
                                                   "person_phone", "organization_phone", "email", "is_interested",
                                                   "organization_type", "comment", "city"])
                for contact_face in contact_faces:
                    if contact_face['id'] != 0:
                        if contact_face.get('is_deleted'):
                            new_contact_face = ContactFaces(id=contact_face['id'],
                                                            is_deleted=contact_face.get('is_deleted'))
                            new_contact_face.save(update_fields=["is_deleted"])
                        else:
                            new_contact_face = ContactFaces(id=contact_face['id'],
                                                            last_name=contact_face.get('last_name'),
                                                            name=contact_face.get('name'),
                                                            is_deleted=contact_face.get('is_deleted'),
                                                            patronymic=contact_face.get('patronymic'),
                                                            organization=new_client)
                            new_contact_face.save()
                        for email in ContactEmail.objects.filter(face=new_contact_face):
                            email.is_deleted = 1
                            email.save()
                        for phone in ContactPhone.objects.filter(face=new_contact_face):
                            phone.is_deleted = 1
                            phone.save()
                    else:
                        new_contact_face = ContactFaces(last_name=contact_face.get('last_name'),
                                                        name=contact_face.get('name'),
                                                        patronymic=contact_face.get('patronymic'),
                                                        organization=new_client)
                        new_contact_face.save()
                    for email in contact_face.get('emails', []):
                        if email:
                            new_email = ContactEmail(face=new_contact_face, email=email)
                            new_email.save()
                    for phone in contact_face.get('phones', []):
                        if phone:
                            new_phone = ContactPhone(face=new_contact_face, phone=phone)
                            new_phone.save()
                new_client.client_label_from_instance = client_label_from_instance(new_client)
                new_client.save()
                get_params = '?'
                if 'search' in request.GET:
                    search = request.GET.get('search')
                    get_params += 'search=' + unicode(search)
                    return HttpResponseRedirect('/search/' + get_params)
                get_params += get_request_param_as_string(request)
                if is_interested == 1:
                    return HttpResponseRedirect('/clients/interested/' + get_params)
                return HttpResponseRedirect('/clients/' + get_params)
            return HttpResponseRedirect('/clients/')
        else:
            organization = request.POST['organization']
            organization_phone = request.POST['organization_phone']
            comment = request.POST['comment']
            city = request.POST['city']
            if city:
                city = Cities.objects.get(pk=city)
            else:
                city = None
            if 'newCity' in request.POST:
                newCity = request.POST['newCity']
                if newCity:
                    city = Cities.objects.create(name=newCity)
            items = request.POST.getlist('items[]')
            contact_faces = []
            for item in items:
                last_name = request.POST['last_name_{}'.format(item)]
                name = request.POST['name_{}'.format(item)]
                patronymic = request.POST['patronymic_{}'.format(item)]
                emails = []
                phones = []
                email_ids = request.POST.getlist('emails_{}[]'.format(item))
                for email_id in email_ids:
                    emails.append(request.POST.get('email_{}'.format(email_id)))
                phone_ids = request.POST.getlist('phones_{}[]'.format(item))
                for phone_id in phone_ids:
                    phones.append(request.POST.get('person_phone_{}'.format(phone_id)))
                if organization == '' and last_name == '' and name == '' and patronymic == '':
                    out.update({"error": 3})
                    out.update({'client_form': form})
                    out.update({'page_title': "Редактирование клиента"})
                    return render(request, 'client/add_edit_client.html', out)
                if ''.join(phones) == '' and organization_phone == '' and ''.join(emails) == '':
                    out.update({"error": 2})
                    out.update({'client_form': form})
                    out.update({'page_title': "Редактирование клиента"})
                    return render(request, 'client/add_edit_client.html', out)
                contact_faces.append({
                    'last_name': last_name,
                    'name': name,
                    'patronymic': patronymic,
                    'emails': emails,
                    'phones': phones,
                })
            last_name = ''
            name = ''
            patronymic = ''
            person_phone = ''
            email = ''
            type = request.POST['organization-type']
            if 'ip' == type:
                organization_type = u'ИП'
            elif 'ooo' == type:
                organization_type = u'ООО'
            elif 'zao' == type:
                organization_type = u'ЗАО'
            elif 'oao' == type:
                organization_type = u'ОАО'
            elif 'nko' == type:
                organization_type = u'НКО'
            elif 'tszh' == type:
                organization_type = u'ТСЖ'
            elif 'op' == type:
                organization_type = u'ОП'
            elif 'ao' == type:
                organization_type = u'АО'
            elif 'too' == type:
                organization_type = u'ТОО'
            elif 'mp' == type:
                organization_type = u'МП'
            elif 'pao' == type:
                organization_type = u'ПАО'
            else:
                organization_type = u''
            role = Roles.objects.get(id=request.user.id, is_deleted=0)
            is_interested = 0
            if 'is_interested' in request.POST:
                is_interested = 1
            print '1'
            if organization != '':
                is_org_exist = Clients.objects.filter(organization_type=organization_type,
                                                   organization=organization,
                                                   organization_phone=organization_phone,
                                                   is_deleted=0).all()
                if not is_org_exist:
                    if 'save-and-upload-file' in form.data:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            creation_date=datetime.now(), is_interested=is_interested,
                                                            role=role, organization_type=organization_type,
                                                            comment=comment, city=city)
                        for contact_face in contact_faces:
                            new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                           name=contact_face['name'],
                                                                           patronymic=contact_face['patronymic'],
                                                                           organization=new_client)
                            for email in contact_face['emails']:
                                if email:
                                    new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                            for phone in contact_face['phones']:
                                if phone:
                                    new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                        new_client.client_label_from_instance = client_label_from_instance(new_client)
                        new_client.save()
                        return HttpResponseRedirect('/uploads/client/?id=%s' % new_client.pk)
                    elif 'only-save' in form.data:
                        get_params = '?'
                        get_params += get_request_param_as_string(request)
                        if is_interested == 1:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), is_interested=is_interested,
                                                                role=role, organization_type=organization_type,
                                                                comment=comment, city=city)
                            for contact_face in contact_faces:
                                new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                               name=contact_face['name'],
                                                                               patronymic=contact_face['patronymic'],
                                                                               organization=new_client)
                                for email in contact_face['emails']:
                                    if email:
                                        new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                                for phone in contact_face['phones']:
                                    if phone:
                                        new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                            new_client.client_label_from_instance = client_label_from_instance(new_client)
                            new_client.save()
                            return HttpResponseRedirect('/clients/interested/' + get_params)
                        else:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), role=role,
                                                                organization_type=organization_type,
                                                                comment=comment, city=city)
                            for contact_face in contact_faces:
                                new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                               name=contact_face['name'],
                                                                               patronymic=contact_face['patronymic'],
                                                                               organization=new_client)
                                for email in contact_face['emails']:
                                    if email:
                                        new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                                for phone in contact_face['phones']:
                                    if phone:
                                        new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                            new_client.client_label_from_instance = client_label_from_instance(new_client)
                            new_client.save()
                            return HttpResponseRedirect('/clients/' + get_params)
                    # if 'save-and-add-order' in form.data:
                    else:
                        if is_interested == 1:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), is_interested=is_interested,
                                                                role=role, organization_type=organization_type,
                                                                comment=comment, city=city)
                            for contact_face in contact_faces:
                                new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                               name=contact_face['name'],
                                                                               patronymic=contact_face['patronymic'],
                                                                               organization=new_client)
                                for email in contact_face['emails']:
                                    if email:
                                        new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                                for phone in contact_face['phones']:
                                    if phone:
                                        new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                            new_client.client_label_from_instance = client_label_from_instance(new_client)
                            new_client.save()
                            return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                        else:
                            new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                                patronymic=patronymic, person_phone=person_phone,
                                                                organization_phone=organization_phone, email=email,
                                                                creation_date=datetime.now(), role=role,
                                                                organization_type=organization_type,
                                                                comment=comment, city=city)
                            for contact_face in contact_faces:
                                new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                               name=contact_face['name'],
                                                                               patronymic=contact_face['patronymic'],
                                                                               organization=new_client)
                                for email in contact_face['emails']:
                                    if email:
                                        new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                                for phone in contact_face['phones']:
                                    if phone:
                                        new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                            new_client.client_label_from_instance = client_label_from_instance(new_client)
                            new_client.save()
                            return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                    return HttpResponseRedirect('/clients/')
                out.update({"error": 1})
                out.update({'client_form': form})
                out.update({'page_title': "Добавление клиента"})
                return render(request, 'client/add_edit_client.html', out)
            else:
                print '2'
                if 'only-save' in form.data:
                    get_params = '?'
                    get_params += get_request_param_as_string(request)
                    if is_interested == 1:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            creation_date=datetime.now(), is_interested=is_interested,
                                                            role=role, organization_type=organization_type,
                                                            comment=comment, city=city)
                        for contact_face in contact_faces:
                            new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                           name=contact_face['name'],
                                                                           patronymic=contact_face['patronymic'],
                                                                           organization=new_client)
                            for email in contact_face['emails']:
                                if email:
                                    new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                            for phone in contact_face['phones']:
                                if phone:
                                    new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                        new_client.client_label_from_instance = client_label_from_instance(new_client)
                        new_client.save()
                        return HttpResponseRedirect('/clients/interested/' + get_params)
                    else:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            creation_date=datetime.now(), role=role,
                                                            organization_type=organization_type,
                                                            comment=comment, city=city)
                        for contact_face in contact_faces:
                            new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                           name=contact_face['name'],
                                                                           patronymic=contact_face['patronymic'],
                                                                           organization=new_client)
                            for email in contact_face['emails']:
                                if email:
                                    new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                            for phone in contact_face['phones']:
                                if phone:
                                    new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                        new_client.client_label_from_instance = client_label_from_instance(new_client)
                        new_client.save()
                        return HttpResponseRedirect('/clients/' + get_params)
                elif 'save-and-upload-file' in form.data:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            creation_date=datetime.now(), is_interested=is_interested,
                                                            role=role, organization_type=organization_type,
                                                            comment=comment, city=city)
                        for contact_face in contact_faces:
                            new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                           name=contact_face['name'],
                                                                           patronymic=contact_face['patronymic'],
                                                                           organization=new_client)
                            for email in contact_face['emails']:
                                if email:
                                    new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                            for phone in contact_face['phones']:
                                if phone:
                                    new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                        new_client.client_label_from_instance = client_label_from_instance(new_client)
                        new_client.save()
                        return HttpResponseRedirect('/uploads/client/?id=%s' % new_client.pk)
                # elif 'save-and-add-order' in form.data:
                else:
                    if is_interested == 1:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            creation_date=datetime.now(),
                                                            is_interested=is_interested, role=role,
                                                            organization_type=organization_type,
                                                            comment=comment, city=city)
                        for contact_face in contact_faces:
                            new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                           name=contact_face['name'],
                                                                           patronymic=contact_face['patronymic'],
                                                                           organization=new_client)
                            for email in contact_face['emails']:
                                if email:
                                    new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                            for phone in contact_face['phones']:
                                if phone:
                                    new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                        new_client.client_label_from_instance = client_label_from_instance(new_client)
                        new_client.save()
                        return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                    else:
                        new_client = Clients.objects.create(organization=organization, last_name=last_name, name=name,
                                                            patronymic=patronymic, person_phone=person_phone,
                                                            organization_phone=organization_phone, email=email,
                                                            creation_date=datetime.now(), role=role,
                                                            organization_type=organization_type,
                                                            comment=comment, city=city)
                        for contact_face in contact_faces:
                            new_contact_face = ContactFaces.objects.create(last_name=contact_face['last_name'],
                                                                           name=contact_face['name'],
                                                                           patronymic=contact_face['patronymic'],
                                                                           organization=new_client)
                            for email in contact_face['emails']:
                                if email:
                                    new_email = ContactEmail.objects.create(face=new_contact_face, email=email)
                            for phone in contact_face['phones']:
                                if phone:
                                    new_phone = ContactPhone.objects.create(face=new_contact_face, phone=phone)
                        new_client.client_label_from_instance = client_label_from_instance(new_client)
                        new_client.save()
                        return HttpResponseRedirect('/claims/add/?client-id=' + str(new_client.pk))
                return HttpResponseRedirect('/clients/')
    else:
        if 'id' in request.GET:
            id_client = request.GET['id']
            out.update({"error": 0})
            client = Clients.objects.get(pk=id_client)
            form = ClientForm({'last_name': client.last_name, 'name': client.name, 'patronymic': client.patronymic,
                               'organization': client.organization, 'person_phone': client.person_phone, 'pk': id_client,
                               'organization_phone': client.organization_phone, 'email': client.email,
                               'organization_type': client.organization_type, 'comment': client.comment,
                               'city': client.city})
            contact_faces = ContactFaces.objects.filter(is_deleted=0, organization=client).all()
            for contact_face in contact_faces:
                contact_face.phones = ContactPhone.objects.filter(is_deleted=0, face=contact_face.id).all()
                contact_face.emails = ContactEmail.objects.filter(is_deleted=0, face=contact_face.id).all()
            out.update({'contact_faces': contact_faces})
            # order_products = Order_Product.objects.filter(order_id=id_order, is_deleted=0)
            # products_list = []
            # for pr in order_products:
            #     products_list.append(pr.product_id)
            # for product in form.products:
            #     product.price_right_format = right_money_format(product.price)
            #     if product.id in products_list:
            #         product.count_of_products = Order_Product.objects.get(product_id=product.id,
            #                                                               order_id=id_order, is_deleted=0).count_of_products
            #         product.price = Order_Product.objects.get(product_id=product.id,
            #                                                               order_id=id_order, is_deleted=0).price
            out.update({'page_title': "Редактирование клиента"})
        else:
            form = ClientForm()
            out.update({'page_title': "Добавление клиента"})
    organizations = []
    for organization in Clients.objects.all().order_by('organization'):
        if organization.organization != "":
            organizations.append(organization.organization.strip())
    out.update({'client_form': form})
    out.update({'organizations': organizations})
    return render(request, 'client/add_edit_client.html', out)


def full_delete_clients(request):
    if not request.user.is_active:
        return HttpResponseRedirect('/login/')
    if Roles.objects.get(id=request.user.id).role != 0:
        return HttpResponseRedirect('/oops')
    id = request.GET['id']
    client = Clients.objects.get(pk=id)
    is_interested = client.is_interested
    client.is_deleted = 1
    client.save(update_fields=["is_deleted"])
    get_params = '?'
    if 'search' in request.GET:
        search = request.GET.get('search')
        get_params += 'search=' + unicode(search)
        return HttpResponseRedirect('/search/' + get_params)
    get_params += get_request_param_as_string(request)
    if is_interested == 0:
        return HttpResponseRedirect('/clients/' + get_params)
    else:
        return HttpResponseRedirect('/clients/interested/' + get_params)


def full_get_clients(request):
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
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_CLIENT)
    sort = SORT_TYPE_FOR_CLIENT.get(sort_key, DEFAULT_SORT_TYPE_FOR_CLIENT)
    try:
        clients = Clients.objects.filter(is_deleted=0, is_interested=0).order_by(sort)
    except TypeError:
        clients = Clients.objects.filter(is_deleted=0, is_interested=0).order_by(*sort)
    number = request.GET.get('length', DEFAULT_NUMBER_FOR_PAGE)
    clients_pages = Paginator(clients, number)
    page = request.GET.get('page')
    try:
        client_list = clients_pages.page(page)
    except PageNotAnInteger:
        client_list = clients_pages.page(1)
    except EmptyPage:
        client_list = clients_pages.page(clients_pages.num_pages)
    for c in client_list:
        c.person_full_name = ''
        c.email = ''
        c.person_phone = ''
        contact_faces = ContactFaces.objects.filter(organization=c.id, is_deleted=0).all()
        for contact_face in contact_faces:
            if c.person_full_name != '':
                c.person_full_name += ', '
            c.person_full_name = c.person_full_name + contact_face.last_name + ' ' \
                                 + contact_face.name + ' ' + contact_face.patronymic
            for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                if email.email:
                    if c.email:
                        c.email += ', '
                    c.email = c.email + email.email + ' (' + contact_face.last_name + ' ' + contact_face.name + ' ' + \
                              contact_face.patronymic + ')'
            for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                if phone.phone:
                    if c.person_phone:
                        c.person_phone += ', '
                    c.person_phone = c.person_phone + phone.phone + ' (' + contact_face.last_name + ' ' + \
                                     contact_face.name + ' ' + contact_face.patronymic + ')'
        c.files = []
        if Client_Files.objects.filter(client_id=c.id).all() is not None:
            for client_file in Client_Files.objects.filter(client_id=c.id).all():
                if client_file.file is not None and client_file.file != '':
                    client_file.name = client_file.title
                    client_file.url = client_file.file.url
                    c.files.append(client_file)
    out.update({'page_title': "Клиенты"})
    out.update({'clients': client_list})
    out.update({'count': clients.count()})
    return render(request, 'client/get_clients.html', out)


def full_get_interested_clients(request):
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
    sort_key = request.GET.get('sort', DEFAULT_SORT_TYPE_FOR_CLIENT)
    sort = SORT_TYPE_FOR_CLIENT.get(sort_key, DEFAULT_SORT_TYPE_FOR_CLIENT)
    try:
        clients = Clients.objects.filter(is_deleted=0).order_by(sort)
    except TypeError:
        clients = Clients.objects.filter(is_deleted=0).order_by(*sort)
    number = request.GET.get('length', DEFAULT_NUMBER_FOR_PAGE)
    clients_pages = Paginator(clients, number)
    page = request.GET.get('page')
    try:
        client_list = clients_pages.page(page)
    except PageNotAnInteger:
        client_list = clients_pages.page(1)
    except EmptyPage:
        client_list = clients_pages.page(clients_pages.num_pages)
    for c in client_list:
        c.person_full_name = ''
        c.email = ''
        c.person_phone = ''
        contact_faces = ContactFaces.objects.filter(organization=c.id, is_deleted=0).all()
        for contact_face in contact_faces:
            if c.person_full_name != '':
                c.person_full_name += ', '
            c.person_full_name = c.person_full_name + contact_face.last_name + ' ' \
                                 + contact_face.name + ' ' + contact_face.patronymic
            for email in ContactEmail.objects.filter(face=contact_face, is_deleted=0).all():
                if email.email:
                    if c.email:
                        c.email += ', '
                    c.email = c.email + email.email + ' (' + contact_face.last_name + ' ' + contact_face.name + ' ' + \
                              contact_face.patronymic + ')'
            for phone in ContactPhone.objects.filter(face=contact_face, is_deleted=0).all():
                if phone.phone:
                    if c.person_phone:
                        c.person_phone += ', '
                    c.person_phone = c.person_phone + phone.phone + ' (' + contact_face.last_name + ' ' + \
                                     contact_face.name + ' ' + contact_face.patronymic + ')'
        c.files = []
        if Client_Files.objects.filter(client_id=c.id).all() is not None:
            for client_file in Client_Files.objects.filter(client_id=c.id).all():
                if client_file.file is not None and client_file.file != '':
                    client_file.name = client_file.title
                    client_file.url = client_file.file.url
                    c.files.append(client_file)
    out.update({'page_title': "Люди"})
    out.update({'clients': client_list})
    out.update({'count': clients.count()})
    return render(request, 'client/get_clients.html', out)