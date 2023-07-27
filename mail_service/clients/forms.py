from django import forms

from clients.models import Client, EmailLetter


class EmailForm(forms.ModelForm):
    class Meta:
        model = EmailLetter
        fields = [
            'text',
            'header',
        ]

class SendLetterForm(forms.Form):
    clients = forms.ModelMultipleChoiceField(
        label='Choose subscribers for sending to',
        queryset=Client.objects.all(),
        widget=forms.widgets.SelectMultiple(attrs={'class': 'form-control'})
    )
    email = forms.ModelChoiceField(
        label='Choose email letter to send',
        queryset=EmailLetter.objects.all(),
        widget=forms.widgets.Select(attrs={'class': 'form-control'})
    )
