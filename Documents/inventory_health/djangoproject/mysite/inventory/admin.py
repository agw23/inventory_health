# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
#from .forms import IPForm
from .models import IP
from .models import Autodiscover

# Register your models here.

from .models import IP
from .models import Autodiscover

class newAdmin(admin.ModelAdmin):
    #search_fields = ["IP_address", "IP_serial"]
    list_filter = ["IP_address", "IP_address_auto", "IP_serial"]
    search_fields = ["IP_address", "IP_serial", "IP_address_auto",]
    #list_filter = ["IP_address", "IP_serial"]
    #form = IPForm


admin.site.register(IP,newAdmin)
admin.site.register(Autodiscover)
