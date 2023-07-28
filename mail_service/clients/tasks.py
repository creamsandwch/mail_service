#!/usr/local/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.template import Context
from django.template.loader import get_template
from smtplib import SMTPException

from mail_service.celeryapp import app as celery_app


logger = logging.getLogger(__name__)


@celery_app.task(
    default_retry_delay=settings.RETRY_PERIOD,
    max_retries=settings.MAX_RETRIES,
)
def celery_send_mail(data):
    """Delayed mail sending."""
    logger.info('task {} scheduled'.format(data.get('subject')))
    try:
        for recipient_email in data.get('recipient_list'):
            mail = EmailMessage(
                    subject=data.get('subject'),
                    body=data.get('message'),
                    from_email=settings.EMAIL_HOST_USER,
                    to=recipient_email,
                    reply_to=settings.EMAIL_HOST_USER,
                )
            mail.content_subtype = 'html'
            mail.send(fail_silently=False)
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
    
    
