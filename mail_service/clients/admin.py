# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from clients.models import Client, EmailLetter


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    readonly_fields = [
        'date_joined',
        'id',
        'letters',
    ]
    list_display = [
        'id',
        'full_name',
        'email',
        'date_joined',
        'letters',
    ]

    def letters(self, obj):
        '''Отправленные письма.'''
        return obj.letters.all()

    def full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name


@admin.register(EmailLetter)
class EmailLetterAdmin(admin.ModelAdmin):
    readonly_fields = [
        'sent_at',
        'is_opened',
    ]
    list_display = [
        'text',
        'header',
        'clients'
    ]

    def clients(self, obj):
        return obj.clients.all().values('email')