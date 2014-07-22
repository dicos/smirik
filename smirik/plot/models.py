#coding: utf8
from django.db import models

from auth.models import NegotiablePaper


class DataCache(models.Model):
    """ cache data from yahoo finance service """
    paper = models.ForeignKey(NegotiablePaper, verbose_name=u'name of paper')
    date = models.DateField(verbose_name=u'date of ticket', db_index=True)
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name=u'price of negotiable paper')

    def __unicode__(self):
        data = (self.paper, self.date.strftime("%Y-%m-%d"), self.price)
        return "%s: %s -- %s" % data

    def __str__(self):
        return self.__unicode__()
    
    class Meta:
        verbose_name = u'cache data by day portfolio'
        unique_together = ('paper', 'date',)
