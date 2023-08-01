#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.utils import timezone

from .models import Client, EmailLetter


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailLetter
        fields = [
            'header',
            'text',
            'footer',
        ]


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'email',
            'birthday',
        ]


class SendLetterForm(forms.Form):
    clients = forms.ModelMultipleChoiceField(
        label='Выберите подписчиков для рассылки',
        queryset=Client.objects.all(),
        widget=forms.widgets.SelectMultiple(attrs={'class': 'form-control'})
    )
    letter = forms.ModelChoiceField(
        label='Выберите письмо для отправки',
        queryset=EmailLetter.objects.all(),
        widget=forms.widgets.Select(attrs={'class': 'form-control'})
    )
    send_datetime = forms.DateTimeField(
        label='Выберите дату и время отправки по Мск',
        required=False,
        initial=format(timezone.now(), '%Y-%m-%d %H:%M'),
    )
