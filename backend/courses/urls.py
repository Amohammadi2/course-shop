from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseListView, CourseDetailView, EnrollCourseView, StreamVideoView,
    AdminCourseViewSet, AdminLessonViewSet
)

# Admin router
admin_router = DefaultRouter()
admin_router.register(r'courses', AdminCourseViewSet)
admin_router.register(r'lessons', AdminLessonViewSet)

urlpatterns = [
    # Public and user-facing URLs
    path('', CourseListView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:course_id>/enroll/', EnrollCourseView.as_view(), name='enroll-course'),
    path('lessons/<int:lesson_id>/stream/', StreamVideoView.as_view(), name='stream-video'),

    # Admin URLs
    path('admin/', include(admin_router.urls)),
]
