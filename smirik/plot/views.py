from io import BytesIO
import base64

import matplotlib.pyplot as plt
from django.shortcuts import render
from pandas import Series

from plot.models import DataCache


def main(request):
    qs = DataCache.objects.filter(paper__client=request.user)
    Series.plot()
    base64.b64encode(image)
    st.seek(0)
    plt.close()
    pass
