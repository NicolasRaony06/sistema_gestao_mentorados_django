from django.contrib import admin
from . models import Navigators, Mentorados, ScheduleAvailability

admin.site.register(Navigators)
admin.site.register(Mentorados)
admin.site.register(ScheduleAvailability)