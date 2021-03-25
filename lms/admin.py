from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Course, Student, Faculty, Student_Course, Faculty_Course, Faculty_Assignment


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'is_staff', 'is_active','identification','designation','first_name','last_name','date_joined')
    list_filter = ('email', 'is_staff', 'is_active','identification','designation','first_name','last_name','date_joined')
    fieldsets = (
        (None, {'fields': ('email', 'password','identification','designation','first_name','last_name','date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','identification','designation','first_name','last_name','date_joined')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Course)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Student_Course)
admin.site.register(Faculty_Course)
admin.site.register(Faculty_Assignment)

