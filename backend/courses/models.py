from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Course(models.Model):
    """
    Represents an educational course available for purchase.
    Each course has a title, description, a price in credits, and an optional
    thumbnail image.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    thumbnail = models.ImageField(upload_to='course_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Lesson(models.Model):
    """
    Represents a single lesson within a course.
    Each lesson is tied to a specific course and contains a reference to the
    video content. The video reference is a path and not a direct URL to

    ensure it can be served securely.
    """
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    # This field will store a path or a reference to the video,
    # not a public URL, to be used by the secure streaming endpoint.
    video_reference = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at'] # Ensure lessons are ordered chronologically

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Enrollment(models.Model):
    """
    Links a user to a course they have purchased.
    This model acts as a junction table, creating a many-to-many relationship
    between Users and Courses. It signifies that a user has access to a course.
    A unique constraint ensures a user can only enroll in a course once.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course') # A user can only enroll in a course once

    def __str__(self):
        return f"{self.user.username} enrolled in {self.course.title}"
