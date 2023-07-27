# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'first_name',
        'last_name',
        'email',
        'birthday',
        'date_joined'
    ]
    readonly_fields = [
        'date_joined',
        'id'
    ]
    list_display = [
        'id',
        'full_name',
        'email',
        'date_joined'
    ]

    def full_name(self, obj):
        return obj.first_name + ' ' + obj.last_name
