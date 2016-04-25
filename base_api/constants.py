SORT_TYPE_FOR_CLAIM = {
    'role': 'role__username',
    'role_d': '-role__username',
    'order_date': 'order_date',
    'order_date_d': '-order_date',
    'organization': ['client__organization', 'client__last_name', 'client__name', 'client__patronymic'],
    'organization_d': ['-client__organization', '-client__last_name', '-client__name', '-client__patronymic'],
    'company': 'company__title',
    'company_d': '-company__title',
    'pk': 'pk',
    'transport_company': 'transport_campaign',
    'transport_company_d': '-transport_campaign',
}
DEFAULT_SORT_TYPE_FOR_CLAIM = 'order_date_d'

SORT_TYPE_FOR_ORDER = {
    'role': ['-order_status', 'role__username'],
    'role_d': ['-order_status', '-role__username'],
    'order_date': ['-order_status', 'order_date'],
    'order_date_d': ['-order_status', '-order_date'],
    'payment_date': ['-order_status', 'payment_date'],
    'payment_date_d': ['-order_status', '-payment_date'],
    'organization': ['-order_status', 'client__organization', 'client__last_name', 'client__name', 'client__patronymic'],
    'organization_d': ['-order_status', '-client__organization', '-client__last_name', '-client__name', '-client__patronymic'],
    'company': ['-order_status', 'company__title'],
    'company_d': ['-order_status', '-company__title'],
    'ready_date': ['-order_status', 'ready_date'],
    'ready_date_d': ['-order_status', '-ready_date'],
    'city': ['-order_status', 'city'],
    'city_d': ['-order_status', '-city'],
    'order_status_d': ['-order_status', '-order_status'],
    'pk': ['-order_status', 'pk'],
    'default': ['-order_status', '-shipped_date'],
    'transport_company': 'transport_campaign',
    'transport_company_d': '-transport_campaign',
}
DEFAULT_SORT_TYPE_FOR_ORDER = 'default'
DEFAULT_SORT_TYPE_FOR_ORDER_IN_ARCHIVE = 'order_date_d'

SORT_TYPE_FOR_CLIENT = {
    'organization': 'organization',
    'organization_d': '-organization',
    'organization_phone': 'organization_phone',
    'organization_phone_d': '-organization_phone',
    'name': ['last_name', 'name', 'patronymic'],
    'name_d': ['-last_name', '-name', '-patronymic'],
    'person_phone': 'person_phone',
    'person_phone_d': '-person_phone',
    'email': 'email',
    'email_d': '-email',
    'pk': 'pk'
}
DEFAULT_SORT_TYPE_FOR_CLIENT = 'organization'

SORT_TYPE_FOR_PRODUCT = {
    'title': 'title',
    'title_d': '-title',
    'price': 'price',
    'price_d': '-price',
    'pk': 'pk'
}
DEFAULT_SORT_TYPE_FOR_PRODUCT = 'title'

SORT_TYPE_FOR_ROLE = {
    'login': 'username',
    'login_d': '-username',
    'role': 'role',
    'role_d': '-role',
    'name': ['last_name', 'name', 'patronymic'],
    'name_d': ['-last_name', '-name', '-patronymic'],
    'pk': 'pk'
}
DEFAULT_SORT_TYPE_FOR_ROLE = 'pk'

SORT_TYPE_FOR_COMPANY = {
    'title': 'title',
    'title_d': '-title',
    'name': ['last_name', 'name', 'patronymic'],
    'name_d': ['-last_name', '-name', '-patronymic'],
    'pk': 'pk'
}
DEFAULT_SORT_TYPE_FOR_COMPANY = 'pk'

DEFAULT_NUMBER_FOR_PAGE = 10