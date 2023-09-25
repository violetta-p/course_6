from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from config import settings
from mailing.models import MailingLogs, Mailing
from django.core.mail import send_mail


def send_email(ms, message_client):
    try:
        send_mail(
            subject=ms.message.client,
            message=ms.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[message_client.client.email]
                  )
        result = True
    except Exception:
        result = False

    MailingLogs.objects.create(
        status=MailingLogs.STATUS_OK if result else MailingLogs.STATUS_FAILED,
        settings=ms,
        client_id=message_client.client_id
    )

def send_mails():
    current_dt = datetime.now(timezone.utc)
    for mailing_setting in Mailing.objects.filter(status=Mailing.START):
        for mc in mailing_setting.client.all():
            ml = MailingLogs.objects.filter(client=mc.client, settings=mailing_setting)
            if ml.exists():
                last_day = ml.order_by('-last try').first().last_try
                if mailing_setting.frequency == Mailing.DAILY:
                    if (current_dt - last_day) >= 1:
                        send_email(mailing_setting, mc)
                elif mailing_setting.frequency == Mailing.WEEKLY:
                    if (current_dt - last_day) >= 7:
                        send_email(mailing_setting, mc)
                elif mailing_setting.frequency == Mailing.MONTHLY:
                    if (current_dt - last_day) >= 30:
                        send_email(mailing_setting, mc)
            else:
                send_email(mailing_setting, mc)


def start_job():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mails, "interval", minutes=10)
    scheduler.start()
