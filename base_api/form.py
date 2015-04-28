#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import *
from django import forms
from base_api.models import *
from django.forms import ModelChoiceField


BILL_STATUS_CHOICES_FOR_CLAIM = (('0', 'Выставлен'),
                                 ('1', 'Нужна доплата'),
                                 ('2', 'Оплачен'),
                                 ('4', 'Устно'))
BILL_STATUS_CHOICES_FOR_ORDER = (('1', 'Нужна доплата'),
                                 ('3', 'Отсрочка платежа'),
                                 ('2', 'Оплачен'))


class CompanyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class ClientModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.organization == '':
            return obj.last_name + ' ' + obj.name + ' ' + obj.patronymic
        elif obj.organization_type != '':
            return '"' + obj.organization + '", ' + obj.organization_type
        else:
            return '"' + obj.organization + '"'


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
            'organization_type': RadioSelect(attrs={'id': "inputOrganizationType",
                                                    'placeholder': "Тип организации"}),
            'last_name': TextInput(attrs={'id': "inputСontactPerson",
                                          'placeholder': "Фамилия"}),
            'name': TextInput(attrs={'placeholder': "Имя"}),
            'patronymic': TextInput(attrs={'placeholder': "Отчество"}),
            'organization': TextInput(attrs={'id': "inputOrganization",
                                             'placeholder': "Название",
                                             'class': "form-add-client__organization-name",
                                             'autocomplete': "off"}),
            'person_phone': TextInput(attrs={'id': "inputPersonPhone"}),
            'organization_phone': TextInput(attrs={'id': "inputOrganizationPhone"}),
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

orders_form_widgets = {
    'client': Select(attrs={'id': "selectClient", 'required': 1, 'class': 'selectpicker'}),
    'company': Select(attrs={'id': "selectCompany", 'class': 'selectpicker'}),
    'bill': TextInput(attrs={'id': "inputBill"}),
    'payment_date': TextInput(attrs={'id': "inputPaymentDate",
                                     'class': "datetime",
                                     'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'order_status': Select(attrs={'id': "selectStatus"}),
    'bill_status': Select(attrs={'id': "selectBillStatus"}, choices=BILL_STATUS_CHOICES_FOR_ORDER),
    'city': TextInput(attrs={'id': "inputCity",
                             'placeholder': "Город"}),
    'comment': Textarea(attrs={'id': "inputComment",
                               'placeholder': "Комментарии"}),
    'source': Select(attrs={'id': "selectSource", 'required': 1}),
    'ready_date': TextInput(attrs={'id': "inputReadyDate",
                                   'class': "datetime",
                                   'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'shipped_date': TextInput(attrs={'id': "inputShippedDate",
                                     'class': "datetime",
                                     'placeholder': "ГГГГ-ММ-ДД"}),
}

class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'role', 'in_archive', 'order_date', 'unique_number']
        widgets = orders_form_widgets

orders_form_widgets.update({'role': Select(attrs={'id': "selectRole", 'required': 1})})


class OrdersFormForAdmins(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'role', 'in_archive', 'order_date', 'unique_number']
        widgets = orders_form_widgets

claims_form_widgets = {
    'client': Select(attrs={'id': "selectClient", 'required': 1, 'class': 'selectpicker'}),
    'company': Select(attrs={'id': "selectCompany", 'class': 'selectpicker'}),
    'bill': TextInput(attrs={'id': "inputBill"}),
    'payment_date': TextInput(attrs={'id': "inputPaymentDate",
                                     'class': "datetime",
                                     'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'order_status': Select(attrs={'id': "selectStatus"}),
    'bill_status': Select(attrs={'id': "selectBillStatus"}, choices=BILL_STATUS_CHOICES_FOR_CLAIM),
    'city': TextInput(attrs={'id': "inputCity",
                             'placeholder': "Город"}),
    'comment': Textarea(attrs={'id': "inputComment",
                               'placeholder': "Комментарии"}),
    'source': Select(attrs={'id': "selectSource", 'required': 1}),
    'ready_date': TextInput(attrs={'id': "inputReadyDate",
                                   'class': "datetime",
                                   'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
}


class ClaimsForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'role', 'in_archive', 'order_date', 'unique_number']
        widgets = claims_form_widgets

claims_form_widgets.update({'role': Select(attrs={'id': "selectRole", 'required': 1})})


class ClaimsFormForAdmins(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'in_archive', 'order_date', 'unique_number']
        widgets = claims_form_widgets


class ClaimsFormForAdmin(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'in_archive', 'order_date', 'unique_number']
        widgets = {
            'client': Select(attrs={'id': "selectClient", 'required': 1, 'class': 'selectpicker'}),
            'company': Select(attrs={'id': "selectCompany", 'class': 'selectpicker'}),
            'bill': TextInput(attrs={'id': "inputBill"}),
            'payment_date': TextInput(attrs={'id': "inputPaymentDate",
                                             'class': "datetime",
                                             'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
            'order_status': Select(attrs={'id': "selectStatus"}),
            'bill_status': Select(attrs={'id': "selectBillStatus"}, choices=BILL_STATUS_CHOICES_FOR_CLAIM),
            'city': TextInput(attrs={'id': "inputCity",
                                     'placeholder': "Город"}),
            'comment': Textarea(attrs={'id': "inputComment",
                                       'placeholder': "Комментарии"}),
            'source': Select(attrs={'id': "selectSource", 'required': 1}),
            'ready_date': TextInput(attrs={'id': "inputReadyDate",
                                           'class': "datetime",
                                           'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
            'role': Select(attrs={'id': "selectRole", 'required': 1}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Products
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'required': 1}),
        }


class UploadFileForOrderForm(ModelForm):
    class Meta:
        model = Order_Files
        exclude = ['order']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'placeholder': "Название"}),
            'file': FileInput(),
        }


class UploadFileForClientForm(ModelForm):
    class Meta:
        model = Client_Files
        exclude = ['client']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'placeholder': "Название"}),
            'file': FileInput(),
        }