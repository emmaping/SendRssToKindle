from django.contrib import admin

# Register your models here.
from SendRssToKindle.models import *

admin.site.register(KindleUser)
admin.site.register(RSSList)
admin.site.register(RSSContent)