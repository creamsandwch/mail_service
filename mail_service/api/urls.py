from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from api.views import EmailLetterViewSet


app_name = 'api'

router = DefaultRouter()

router.register('emails', EmailLetterViewSet, basename='emails')

urlpatterns = [
    url('', include(router.urls)),
]
