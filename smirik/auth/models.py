# coding: utf8
from django.contrib.auth.models import AbstractUser
from django.db import models


class NegotiablePaper(models.Model):
    """ negotiable papers """
    name = models.CharField(u"name of negotiable paper",
                            max_length=20,
                            unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'negotiable paper'
        verbose_name_plural = u'negotiables papers'


class Client(AbstractUser):
    """ clients """
    papers = models.ManyToManyField(NegotiablePaper, verbose_name=u'negotiable papers')

    class Meta:
        verbose_name = u'client'
        verbose_name_plural = u'clients'
