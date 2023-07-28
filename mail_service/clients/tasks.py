import logging

from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
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
        send_mail(
            subject=data.get('subject'),
            message=data.get('message'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=data.get('recipient_list'),
            fail_silently=False
        )
        logger.info(
            'Mail with subject {} sent to {} successfully!'.format(
                data.get('subject'),
                data.get('recipient_list'),
            )
        )
    except BadHeaderError:
        logger.warning('Invalid header found.')
    except SMTPException:
        logger.warning('Error sending an email.')
    except Exception as error:
        logger.info('Mail sending failed: {}'.format(error))
    return
