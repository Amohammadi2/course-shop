from rest_framework import permissions
from .models import Enrollment, Course

class IsEnrolled(permissions.BasePermission):
    """
    Custom permission to only allow users who are enrolled in a course to view its details.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is enrolled in the course.
        """
        if not request.user.is_authenticated:
            return False

        # The object `obj` is a Course instance.
        # We need to check if an enrollment exists for the current user and this course.
        return Enrollment.objects.filter(user=request.user, course=obj).exists()
