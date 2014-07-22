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


def plot_paper(prices, dates, paper_name):
    """ plot current negotiable paper """
    Series(prices, index=dates, name=paper_name, dtype='float32').plot()


def call_main(qs):
    """ prepare adata for report "portfolio by months" and 
        plotting report "portfolio vs time" """
    #  initialize data
    ticks = {}
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

    def update_portfolio_data(paper_name, price, tick_date):
        """ update data portfolio_by_month and portfolio_by_month_dates """
        portfolio_by_month[paper_name].append(price)
        portfolio_by_month_dates.add(tick_date)

    for item in qs:
        if curr_paper != item['paper__name']:
            first_price = item['price']
            portfolio_by_month[item['paper__name']] = []
            if len(prices) > 0:
                plot_paper(prices, dates, curr_paper)
            prices = []
            dates = []
            if is_init:
                update_portfolio_data(curr_paper, last_price, curr_date)
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
            last_month = datetime(prev_month[0], prev_month[1], last_day)
            update_portfolio_data(curr_paper, last_price, last_month)
            prev_month = curr_month
        last_price = item['price']
    plot_paper(prices, dates, curr_paper)

    portfolio_by_month[curr_paper].append(last_price)
    portfolio_by_month_dates.add(curr_date)

    portfolio_by_month_dates = list(portfolio_by_month_dates)
    portfolio_by_month_dates.sort()
    return portfolio_by_month, portfolio_by_month_dates


def main(request):
    """ plotting reports "portfolio vs time" and "portfolio by months" """

    data = DataCache.objects.values('paper__name', 'date', 'price') \
                            .order_by('paper' ,'date')

    portfolio_by_month, index = call_main(data)
    # polotting report "portfolio vs time"
    img_file = BytesIO()
    figure = plt.gcf()
    figure.set_size_inches(15, 8)
    plt.legend(loc=2)
    plt.ylabel('Change of price, $')
    plt.xlabel('Date')
    plt.title("Report portfolio vs time")
    plt.savefig(img_file, format='svg', dpi=100)
    plt.close()
    
    # generate table "portfolio by month"
    frame = DataFrame(portfolio_by_month, index=index)
    frame['total'] = sum((frame[col] for col in frame.columns))

    t_data = {'img': img_file.getvalue(),
              'table': frame}
    return render(request, 'main.html', t_data)
