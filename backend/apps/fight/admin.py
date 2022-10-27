from django.contrib import admin

# Register your models here.
from ..fight.models.fight import Fight, History

admin.site.register(Fight)


admin.site.register(History)