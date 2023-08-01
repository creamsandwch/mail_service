#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy

from .forms import SendLetterForm, EmailForm, ClientForm
from .tasks import celery_send_mail
from .models import EmailLetter, Client


def manage_mail_service_view(request):
    email_form = EmailForm()
    client_form = ClientForm()
    send_form = SendLetterForm()

    if request.method == 'POST':
        if 'header' in request.POST:
            email_form = EmailForm(request.POST)

            if not email_form.is_valid():
                errors = email_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)

            email_form.save()
            return JsonResponse(email_form.cleaned_data, status=200)

        if 'email' in request.POST:
            client_form = ClientForm(request.POST)

            if not client_form.is_valid():
                errors = client_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)

            client_form.save()
            return JsonResponse(
                client_form.cleaned_data,
                status=200
            )

        if 'send_datetime' in request.POST:
            send_form = SendLetterForm(request.POST)

            if not send_form.is_valid():
                errors = send_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)

            send_form.is_valid()

            letter = send_form.cleaned_data.get('letter')
            clients = send_form.cleaned_data.get('clients')

            for client in clients:
                client.letters.add(letter)
                client.save()

            data = {}
            data['subject'] = letter.header
            data['message'] = letter.text
            data['recipient_list'] = [
                client.email for client in clients
            ]

            date_to_send = send_form.cleaned_data.get('send_datetime')
            delay = (date_to_send - timezone.now()).total_seconds()
            if delay > 0:
                celery_send_mail.apply_async(
                    args=[data], countdown=delay
                )
            else:
                celery_send_mail.apply_async(
                    args=[data],
                )

            return JsonResponse(
                {
                    "letter": letter.header,
                    "clients": data.get('recipient_list'),
                },
                status=200
            )
    default_client = Client(
        first_name='Имя',
        last_name='Фамилия',
        email='example@example.com',
    )
    default_letter = EmailLetter(
        header='Заголовок',
        text='Текст письма',
        footer='Подпись',
    )

    context = {
            'client_form': client_form,
            'email_form': email_form,
            'send_form': send_form,
            'default_letter': default_letter,
            'default_client': default_client
        }
    return render(
        request,
        'form_ajax.html',
        context=context
    )


class ClientListView(ListView):
    template_name = 'list.html'
    model = Client
    context_object_name = 'clients_list'


class LetterListView(ListView):
    template_name = 'list.html'
    model = EmailLetter
    context_object_name = 'letters_list'


class ClientUpdateView(UpdateView):
    template_name = "edit.html"
    model = Client
    form_class = ClientForm
    context_object_name = 'client_edit'
    success_url = reverse_lazy('clients:clients_list')


class EmailUpdateView(UpdateView):
    template_name = "edit.html"
    model = EmailLetter
    form_class = EmailForm
    context_object_name = 'letter_edit'
    success_url = reverse_lazy('clients:letters_list')
