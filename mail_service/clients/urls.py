from django.conf.urls import url

from .views import send_email_form, create_email

app_name = 'clients'

urlpatterns = [
    url(r'^send_email/', send_email_form, name='send_mail'),
    url(r'^create_email/', create_email, name='create_email')
]
