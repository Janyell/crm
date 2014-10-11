from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'base_api.views.analyst', name='index'),
                       url(r'^analyst/$', 'base_api.views.analyst', name='analyst'),
                       url(r'^login/$', 'base_api.views.log_in', name='login'),
                       url(r'^logout/$', 'base_api.views.log_out', name='logout'),
                       url(r'^orders/$', 'base_api.views.get_orders', name='get_orders'),
                       url(r'^orders/add/$', 'base_api.views.add_edit_order', name='add_order'),
                       url(r'^orders/edit/$', 'base_api.views.add_edit_order', name='edit_order'),
                       url(r'^clients/$', 'base_api.views.get_clients', name='get_clients'),
                       url(r'^clients/add/$', 'base_api.views.add_edit_client', name='add_client'),
                       url(r'^clients/edit/$', 'base_api.views.add_edit_client', name='edit_client'),
                       url(r'^roles/$', 'base_api.views.get_roles', name='get_roles'),
                       url(r'^roles/add/$', 'base_api.views.add_edit_role', name='add_role'),
                       url(r'^roles/edit/$', 'base_api.views.add_edit_role', name='edit_role'),
                       url(r'^roles/delete/$', 'base_api.views.delete_role', name='delete_role'),
                       url(r'^companies/$', "base_api.views.get_companies", name='get_companies'),
                       url(r'^companies/add/$', 'base_api.views.add_edit_company', name='add_company'),
                       url(r'^companies/edit/$', 'base_api.views.add_edit_company', name='edit_company'),
                       url(r'^companies/delete/$', 'base_api.views.delete_company', name='delete_company'),
                       url(r'', 'base_api.views.page_not_found', name='404'),
)
