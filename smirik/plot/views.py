#coding: utf8
import base64
from io import BytesIO
from decimal import Decimal
from collections import defaultdict

import matplotlib.pyplot as plt
from django.shortcuts import render
from pandas import Series, DataFrame
from numpy import array

from plot.models import DataCache


def main(request):
    data = DataCache.objects.values('paper__name', 'date', 'price') \
                            .order_by('paper' ,'date')
    ticks = {}
# TODO: need work it!
    first_price = 0
    prices = array()
    dates = array()
    curr_paper = ''
    portfolio_by_month = defaultdict(list)
    portfolio_by_month_dates = set()
    prev_month = (1, 100)  # month, year
    for item in data:
        if curr_paper != item['paper__name']:
            first_price = item['price']
            portfolio_by_month[item['paper__name']] = []
            if len(prices) > 0:
                s = Series(prices, index=dates, name=curr_paper)
                s.plot(label=curr_paper)
            curr_paper = item['paper__name']
            prices = array()
            dates = array()
        prices.append(item['price'] - first_price)
        dates.append(item['date'])
        curr_month = (item['date'].month, item['date'].year)
        if curr_month > prev_month:
            portfolio_by_month[curr_paper].append(item['price'])
            portfolio_by_month_dates.add(item['date'])
    s = Series(prices, index=dates, name=curr_paper)
    s.plot(label=curr_paper)

    portfolio_by_month[curr_paper].append(item['price'])
    portfolio_by_month_dates.add(item['date'])
    del prices, dates, curr_paper, s

    img_file = BytesIO()
    plt.savefig(img_file, format='svg')
    plt.close()
    img_file = base64.b64encode(img_file.getvalue())

    frame = DataFrame(portfolio_by_month, index=portfolio_by_month_dates)
    frame['total'] = sum((frame[col] for col in frame.columns))

    t_data = {'img': img_file,
              'table': frame}
    return render(request, 'main.html', t_data)
    #Series.plot()
    #base64.b64encode(image)
    #st.seek(0)
    #plt.close()
