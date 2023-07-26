from django.db import models
from django.utils.translation import gettext_lazy as _


class Client(models.Model):
    first_name = models.CharField(
        verbose_name=_('Имя клиента'),
        max_length=50,
    )
    last_name = models.CharField(
        verbose_name=_('Фамилия клиента'),
        max_length=50,
    )
    email = models.EmailField(
        verbose_name=_('Адрес электронной почты'),
    )
    birthday_date = models.DateField(
        verbose_name=_('День рождения'),
        blank=True,
    )
    joined_at = models.DateTimeField(
        auto_now_add=True,
    )
