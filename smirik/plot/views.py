from io import BytesIO
import base64
from decimal import Decimal

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
    first_prices = {}
    prices = array()
    dates = array()
    curr_paper = ''
    for item in data:
        if curr_paper != item['paper__name']:
            first_prices
            if len(prices) > 0:
                ticks[curr_paper] = Series(prices, index=dates, name=curr_paper)
            curr_paper = item['paper__name']
            prices = array()
            dates = array()
        prices.append(item['price'])
        dates.append(item['date'])
    if len(array) > 0:
        ticks[curr_paper] = Series(prices, index=dates, name=curr_paper)
        del prices, dates, curr_paper


    Series.plot()
    base64.b64encode(image)
    st.seek(0)
    plt.close()
    pass
