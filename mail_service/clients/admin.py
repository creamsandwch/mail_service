from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    fields = [
        'id',
        'email',
        'first_name',
        'last_name',
        'birthday_date',
        'joined_at'
    ]
    search_fields = [
        'email',
        'birthday_date',
        'joined_at',
    ]
    readonly_fields = [
        'joined_at',
    ]
