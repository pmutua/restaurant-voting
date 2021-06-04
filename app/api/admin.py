from django.contrib import admin
from api.models import *
# Register your models here.
admin.site.register(Role)
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Restaurant)
# admin.site.register(Menu)
admin.site.register(Vote)


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id','restaurant', 'file','votes','created_at')


admin.site.register(Menu, MenuAdmin)


