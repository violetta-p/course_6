from django.db import models

import users
from config import settings

NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=50, db_index=True, verbose_name='Category name')
    description = models.TextField(verbose_name='Category description', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Client(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Name', **NULLABLE)
    last_name = models.CharField(max_length=100, verbose_name='Last name', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='Email address')
    comment = models.TextField(verbose_name='Comment', **NULLABLE)
    is_active = models.BooleanField(default=True, verbose_name='Activity')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Author')

    def __str__(self):
        return f"{self.first_name}, {self.last_name}: {self.email}"

    class Meta:
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'


class Message(models.Model):
    topic = models.CharField(max_length=200, verbose_name='Topic')
    message = models.TextField(verbose_name='Message body')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, **NULLABLE, verbose_name='Author')
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    def __str__(self):
        return self.topic

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'


class Mailing(models.Model):

    FREQUENCY = (('DAILY', 'Every day'),
                 ('WEEKLY', 'Once a week'),
                 ('MONTHLY', 'Once a month'))

    DAILY = 'daily'
    WEEKLY = 'weekly'
    MONTHLY = 'monthly'

    CREATE = 'created'
    START = 'started'
    FINISH = 'done'

    STATUS = (('FINISH', 'Finished'),
              ('CREATE', 'Created'),
              ('START', 'Started'))

    create_date = models.DateField(auto_now_add=True, verbose_name='Created')
    sending_time = models.TimeField(default='00:00', verbose_name='Time of sending mailings')
    frequency = models.CharField(max_length=50, choices=FREQUENCY, verbose_name='Interval', default='daily')
    status = models.CharField(max_length=50, choices=STATUS, verbose_name='Status', default=CREATE)
    client = models.ManyToManyField(Client, verbose_name='Client')
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Message', **NULLABLE)
    finish_date = models.DateField(verbose_name='Termination date', default='2025-01-01')
    finish_time = models.TimeField(verbose_name='Termination time', default='00:00')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='Author')
    is_active = models.BooleanField(default=True, verbose_name='Activity') # поле для блокировки рассылки менеждером.
    # пользователь не может самостоятельно включить рассылку, заблокированную менеджером

    def __str__(self):
        return self.pk

    def make_not_active(self, *args, **kwargs):
        self.status = 'FINISH'
        self.save()

    class Meta:
        verbose_name = 'Mailing'
        verbose_name_plural = 'Mailings'
        ordering = ('id',)


class MailingLogs(models.Model):

    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'

    STATUS = ((STATUS_OK, 'Success'),
              (STATUS_FAILED, 'Failure'))

    last_try = models.DateTimeField(auto_now_add=True, verbose_name='The last attempt')
    status = models.CharField(max_length=30, default=STATUS_OK, choices=STATUS, verbose_name='Status')
    mail_settings = models.ForeignKey('Mailing', on_delete=models.CASCADE, verbose_name='Mailing')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client')

    def __str__(self):
        return self.pk

    class Meta:
        verbose_name = 'Mailing log'
        verbose_name_plural = 'Mailing logs'


class MessageVersion(models.Model):
    product = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name='Message')
    version_number = models.PositiveSmallIntegerField(verbose_name='Version number')
    version_name = models.CharField(max_length=100, verbose_name='Version name')
    is_active = models.BooleanField(verbose_name='Flag of the current version')

    def __str__(self):
        return f'{self.version_number}: {self.version_name}'
