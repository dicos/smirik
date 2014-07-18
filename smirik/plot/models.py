#coding: utf8
from django.db import models

from auth.models import NegotiablePaper


class DataCache(models.Model):
    """ cache data from yahoo finance service """
    paper = models.ForeignKey(NegotiablePaper, verbose_name=u'name of paper')
    date = models.DateField(verbose_name=u'date of ticket')
    price = models.DecimalField(max_digits=8,
                                decimal_places=6,
                                verbose_name=u'price of negotiable paper')
    
    class Meta:
        verbose_name = u'cache data by day portfolio'
        unique_together = ('paper', 'date',)
