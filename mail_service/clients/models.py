# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Client(models.Model):
    """Модель клиента-получателя писем."""
    first_name = models.CharField(
        max_length=150,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='Фамилия'
    )
    email = models.EmailField(
        verbose_name='Адрес почты'
    )
    birthday = models.DateField(
        verbose_name='Дата рождения',
        blank=True,
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
    )
    letters = models.ManyToManyField(
        to='EmailLetter',
        related_name='clients'
    )

    def __str__(self):
        return str(self.email)


class EmailLetter(models.Model):
    text = models.TextField(
        max_length=1500,
        verbose_name='Текст письма',
        blank=False,
        null=False,
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
    received = models.BooleanField(
        default=False,
    )
