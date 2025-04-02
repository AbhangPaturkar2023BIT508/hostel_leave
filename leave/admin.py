from django.contrib import admin
from .models import HostelUser, LeaveApplication
from django.contrib.auth.hashers import make_password, check_password

# Register your models here.

class HostelUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'contact', 'address')
    search_fields = ('username', 'email', 'role')
    list_filter = ('role',)

    # Custom save method to hash password before saving it
    def save_model(self, request, obj, form, change):
        if obj.password:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

admin.site.register(HostelUser, HostelUserAdmin)

class LeaveApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'start_date', 'end_date', 'status')
    list_filter = ('status', 'student')
    search_fields = ('student__username', 'status')

admin.site.register(LeaveApplication, LeaveApplicationAdmin)
