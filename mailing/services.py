from datetime import datetime
from mailing.models import Category
from django.conf import settings
from django.core.cache import cache
from config import settings
from mailing.models import MailingLogs, Mailing


def send_mail(ms, message_client):
    result = send_mail(
        subject=ms.message.subject,
        message=ms.message.message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[message_client.client.email],
        fail_silently=False
    )

    MailingLogs.objects.create(
        status=MailingLogs.STATUS_OK if result else MailingLogs.STATUS_FAILED,
        settings=ms,
        client_id=message_client.client_id
    )

def send_mails():
    current_dt = datetime.datetime.now(datetime.timezone.utc)
    for ms in Mailing.objects.filter(status=Mailing.START):
        for mc in ms.mailingclient_set.all():
            ml = MailingLogs.objects.filter(client=mc.client, settings=ms)
            if ml.exists():
                last_day = ml.order_by('-last try').first().last_try
                if ms.period == Mailing.DAILY:
                    if (current_dt - last_day) >= 1:
                        send_mail(ms, mc)
                elif ms.period == Mailing.WEEKLY:
                    if (current_dt - last_day) >= 7:
                        send_mail(ms, mc)
                elif ms.period == Mailing.MONTHLY:
                    if (current_dt - last_day) >= 30:
                        send_mail(ms, mc)
            else:
                send_mail(ms, mc)


def get_categories_cache():

    if settings.CACHE_ENABLED:
        key = 'categories'
        category_list = cache.get(key)
        if category_list is None:
            category_list = Category.objects.all()
            cache.set(key, category_list)
    else:
        category_list = Category.objects.all()

    return category_list
