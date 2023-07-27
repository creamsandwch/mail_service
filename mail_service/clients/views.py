import json

from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.generic import FormView

from clients.forms import SendLetterForm, EmailForm, ClientForm


class SendMail(FormView):
    form = SendLetterForm()

    def form_valid(self, form):
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


class CreateEmailForm(FormView):
    template_name = 'form_ajax.html'
    form_class = EmailForm

    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """
        text = form.cleaned_data['text']
        header = form.cleaned_data['header']
        form.save()
        return JsonResponse({"text": text, "header": header}, status=200)

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)
    

class CreateClientForm(FormView):
    template_name = 'form_ajax.html'
    form_class = ClientForm

    def form_valid(self, form):
        """
        If the form is valid return HTTP 200 status
        code along with name of the user
        """
        first_name = form.cleaned_data.get('first_name', None)
        last_name = form.cleaned_data.get('last_name', None)
        email = form.cleaned_data['email']
        birthday = form.cleaned_data.get('birthday')
        form.save()
        return JsonResponse(
            {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "birthday": birthday,
            },
            status=200
        )

    def form_invalid(self, form):
        """
        If the form is invalid return status 400
        with the errors.
        """
        errors = form.errors.as_json()
        return JsonResponse({"errors": errors}, status=400)