# coding: utf8
from django.contrib import admin

from .models import Client, NegotiablePaper


admin.site.register([Client, NegotiablePaper])
