#coding: utf8
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_FLOOR
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
import pandas.io.data as web

from common_helpers import nested_commit_on_success
from auth.models import NegotiablePaper
from plot.models import DataCache


class Command(BaseCommand):
    help = 'Load data from yahoo finance into DataCache model'
    option_list = BaseCommand.option_list + (
        make_option('-c',
                    '--clear',
                    action="store_true",
                    default=False,
                    dest="clear"),
    )
    quantize = Decimal('0.01')  # round quantize of price

    def clear(self):
        DataCache.objects.all().delete()

    def get_price(self, value):
        """ get rounding price (convert float64 to Decimal) """
        return Decimal(value).quantize(self.quantize, rounding=ROUND_FLOOR)

    @nested_commit_on_success
    def handle(self, *args, **options):
        if options['clear']:
            self.clear()

        months = []
        if len(args) == 2:
            for arg in args:
                try:
                    dt = datetime.strptime(arg, '%Y-%m-%d')
                except:
                    print("wrong data format format, need YYYY-MM-DD")
                    raise
                else:
                    months.append(dt)
        else:
            months = [date(2014, 1, 1), (date.today() - timedelta(days=1))]

        all_data = {}
        quantize = Decimal('0.01')
        for ticker in NegotiablePaper.objects.all():
            data_series = web.get_data_yahoo(ticker.name,
                                             months[0],
                                             months[1])
            cache_gen = [DataCache(paper=ticker,
                                   date=ind,
                                   price=self.get_price(data_series.Close[ind])) \
                            for ind in data_series.index]
            DataCache.objects.bulk_create(cache_gen)
