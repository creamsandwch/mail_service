from django.conf.urls import url

from .views import send_email_form, CreateEmailForm, CreateClientForm

app_name = 'clients'

urlpatterns = [
    url(r'^send_email/', send_email_form, name='send_mail'),
    url(r'^create_email', CreateEmailForm.as_view(), name='create_email_form'),
    url(r'^create_client', CreateClientForm.as_view(), name='create_client_form'),
]
