#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import *
from django import forms
from base_api.models import *
from django.forms import ModelChoiceField


BILL_STATUS_CHOICES_FOR_CLAIM = (('', '----------'),
                                 ('4', 'Устно'),
                                 ('5', 'Подбор'),
                                 ('0', 'Выставлен'),
                                 ('1', 'Нужна доплата'),
                                 ('2', 'Оплачен'))
BILL_STATUS_CHOICES_FOR_ORDER = (('1', 'Нужна доплата'),
                                 ('3', 'Отсрочка платежа'),
                                 ('2', 'Оплачен'))
PRODUCT_STATUS_FOR_PRODUCT = (('1', 'Активный'),
                              ('0', 'Неактивный'))
SOURCE_STATUS = (('1', 'Активный'),
                 ('0', 'Неактивный'))
TRANSPORT_CAMPAIGNS_STATUS = (('1', 'Активный'),
                              ('0', 'Неактивный'))
CLOSE_REASONS_STATUS = (('1', 'Активный'),
                        ('0', 'Неактивный'))


class CompanyModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class SourceModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class TransportCampaignsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class ProductGroupModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class CloseReasonsModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class CityModelChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name


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
        fields = ['username', 'password', 'role', 'surname', 'name', 'patronymic', 'email', 'phone']
        widgets = {
            'username': TextInput(attrs={'id': "inputLogin",
                                         'placeholder': "Логин",
                                         'required': 1}),
            'password': PasswordInput(attrs={'id': "inputPassword",
                                             'placeholder': "Пароль"}),
            'role': Select(attrs={'id': "selectRole",
                                  'required': 1}),
            'email': TextInput(attrs={'id': "inputEmail",
                                      'placeholder': "Email"}),
            'phone': TextInput(attrs={'id': "inputPhone",
                                      'placeholder': "Телефон"}),
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
            'person_phone': TextInput(attrs={'id': "inputPersonPhone",
                                             'type': "tel",
                                             'pattern': "(\+\d+)?([- ]?\(?\d+\)[- ]?)?(\d+[- ]?)*",
                                             'placeholder': "Телефон контактного лица"}),
            'organization_phone': TextInput(attrs={'id': "inputOrganizationPhone",
                                                   'type': "tel",
                                                   'pattern': "(\+\d+)?([- ]?\(?\d+\)[- ]?)?(\d+[- ]?)*",
                                                   'placeholder': "Телефон организации"}),
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
    'bill': NumberInput(attrs={'id': "inputBill"}),
    'payment_date': TextInput(attrs={'id': "inputPaymentDate",
                                     'class': "datetime",
                                     'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'order_status': Select(attrs={'id': "selectStatus"}),
    'bill_status': Select(attrs={'id': "selectBillStatus"}, choices=BILL_STATUS_CHOICES_FOR_ORDER),
    'city': Select(attrs={'id': "selectCity",
                          'placeholder': "Город"}),
    'comment': Textarea(attrs={'id': "inputComment",
                               'placeholder': "Комментарии",
                               'rows': "1"}),
    'source': Select(attrs={'id': "selectSource", 'required': 1}),
    'transport_campaign': Select(attrs={'id': "selectTransportCampaign", 'required': 0}),
    'ready_date': TextInput(attrs={'id': "inputReadyDate",
                                   'class': "datetime",
                                   'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'shipped_date': TextInput(attrs={'id': "inputShippedDate",
                                     'class': "datetime",
                                     'placeholder': "ГГГГ-ММ-ДД"}),
    'brought_sum': NumberInput(attrs={'id': "inputBroughtSum"}),
    'factory_comment': Textarea(attrs={'id': "inputFactoryComment",
                                       'placeholder': "Информация для производства",
                                       'rows': "1"})
}


class OrdersForm(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'role', 'in_archive', 'order_date', 'unique_number']
        widgets = orders_form_widgets

orders_form_widgets.update({'role': Select(attrs={'id': "selectRole"})})


class OrdersFormForAdmins(forms.ModelForm):
    class Meta:
        model = Orders
        exclude = ['is_deleted', 'in_archive', 'order_date', 'unique_number']
        widgets = orders_form_widgets

claims_form_widgets = {
    'client': Select(attrs={'id': "selectClient", 'required': 1, 'class': 'selectpicker'}),
    'company': Select(attrs={'id': "selectCompany", 'class': 'selectpicker', 'required': 0}),
    'bill': NumberInput(attrs={'id': "inputBill"}),
    'payment_date': TextInput(attrs={'id': "inputPaymentDate",
                                     'class': "datetime",
                                     'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'order_status': Select(attrs={'id': "selectStatus"}),
    'bill_status': Select(attrs={'id': "selectBillStatus", 'required': 1}, choices=BILL_STATUS_CHOICES_FOR_CLAIM),
    'city': Select(attrs={'id': "selectCity",
                          'placeholder': "Город"}),
    'comment': Textarea(attrs={'id': "inputComment",
                               'placeholder': "Комментарии",
                               'rows': "1"}),
    'source': Select(attrs={'id': "selectSource", 'required': 1}),
    'transport_campaign': Select(attrs={'id': "selectTransportCampaign"}),
    'ready_date': TextInput(attrs={'id': "inputReadyDate",
                                   'class': "datetime",
                                   'placeholder': "ГГГГ-ММ-ДД ЧЧ:ММ:СС"}),
    'brought_sum': NumberInput(attrs={'id': "inputBroughtSum"}),
    'factory_comment': Textarea(attrs={'id': "inputFactoryComment",
                                       'placeholder': "Информация для производства",
                                       'rows': "1"})
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


class ProductForm(ModelForm):
    class Meta:
        model = Products
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'required': 1}),
            'price': NumberInput(attrs={'id': "inputPrice"}),
            'group': Select(attrs={'id': "selectAddGroup", 'required': 1, 'class': 'selectpicker'}),
        }


class ProductEditForm(ModelForm):
    class Meta:
        model = Products
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputEditTitle",
                                      'required': 1}),
            'price': NumberInput(attrs={'id': "inputEditPrice"}),
            'is_active': Select(attrs={'id': "selectIsActive"}, choices=PRODUCT_STATUS_FOR_PRODUCT),
            'group': Select(attrs={'id': "selectEditGroup", 'required': 1, 'class': 'selectpicker'}),
        }


class ProductGroupForm(ModelForm):
    class Meta:
        model = ProductGroups
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputGroupTitle",
                                      'required': 1}),
        }


class ProductGroupEditForm(ModelForm):
    class Meta:
        model = ProductGroups
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputEditGroupTitle",
                                      'required': 1}),
        }


class CityForm(ModelForm):
    class Meta:
        model = Cities
        widgets = {
            'name': TextInput(attrs={'id': "inputName",
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


class SourceForm(ModelForm):
    class Meta:
        model = Sources
        exclude = ['is_deleted', 'is_active']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'required': 1})
        }


class TransportCampaignForm(ModelForm):
    class Meta:
        model = TransportCampaigns
        exclude = ['is_deleted', 'is_active']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'required': 1})
        }


class SourceEditForm(ModelForm):
    class Meta:
        model = Sources
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputEditTitle",
                                      'required': 1}),
            'is_active': Select(attrs={'id': "selectEditStatus"}, choices=SOURCE_STATUS),
        }


class TransportCampaignEditForm(ModelForm):
    class Meta:
        model = Sources
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputEditTitle",
                                      'required': 1}),
            'is_active': Select(attrs={'id': "selectEditStatus"}, choices=TRANSPORT_CAMPAIGNS_STATUS),
        }


class ClientRelatedForm(ModelForm):
    class Meta:
        model = Clients
        exclude = ['is_deleted']
        widgets = {
            'client_related_with': Select(attrs={'id': "id_client_related_with", 'required': 0, 'class': 'selectpicker'}),
        }


class KPTemplatesForm(ModelForm):
    class Meta:
        model = KPTemplates
        exclude = ['html_text', 'html_text_for_kp', 'company']
        widgets = {
            'number': NumberInput(attrs={'id': "inputNumber"}),
        }


class CloseClaimForm(ModelForm):
    class Meta:
        model = CloseClaims
        exclude = ['is_deleted', 'is_closed', 'order']
        widgets = {
            'final_comment': Textarea(attrs={'id': "id_final_comment",
                                             'required': 1,
                                             'rows': "1"}),
            'reason': Select(attrs={'id': "id_reason", 'required': 1, 'class': 'selectpicker'}),
        }


class CloseReasonsForm(ModelForm):
    class Meta:
        model = CloseReasons
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputTitle",
                                      'required': 1})
        }


class CloseReasonsEditForm(ModelForm):
    class Meta:
        model = CloseReasons
        exclude = ['is_deleted']
        widgets = {
            'title': TextInput(attrs={'id': "inputEditTitle",
                                      'required': 1}),
            'is_active': Select(attrs={'id': "selectEditStatus"}, choices=CLOSE_REASONS_STATUS),
        }


class TaskForm(ModelForm):
    class Meta:
        model = Tasks
        exclude = ['is_deleted']
        widgets = {
            'comment': TextInput(attrs={'id': "inputComment"}),
        }
