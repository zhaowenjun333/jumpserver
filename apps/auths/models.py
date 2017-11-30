# -*- coding: utf-8 -*-
#

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _
from rest_framework.authtoken.models import Token
from django.conf import settings


class AccessKey(models.Model):
    id = models.UUIDField(verbose_name='AccessKeyID', primary_key=True,
                          default=uuid.uuid4, editable=False)
    secret = models.UUIDField(verbose_name='AccessKeySecret',
                              default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User',
                             related_name='access_key')

    def get_id(self):
        return str(self.id)

    def get_secret(self):
        return str(self.secret)

    def __str__(self):
        return str(self.id)


class PrivateToken(Token):
    """
    Inherit from auth token, otherwise migration is boring
    """

    class Meta:
        verbose_name = _('Private Token')


class LoginLog(models.Model):
    LOGIN_TYPE_CHOICE = (
        ('W', 'Web'),
        ('ST', 'SSH Terminal'),
        ('WT', 'Web Terminal')
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=20, verbose_name=_('Username'))
    name = models.CharField(max_length=20, blank=True, verbose_name=_('Name'))
    login_type = models.CharField(choices=LOGIN_TYPE_CHOICE, max_length=2,
                                  verbose_name=_('Login type'))
    login_ip = models.GenericIPAddressField(verbose_name=_('Login ip'))
    login_city = models.CharField(max_length=254, blank=True, null=True,
                                  verbose_name=_('Login city'))
    user_agent = models.CharField(max_length=254, blank=True, null=True,
                                  verbose_name=_('User agent'))
    date_login = models.DateTimeField(auto_now_add=True,
                                      verbose_name=_('Date login'))

    class Meta:
        db_table = 'login_log'
        ordering = ['-date_login', 'username']