#coding: utf8
import calendar
from io import BytesIO
from datetime import datetime, time
from decimal import Decimal
from collections import defaultdict

import matplotlib.pyplot as plt
from django.shortcuts import render
from pandas import Series, DataFrame

from plot.models import DataCache


def main(request):
    all_dates = set()
    data = DataCache.objects.values('paper__name', 'date', 'price') \
                            .order_by('paper' ,'date')
    ticks = {}
# TODO: need work it!
    obj_time = time()
    first_price = 0
    prices = []
    dates = []
    curr_paper = ''
    portfolio_by_month = defaultdict(list)
    portfolio_by_month_dates = set()
    prev_month = (100, 1)  # year, month
    last_price = .0
    curr_date = datetime.now()
    is_init = False
    for item in data:
        if curr_paper != item['paper__name']:
            first_price = item['price']
            portfolio_by_month[item['paper__name']] = []
            if len(prices) > 0:
                s = Series(prices, index=dates, name=curr_paper, dtype='float32')
                s.plot(label=curr_paper)
            prices = []
            dates = []
            if is_init:
                portfolio_by_month[curr_paper].append(last_price)
                portfolio_by_month_dates.add(curr_date)
            curr_paper = item['paper__name']
            prev_month = (item['date'].year, item['date'].month)  # year, month
            last_price = item['price']
            is_init = True
        prices.append(item['price'] - first_price)
        curr_date = datetime.combine(item['date'], obj_time)
        dates.append(curr_date)
        curr_month = (item['date'].year, item['date'].month)
        if curr_month > prev_month:
            last_day = calendar.monthrange(*prev_month)[1]
            portfolio_by_month[curr_paper].append(last_price)
            portfolio_by_month_dates.add(datetime(prev_month[0], prev_month[1], last_day))
            prev_month = curr_month
        last_price = item['price']
    s = Series(prices, index=dates, name=curr_paper, dtype='float32')
    s.plot(label=curr_paper)

    last_day = calendar.monthrange(*prev_month)[1]
    portfolio_by_month[curr_paper].append(last_price)
    portfolio_by_month_dates.add(curr_date)
    del prices, dates, curr_paper, s

    img_file = BytesIO()
    figure = plt.gcf()
    figure.set_size_inches(15, 8)
    plt.legend(loc=2)
    plt.ylabel('Change of price, $')
    plt.xlabel('Date')
    plt.title("Report portfolio vs time")
    plt.savefig(img_file, format='svg', dpi=100)
    plt.close()
    
    frame = DataFrame(portfolio_by_month, index=portfolio_by_month_dates)
    frame['total'] = sum((frame[col] for col in frame.columns))
    frame = frame.sort_index()

    t_data = {'img': img_file.getvalue(),
              'table': frame}
    return render(request, 'main.html', t_data)
