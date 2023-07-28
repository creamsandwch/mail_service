import logging

from django.shortcuts import render
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import get_object_or_404

from clients.forms import SendLetterForm, EmailForm, ClientForm
from clients.tasks import celery_send_mail
from clients.models import EmailLetter


def manage_mail_service_view(request):
    email_form = EmailForm()
    client_form = ClientForm()
    send_form = SendLetterForm()
    
    if request.method == 'POST' and request.is_ajax():
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

        if 'adresses' in request.POST:
            send_form = SendLetterForm(request.POST)
            
            if not send_form.is_valid():
                errors = send_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)

            header = send_form.cleaned_data.get('adresses')
            letter = get_object_or_404(EmailLetter, header=header)
            clients = send_form.cleaned_data.get('clients')

            letter.clients.clear()
            letter.clients.add(*clients)
            letter.save()

            data = {}
            data['subject'] = letter.header
            data['message'] = letter.text
            data['recipient_list'] = [
                client.email for client in clients
            ]

            date_to_send = send_form.cleaned_data.get('send_datetime')
            delay = (timezone.now() - date_to_send).total_seconds()
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
    
    return render(
        request,
        'form_ajax.html',
        context={
            'client_form': client_form,
            'email_form': email_form,
            'send_form': send_form
        }
    )
