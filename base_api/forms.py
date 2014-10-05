#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import *
from base_api.models import *


class RoleForm(ModelForm):
    class Meta:
        model = Roles
        fields = ['username', 'password', 'role', 'surname', 'name', 'patronymic']
        widgets = {
            'username': TextInput(attrs={'id': "inputLogin",
                                      'placeholder': "Логин",
                                      'required': 1}),
            'password': PasswordInput(attrs={'id': "inputPassword",
                                             'placeholder': "Пароль",
                                             'required': 1}),
            'role': Select(attrs={'id': "selectRole",
                                  'required': 1}),
            'surname': TextInput(attrs={'id': "inputSurname",
                                          'placeholder': "Фамилия"}),
            'name': TextInput(attrs={'id': "inputName",
                                     'placeholder': "Имя"}),
            'patronymic': TextInput(attrs={'id': "inputPatronymic",
                                           'placeholder': "Отчество"}),
        }


class ClientForm(ModelForm):
    class Meta:
        model = Clients
        exclude = ['is_deleted', 'creation_date', 'account_number', 'is_interested']
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
                                       'placeholder': "E-mail"})
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