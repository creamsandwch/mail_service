import datetime
from django import forms

from clients.models import Client, EmailLetter


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailLetter
        fields = [
            'header',
            'text'
        ]

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'first_name',
            'last_name',
            'email',
            'birthday',
        ]


class SendLetterForm(forms.Form):
    clients = forms.ModelMultipleChoiceField(
        label='Choose subscribers for sending to',
        queryset=Client.objects.all(),
        widget=forms.widgets.SelectMultiple(attrs={'class': 'form-control'})
    )
    adresses = forms.ModelChoiceField(
        label='Choose email letter to send',
        queryset=EmailLetter.objects.all(),
        widget=forms.widgets.Select(attrs={'class': 'form-control'})
    )
    send_datetime = forms.DateTimeField(
        label='Send time in Europe/Moscow (default: now)',
        required=False,
        initial=format(datetime.datetime.now(),'%Y-%m-%d %H:%M'),
    )
