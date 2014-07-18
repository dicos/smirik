#coding: utf8
from datetime import datetime, date, timedelta
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
import pandas.io.data as web

from auth.models import NegotiablePaper
from plot.models import DataCache


class Command(BaseCommand):
    help = 'Load data from yahoo finance into DataCache model'
    option_list = BaseCommand.option_list + (
        make_option('--clear', action="clear", default=None, dest='clear_cache'),
    )

    def delete_cache(self):
        DataCache.objects.all().delete()

    def handle(self, *args, **options):
        if options['delete_cache']:
            self.delete_cache

        if (options['export_chargings'] or
            options['export_other_operations'] or
            options['export_loan_operations'] or
            options['export_insurance_operations'] or
            options['export_chargings_zipped'] or
            options['export_write_offs']):

            months = []
            if len(args) == 2:
                for arg in args:
                    try:
                        dt = datetime.strptime(arg, '%Y-%m-%d')
                    except:
                        print "wrong data format format, need YYYY-MM-DD"
                        raise
                    else:
                        months.append(dt)
            else:
                months = [date(2001, 1, 1), (date.today() - timedelta(days=1))]

            all_data = {}
            for ticker in NegotiablePaper.objects.all():
                data_series = web.get_data_yahoo(ticker.name, months[0], months[1])
                cache_gen = {DataCache(paper=ticker,
                                       date=ind,
                                       price=data_series.Close[ind] \
                                for ind in data_series.index)}
                DataCache.objects.bulk_create(cache_gen)
