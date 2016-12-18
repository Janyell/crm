from django.conf.urls import patterns, url, include
from django.http import HttpResponse
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'base_api.views.get_orders', name='index'),
                       url(r'^analyst/$', 'base_api.views.analyst', name='analyst'),
                       url(r'^analyst/products/$', 'base_api.views.analyze_products', name='analyze_products'),
                       url(r'^analyst/products/view/$', 'base_api.views.view_analyzed_product',
                           name='view_analyzed_product'),
                       url(r'^analyst/product-groups/$',
                           'base_api.full_views.analyze_products.full_analyze_products_groups',
                           name='analyze_product_groups'),
                       url(r'^analyst/product-groups/view/$',
                           'base_api.full_views.analyze_products.full_view_analyzed_product_groups',
                           name='view_analyzed_product_group'),
                       url(r'^analyst/managers/$', 'base_api.views.analyze_managers', name='analyze_managers'),
                       url(r'^analyst/period/$', 'base_api.views.analyze_period',
                           name='analyze_period'),
                       url(r'^analyst/period_product-groups/$', 'base_api.views.analyze_period_product_groups',
                           name='analyze_period_product_groups'),
                       url(r'^analyst/debtors/$', 'base_api.views.analyze_debtors', name='analyze_debtors'),
                       url(r'^analyst/cities/$', 'base_api.full_views.analyze_city.full_analyze_city',
                           name='analyze_cities'),
                       url(r'^login/$', 'base_api.views.log_in', name='login'),
                       url(r'^logout/$', 'base_api.views.log_out', name='logout'),
                       url(r'^orders/$', 'base_api.views.get_orders', name='get_orders'),
                       url(r'^orders/status/$', 'base_api.views.give_order_status', name='give_order_status'),
                       url(r'^orders/archive/add/$', 'base_api.views.add_in_archive', name='add_in_archive'),
                       url(r'^orders/archive/$', 'base_api.views.get_old_orders', name='get_old_orders'),
                       url(r'^orders/archive/delete/$', 'base_api.views.delete_from_archive',
                           name='delete_from_archive'),
                       url(r'^orders/add/$', 'base_api.views.add_edit_order', name='add_order'),
                       url(r'^orders/edit/$', 'base_api.views.add_edit_order', name='edit_order'),
                       url(r'^orders/edit/factory/$', 'base_api.views.edit_order_for_factory',
                           name='edit_order_for_factory'),
                       url(r'^orders/edit/foreign/$', 'base_api.views.edit_order_for_other_managers',
                           name='edit_order_for_other_managers'),
                       url(r'^orders/delete/$', 'base_api.views.delete_order', name='delete_order'),
                       url(r'^orders/make_claim/$', 'base_api.full_views.order_views.full_make_claim', name='make_claim'),
                       url(r'^clients/$', 'base_api.views.get_clients', name='get_clients'),
                       url(r'^clients/interested/$', 'base_api.views.get_interested_clients',
                           name='get_interested_clients'),
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
                       url(r'^products/$', 'base_api.views.get_products', name='get_products'),
                       url(r'^products/edit/$', 'base_api.views.edit_product', name='edit_product'),
                       url(r'^products/delete/$', 'base_api.views.delete_product', name='delete_product'),
                       url(r'^product_groups/$', 'base_api.views.get_product_groups', name='get_product_groups'),
                       url(r'^product_groups/edit/$', 'base_api.views.edit_product_group', name='edit_product_group'),
                       url(r'^product_groups/delete/$', 'base_api.views.delete_product_group',
                           name='delete_product_group'),
                       url(r'^claims/$', 'base_api.views.get_claims', name='get_claims'),
                       url(r'^claims/add/$', 'base_api.views.add_edit_claim', name='add_claim'),
                       url(r'^claims/edit/$', 'base_api.views.add_edit_claim', name='edit_claim'),
                       url(r'^claims/edit/foreign/$', 'base_api.views.edit_claim_for_other_managers',
                           name='edit_claim_for_other_managers'),
                       url(r'^claims/delete/$', 'base_api.views.delete_claim', name='delete_claim'),
                       url(r'^claims/bind/$', 'base_api.views.bind_claim', name='bind_claim'),
                       url(r'^claims/unbind/$', 'base_api.views.unbind_claim', name='unbind_claim'),
                       url(r'^claims/close/$', 'base_api.views.close_claim', name='close_claim'),

                       url(r'^claims/kp/edit/$', 'base_api.views.edit_kp', name='edit_kp'),
                       url(r'^uploads/order/$', 'base_api.views.upload_order_files', name='upload_order_files'),
                       url(r'^uploads/delete/order/$', 'base_api.views.delete_order_files', name='delete_order_files'),
                       url(r'^uploads/client/$', 'base_api.views.upload_client_files', name='upload_client_files'),
                       url(r'^uploads/delete/client/$', 'base_api.views.delete_client_files',
                           name='delete_client_files'),
                       url(r'^uploads/kp/$', 'base_api.full_views.attach.upload_kp_files', name='upload_kp_files'),
                       url(r'^massive/delete/clients/$', 'base_api.full_views.massive_edit.massive_delete_clients',
                           name='massive_delete_clients'),
                       url(r'^massive/delete/claims/$', 'base_api.full_views.massive_edit.massive_delete_claims',
                           name='massive_delete_claims'),
                       url(r'^massive/delete/companies/$', 'base_api.full_views.massive_edit.massive_delete_companies',
                           name='massive_delete_companies'),
                       url(r'^massive/delete/orders/$', 'base_api.full_views.massive_edit.massive_delete_orders',
                           name='massive_delete_orders'),
                       url(r'^massive/delete/products/$', 'base_api.full_views.massive_edit.massive_delete_products',
                           name='massive_delete_products'),
                       url(r'^massive/delete/roles/$', 'base_api.full_views.massive_edit.massive_delete_roles',
                           name='massive_delete_roles'),
                       url(r'^massive/delete/product_groups/$',
                           'base_api.full_views.massive_edit.massive_delete_product_groups',
                           name='massive_delete_product_groups'),
                       url(r'^massive/delete/sources/$',
                           'base_api.full_views.massive_edit.massive_delete_sources',
                           name='massive_delete_sources'),

                       url(r'^massive/delete/transport_companies/$',
                           'base_api.full_views.massive_edit.massive_delete_transport_companies',
                           name='massive_delete_transport_companies'),

                       url(r'^massive/delete/reasons/$',
                           'base_api.full_views.massive_edit.massive_delete_reasons',
                           name='massive_delete_reasons'),

                       url(r'^massive/change_manager/$',
                           'base_api.full_views.massive_edit.massive_change_manager_in_order',
                           name='massive_change_manager_in_order'),
                       url(r'^massive/add_in_archive/$', 'base_api.full_views.massive_edit.massive_add_in_archive',
                           name='massive_add_in_archive'),
                       url(r'^massive/deactivate_products/$',
                           'base_api.full_views.massive_edit.massive_deactivate_product',
                           name='massive_deactivate_product'),
                       url(r'^massive/activate_products/$', 'base_api.full_views.massive_edit.massive_activate_product',
                           name='massive_activate_product'),
                       url(r'^massive/change_product_group/$',
                           'base_api.full_views.massive_edit.massive_change_product_group',
                           name='massive_change_product_group'),
                       url(r'^massive/activate_sources/$',
                           'base_api.full_views.massive_edit.massive_activate_source',
                           name='massive_activate_source'),
                       url(r'^massive/deactivate_sources/$',
                           'base_api.full_views.massive_edit.massive_deactivate_source',
                           name='massive_deactivate_source'),

                       url(r'^massive/activate_transport_companies/$',
                           'base_api.full_views.massive_edit.massive_activate_transport_companies',
                           name='massive_activate_transport_companies'),
                       url(r'^massive/deactivate_transport_companies/$',
                           'base_api.full_views.massive_edit.massive_deactivate_transport_companies',
                           name='massive_deactivate_transport_companies'),

                       url(r'^massive/activate_reasons/$',
                           'base_api.full_views.massive_edit.massive_activate_reasons',
                           name='massive_activate_reasons'),
                       url(r'^massive/deactivate_reasons/$',
                           'base_api.full_views.massive_edit.massive_deactivate_reasons',
                           name='massive_deactivate_reasons'),

                       url(r'^cities/add/$', 'base_api.full_views.city_views.full_add_city', name='add_city'),
                       url(r'^excel/$', 'base_api.views.made_excel', name='made_excel'),
                       url(r'^excel_products/$', 'base_api.views.made_excel_products', name='made_excel_products'),
                       url(r'^documents/$', 'base_api.views.get_documents', name='get_documents'),
                       url(r'^kp/get/$', 'base_api.full_views.kp_model.get_kp', name='get_kp'),
                       # url(r'^fix_bd_org_type/$', 'base_api.views.fix_bd_org_type', name='fix_bd_org_type'),
                       # url(r'^fix_file_nodes/$', 'base_api.views.fix_file_nodes', name='fix_file_nodes'),
                       # url(r'^fix_cities/$', 'base_api.views.fix_cities', name='fix_cities'),
                       # url(r'^fix_bd_client_faces/$', 'base_api.views.fix_bd_client_faces', name='fix_bd_client_faces'),
                       url(r'^search/$', 'base_api.views.search', name='search'),
                       url(r'^settings/$', 'base_api.views.get_settings', name='get_settings'),

                       url(r'^settings/sources/$', 'base_api.full_views.source_views.full_get_sources',
                           name='get_sources'),
                       url(r'^settings/sources/edit/$', 'base_api.full_views.source_views.full_edit_source',
                           name='edit_source'),
                       url(r'^settings/sources/delete/$', 'base_api.full_views.source_views.full_delete_source',
                           name='delete_source'),

                       url(r'^settings/transport_companies/$', 'base_api.full_views.transport_campaign_views.full_get_transport_campaigns',
                           name='get_transport_companies'),
                       url(r'^settings/transport_companies/edit/$', 'base_api.full_views.transport_campaign_views.full_edit_transport_campaign',
                           name='edit_transport_company'),
                       url(r'^settings/transport_companies/delete/$', 'base_api.full_views.transport_campaign_views.full_delete_transport_campaign',
                           name='delete_transport_company'),

                       url(r'^settings/reasons/$', 'base_api.full_views.reason_views.full_get_reasons',
                           name='get_reasons'),
                       url(r'^settings/reasons/edit/$', 'base_api.full_views.reason_views.full_edit_reason',
                           name='edit_reason'),
                       url(r'^settings/reasons/delete/$', 'base_api.full_views.reason_views.full_delete_reason',
                           name='delete_reason'),

                       url(r'^settings/template/$', 'base_api.views.get_templates',
                           name='get_templates'),
                       url(r'^settings/template/edit_number$', 'base_api.views.edit_number_template',
                           name='edit_number_template'),
                       url(r'^settings/template/edit/$', 'base_api.views.edit_template',
                           name='edit_template'),

                       url(r'^reports/$', 'base_api.views.get_reports', name='get_reports'),

                       url(r'^tasks/$', 'base_api.full_views.task_views.full_get_tasks', name='get_tasks'),
                       url(r'^tasks/edit/$', 'base_api.full_views.task_views.full_edit_task', name='edit_task'),
                       url(r'^tasks/do/$', 'base_api.full_views.task_views.full_do_task', name='do_task'),

                       url(r'^related/claim/$', 'base_api.full_views.claim_views.full_bind_claims', name='related_claims'),

                       # hidden page
                       url(r'^claims/related/$', 'base_api.views.get_related_claims', name='get_related_claims'),
                       url(r'^claims/client/$', 'base_api.views.get_client_claims', name='get_client_claims'),
                       url(r'^script_phone_to_numeric/$', 'base_api.views.script_phone_to_numeric',
                           name='script_phone_to_numeric'),

                       # ajax
                       url(r'^get_clients/$', 'base_api.full_views.ajax.get_clients', name='ajax_get_clients'),

                       url(r'^robots.txt$',
                           lambda r: HttpResponse("User-agent: *\nDisallow: /", content_type="text/plain")),
                       url(r'^admin/', include(admin.site.urls)),
                       # url(r'', 'base_api.views.page_not_found', name='404'),
                       )

if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns.append(url(r'', 'base_api.views.page_not_found', name='404'))
