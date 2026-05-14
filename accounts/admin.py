from django.contrib import admin
from .models import StudentProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'roll_no', 'semester', 'created_at')
    search_fields = ('user__username', 'roll_no')
    list_filter = ('semester', 'created_at')