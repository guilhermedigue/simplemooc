from django.contrib import admin

# Register your models here.
from .models import Courses, Enrollment, Announcement, Comment, Lesson, Material


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class MaterilInlineAdmin(admin.TabularInline):
    model = Material


class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'number', 'course', 'release_date']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    inlines = [
        MaterilInlineAdmin
    ]


admin.site.register(Courses, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])
admin.site.register(Lesson, LessonAdmin)
