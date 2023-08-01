# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Client, EmailLetter


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
        return obj.letters.all().values('text')

    def full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name


@admin.register(EmailLetter)
class EmailLetterAdmin(admin.ModelAdmin):
    readonly_fields = [
        'sent_at',
        'is_opened',
        'client',
    ]
    list_display = [
        'id',
        'text',
        'header',
        'client'
    ]
