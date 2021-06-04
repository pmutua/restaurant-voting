from django.contrib import admin
from api.models import *
# Register your models here.
admin.site.register(Role)
admin.site.register(User)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'employee_no',
        'user',
        'created_at',
        'created_by'
    )


class RestaurantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'contact_no',
        'address',
        'created_at',
        'created_by'
    )


class MenuAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'restaurant',
        'file',
        'votes',
        'created_at'
    )


class VoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'menu', 'voted_at')


admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Vote, VoteAdmin)
