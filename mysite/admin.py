from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
class MyUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name','last_name','email', 'password')}),
        ('Permissions', {'fields': ('is_superuser','is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name','last_name','email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(Myusers,MyUserAdmin)
admin.site.register(UserProfile)
admin.site.register(Booking)
admin.site.register(RentRegister)
admin.site.register(RentImages)
admin.site.register(Vehicle)
admin.site.register(Report)
admin.site.register(ReportImages)
admin.site.register(SlotsPlace)
