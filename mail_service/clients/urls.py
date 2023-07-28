from django.conf.urls import url

from .views import manage_mail_service_view

app_name = 'clients'

urlpatterns = [
    url('', manage_mail_service_view, name='manage_mail_service'),
]
