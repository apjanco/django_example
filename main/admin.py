from django.contrib import admin
from main.models import *


# Register your models here.
class MadLibAdmin(admin.ModelAdmin):
    pass
admin.site.register(MadLib, MadLibAdmin)


class SpanAdmin(admin.ModelAdmin):
    pass
admin.site.register(Span, SpanAdmin)