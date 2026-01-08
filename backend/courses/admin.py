from django.contrib import admin
from .models import Course, Lesson, Enrollment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Course model.
    Provides a clear and manageable view of courses with search, filtering,
    and detailed list display.
    """
    list_display = ('title', 'price', 'created_at', 'updated_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Lesson model.
    Enhances the management of lessons by allowing searching and filtering,
    and displaying key information in the list view.
    """
    list_display = ('title', 'course', 'created_at', 'updated_at')
    search_fields = ('title', 'course__title')
    list_filter = ('course', 'created_at')
    ordering = ('-created_at',)

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Enrollment model.
    Offers a streamlined view of user enrollments, with functionalities
    to search and filter by user or course.
    """
    list_display = ('user', 'course', 'enrolled_at')
    search_fields = ('user__username', 'course__title')
    list_filter = ('enrolled_at', 'course')
    ordering = ('-enrolled_at',)
    autocomplete_fields = ('user', 'course')
