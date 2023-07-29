from rest_framework import serializers
from clients.models import EmailLetter


class EmailLetterSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()

    class Meta:
        model = EmailLetter
        fields = [
            'id',
            'header',
            'text',
            'footer',
            'sent_at',
            'is_opened',
        ]

    def get_text(self, obj):
        return obj.text[:30]

