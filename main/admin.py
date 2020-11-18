from django.contrib import admin
from main.models import *


# Register your models here.
class MadLibAdmin(admin.ModelAdmin):
    autocomplete_fields = ['spans']
admin.site.register(MadLib, MadLibAdmin)


class SpanAdmin(admin.ModelAdmin):
    search_fields = ['text']
    list_filter = ['pos']
admin.site.register(Span, SpanAdmin)