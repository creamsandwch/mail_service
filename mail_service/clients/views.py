import json

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import FormView

from clients.forms import SendLetterForm, EmailForm
from clients.models import Client, EmailLetter



def AjaxFormMixin(FormView):
    template_name = 'form_ajax.html'

    def form_valid(self, form):
        form.save()
        return HttpResponse('OK')

    def form_invalid(self, form):
        errors_dict = json.dumps(dict([(k, [e for e in v]) for k, v in form.errors.items()]))
        return HttpResponseBadRequest(json.dumps(errors_dict))

def send_email_form(AjaxFormMixin):
    form_class = SendLetterForm
    letter = form.cleaned_data.get('email')
    clients = form.cleaned_data.get('clients')
            
    letter.clients.clear()
    letter.clients.add(*clients)

    send_mail(
        subject=letter.header,
        message=letter.text,
        from_email=settings.FROM_EMAIL,
        recipient_list=[
            client.email for client in clients
        ],
        fail_silently=False
    )
