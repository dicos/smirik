#coding: utf8
from datetime import datetime, timedelta

from django.core.management import call_command
from django.test import TestCase

from auth.models import NegotiablePaper, Client
from plot.models import DataCache


class Cases(TestCase):
    def test_load_data(self):
        ''' test python manage.py get_data command 
            it command for load negotiable papers info into local database
            https://github.com/dicos/smirik/issues/3 '''
        paper_ibm = NegotiablePaper.objects.create(name='IBM')
        paper_aapl = NegotiablePaper.objects.create(name='AAPL')

        self.assertEqual(DataCache.objects.count(), 0)
        call_command('get_data')
        count_ibm = DataCache.objects.filter(paper=paper_ibm).count()
        self.assertGreater(count_ibm, 0)
        count_aapl = DataCache.objects.filter(paper=paper_aapl).count()
        self.assertGreater(count_aapl, 0)
        full_count = DataCache.objects.count()
        self.assertEqual(full_count, count_aapl + count_ibm)

        #  test with clear database
        call_command('get_data', '-c')
        call_command('get_data')
        self.assertEqual(full_count, DataCache.objects.all().count())
        call_command('get_data', '--clear')
        call_command('get_data')
        self.assertEqual(full_count, DataCache.objects.all().count())
        #  with data filtering
        call_command('get_data', '-c')
        call_command('get_data', '2013-01-01', '2013-01-31')
        new_full_count = DataCache.objects.count()
        self.assertLess(new_full_count, full_count)
        self.assertGreater(new_full_count, 0)
        date_range = datetime(2013, 1, 1), datetime(2013, 1, 31, 23, 59, 59)
        filtering_count = DataCache.objects.filter(date__range=date_range) \
                                           .count()
        self.assertEqual(filtering_count, new_full_count)
