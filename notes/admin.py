from django.contrib import admin
from .models import Subject, Unit, Note, Course

class UnitInline(admin.TabularInline):
    model = Unit
    extra = 1

class NoteInline(admin.TabularInline):
    model = Note
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [UnitInline]

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject',)
    inlines = [NoteInline]

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'unit', 'uploaded_at')
    list_filter = ('unit__subject', 'unit')
    search_fields = ('title', 'description')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "difficulty", "target_exam", "created_at")
    prepopulated_fields = {"slug": ("title",)}    