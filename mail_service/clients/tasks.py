#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.utils import timezone
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.shortcuts import get_object_or_404
from smtplib import SMTPException
from clients.models import EmailLetter

from mail_service.celeryapp import app as celery_app

logger = logging.getLogger(__name__)


@celery_app.task(
    default_retry_delay=settings.RETRY_PERIOD,
    max_retries=settings.MAX_RETRIES,
)
def celery_send_mail(data):
    """Delayed mail sending."""
    try:
        for recipient_email in data.get('recipient_list'):
            mail = EmailMessage(
                    subject=data.get('subject'),
                    body=data.get('message'),
                    from_email=settings.EMAIL_HOST_USER,
                    to=[recipient_email],
                    reply_to=[settings.EMAIL_HOST_USER],
                )
            mail.content_subtype = 'html'
            mail.send(fail_silently=False)

            letter = get_object_or_404(EmailLetter, header=data.get('subject'))
            letter.sent_at = timezone.now()
            letter.save()

            logger.info(
                'Mail with subject {} sent to {} successfully!'.format(
                    data.get('subject'),
                    recipient_email,
                )
            )

    except BadHeaderError:
        logger.warning('Invalid header found.')
    except SMTPException:
        logger.warning('Error sending an email.')
    except Exception as error:
        logger.info('Mail sending failed: {}'.format(error))
