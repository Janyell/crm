from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'base_api.views.analyst', name='index'),
                       url(r'^analyst/$', 'base_api.views.analyst', name='analyst'),
                       url(r'^analyst/products/$', 'base_api.views.analyze_products', name='analyze_products'),
                       url(r'^analyst/products/view/$', 'base_api.views.view_analyzed_product',
                           name='view_analyzed_product'),
                       url(r'^analyst/sale/$', 'base_api.views.analyze_sale', name='analyst_sale'),
                       url(r'^analyst/managers/$', 'base_api.views.analyze_managers', name='analyze_managers'),
                       url(r'^analyst/sales-by-managers/$', 'base_api.views.analyze_sales_by_managers',
                           name='analyze_sales_by_managers'),
                       url(r'^analyst/total-sales/$', 'base_api.views.analyze_total_sales',
                           name='analyze_total_sales'),
                       url(r'^analyst/period/$', 'base_api.views.analyze_period',
                           name='analyze_period'),
                       url(r'^login/$', 'base_api.views.log_in', name='login'),
                       url(r'^logout/$', 'base_api.views.log_out', name='logout'),
                       url(r'^orders/$', 'base_api.views.get_orders', name='get_orders'),
                       url(r'^orders/archive/add/$', 'base_api.views.add_in_archive', name='add_in_archive'),
                       url(r'^orders/archive/$', 'base_api.views.get_old_orders', name='get_old_orders'),
                       url(r'^orders/add/$', 'base_api.views.add_edit_order', name='add_order'),
                       url(r'^orders/edit/$', 'base_api.views.add_edit_order', name='edit_order'),
                       url(r'^orders/edit_order_for_factory/$', 'base_api.views.edit_order_for_factory', name='edit_order_for_factory'),
                       url(r'^orders/delete/$', 'base_api.views.delete_order', name='delete_order'),
                       url(r'^clients/$', 'base_api.views.get_clients', name='get_clients'),
                       url(r'^clients/interested/$', 'base_api.views.get_interested_clients', name='get_interested_clients'),
                       url(r'^clients/add/$', 'base_api.views.add_edit_client', name='add_client'),
                       url(r'^clients/edit/$', 'base_api.views.add_edit_client', name='edit_client'),
                       url(r'^clients/delete/$', 'base_api.views.delete_client', name='delete_client'),
                       url(r'^roles/$', 'base_api.views.get_roles', name='get_roles'),
                       url(r'^roles/add/$', 'base_api.views.add_edit_role', name='add_role'),
                       url(r'^roles/edit/$', 'base_api.views.add_edit_role', name='edit_role'),
                       url(r'^roles/delete/$', 'base_api.views.delete_role', name='delete_role'),
                       url(r'^companies/$', "base_api.views.get_companies", name='get_companies'),
                       url(r'^companies/add/$', 'base_api.views.add_edit_company', name='add_company'),
                       url(r'^companies/edit/$', 'base_api.views.add_edit_company', name='edit_company'),
                       url(r'^companies/delete/$', 'base_api.views.delete_company', name='delete_company'),
                       url(r'^oops/$', 'base_api.views.permission_deny', name='permission_deny'),
                       url(r'^order_status/$', 'base_api.views.give_order_status', name='give_order_status'),
                       url(r'', 'base_api.views.page_not_found', name='404'),
)
