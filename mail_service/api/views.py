# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from api.serializers import EmailLetterSerializer
from clients.models import EmailLetter


class EmailLetterViewSet(ModelViewSet):
    """
    Эндпоинт, при получении запроса на который
    при открытии пикселя из письма меняется статус у
    соответствующего письма в БД.
    """
    queryset = EmailLetter.objects.all()
    serializer_class = EmailLetterSerializer
    http_method_names = ['get']

    @action(
        methods=['get'],
        detail=True,
    )
    def is_opened(self, request, pk=None):
        '''
        При получении запроса на этот эндпоинт
        по ссылке из пикселя письма меняет статус is_opened
        письма.
        '''
        instance = get_object_or_404(EmailLetter, id=pk)
        instance.is_opened = True
        serializer = self.get_serializer(
            instance, many=False
        )
        return Response(
            serializer.data, status=status.HTTP_200_OK
        )
