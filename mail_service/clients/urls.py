from django.conf.urls import url

from .views import manage_mail_service_view, LetterListView, ClientListView, \
    ClientUpdateView, EmailUpdateView


app_name = 'clients'

urlpatterns = [
    url(r'^index/', manage_mail_service_view, name='manage_mail_service'),
    url(r'^clients/$', LetterListView.as_view(), name='clients_list'),
    url(r'^letters/$', ClientListView.as_view(), name='letters_list'),
    url(
        r'^clients/(?P<pk>\d+)/$',
        ClientUpdateView.as_view(),
        name='clients_update'
    ),
    url(
        r'^letters/(?P<pk>\d+)/$',
        EmailUpdateView.as_view(),
        name='letters_update'
    ),
]
