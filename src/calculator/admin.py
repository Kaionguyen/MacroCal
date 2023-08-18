from django.contrib import admin
from .models import UserStat, Diet, MacroDistribution

admin.site.register(UserStat)
admin.site.register(Diet)
admin.site.register(MacroDistribution)
