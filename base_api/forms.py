#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import *
from django import forms
from base_api.models import *
from django.forms import ModelChoiceField


class CompanyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class ClientModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.organization == '':
            return obj.last_name + ' ' + obj.name + ' ' + obj.patronymic
        else:
            return obj.organization


class RoleForm(ModelForm):
    class Meta:
        model = Roles
        fields = ['username', 'password', 'role', 'surname', 'name', 'patronymic']
        widgets = {
            'username': TextInput(attrs={'id': "inputLogin",
                                         'placeholder': "Логин",
                                         'required': 1}),
            'password': PasswordInput(attrs={'id': "inputPassword",
                                             'placeholder': "Пароль"}),
            'role': Select(attrs={'id': "selectRole",
                                  'required': 1}),
            'surname': TextInput(attrs={'id': "inputSurname",
                                        'placeholder': "Фамилия"}),
            'name': TextInput(attrs={'id': "inputName",
                                     'placeholder': "Имя"}),
            'patronymic': TextInput(attrs={'id': "inputPatronymic",
                                           'placeholder': "Отчество"})
        }


class ClientForm(ModelForm):
    class Meta:
        model = Clients
        exclude = ['is_deleted', 'creation_date', 'is_interested']
        widgets = {
            'last_name': TextInput(attrs={'id': "inputСontactPerson",
                                          'placeholder': "Фамилия"}),
            'name': TextInput(attrs={'placeholder': "Имя"}),
            'patronymic': TextInput(attrs={'placeholder': "Отчество"}),
            'organization': TextInput(attrs={'id': "inputOrganization",
                                             'placeholder': "Название",
                                             'class': "form-add-client__organization-name"}),
            'person_phone': TextInput(attrs={'id': "inputPersonPhone",
                                             'placeholder': "+7"}),
            'organization_phone': TextInput(attrs={'id': "inputOrganizationPhone",
                                                   'placeholder': "+7"}),
            'email': EmailInput(attrs={'id': "inputEmail",
                                       'placeholder': "E-mail"}),
            'account_number': TextInput(attrs={'id': 'inputAccountNumber',
                                               'placeholder': 'Номер счета'})
        }


class CompanyForm(ModelForm):
    class Meta:
        model = Companies
        exclude = ['is_delete']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'placeholder': "Название",
                                      'required': 1}),
            'last_name': TextInput(attrs={'id': "inputRepresentative",
                                          'placeholder': "Фамилия"}),
            'name': TextInput(attrs={'placeholder': "Имя"}),
            'patronymic': TextInput(attrs={'placeholder': "Отчество"}),
        }


class LoginForm(ModelForm):
    class Meta:
        model = Roles
        fields = ['username', 'password']
        widgets = {
            'username': TextInput(attrs={'class': "input-block-level",
                                      'placeholder': "Логин",
                                      'required': 1}),
            'password': PasswordInput(attrs={'class': "input-block-level",
                                             'placeholder': "Пароль",
                                             'required': 1})
        }


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'role', 'in_archive', 'order_date', 'unique_number']
        widgets = {
            'client': Select(attrs={'id': "selectClient", 'required': 1}),
            'company': Select(attrs={'id': "selectCompany"}),
            'bill': TextInput(attrs={'id': "inputBill"}),
            'payment_date': TextInput(attrs={'id': "inputPaymentDate",
                                             'class': "datetime",
                                             'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
            'order_status': Select(attrs={'id': "selectStatus"}),
            'bill_status': Select(attrs={'id': "selectBillStatus"}),
            'city': TextInput(attrs={'id': "inputCity",
                                     'placeholder': "Город"}),
            'comment': Textarea(attrs={'id': "inputComment",
                                       'placeholder': "Комментарии"}),
            'source': Select(attrs={'id': "selectSource", 'required': 1}),
            'ready_date': TextInput(attrs={'id': "inputReadyDate",
                                           'class': "datetime",
                                           'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"})
        }


class ProductForm(ModelForm):
    class Meta:
        model = Products
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'required': 1}),
        }
