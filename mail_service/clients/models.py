#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Client(models.Model):
    """Модель клиента-получателя писем."""
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия',
    )
    email = models.EmailField(
        verbose_name='Адрес почты',
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.email)


@python_2_unicode_compatible
class EmailLetter(models.Model):
    text = models.TextField(
        max_length=1500,
        verbose_name='Текст письма',
        blank=False,
        null=False,
    )
    footer = models.CharField(
        max_length=150,
        verbose_name='Футер',
        blank=True,
        null=True,
    )
    header = models.CharField(
        max_length=150,
        verbose_name='Заголовок',
        blank=True,
        null=True,
        unique=True,
    )
    sent_at = models.DateTimeField(
        verbose_name='Время отправки',
        blank=True,
        null=True,
    )
    is_opened = models.BooleanField(
        default=False,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='letters',
    )

    def __str__(self):
        return '{}: {}'.format(self.header, self.text[:15])
