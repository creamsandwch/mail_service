from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse

from clients.forms import SendLetterForm, EmailForm, ClientForm
from clients.models import Client, EmailLetter


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
                erorrs = send_form.errors.as_json()
                return JsonResponse({"errors": errors}, status=400)

            letter = send_form.cleaned_data.get('email')
            clients = send_form.cleaned_data.get('clients')

            letter.clients.clear()
            letter.clients.add(*clients)
            letter.save()
            
            send_mail(
                subject=letter.header,
                message=letter.text,
                from_email=settings.FROM_EMAIL,
                recipient_list=[
                    client.email for client in clients
                ],
                fail_silently=False
            )
            return JsonResponse(
                {
                    "letter": letter,
                    "clients": clients,
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
