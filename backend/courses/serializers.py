from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    Used to list the lessons within a course. The video_reference is a
    sensitive field and should only be exposed to enrolled users, which will
    be handled by the view logic.
    """
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'video_reference', 'created_at')
        read_only_fields = ('id', 'created_at')


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for listing multiple courses.
    Provides a high-level overview of a course without the lesson details.
    """
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'thumbnail', 'created_at')
        read_only_fields = ('id', 'created_at')


class CourseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving a single course, including its lessons.
    This is intended for users who have access to the course content.
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'thumbnail', 'lessons', 'created_at')
        read_only_fields = ('id', 'lessons', 'created_at')

class AdminLessonSerializer(serializers.ModelSerializer):
    """
    Serializer for admin management of Lessons.
    Allows creating and updating lessons, including associating them with a course.
    """
    class Meta:
        model = Lesson
        fields = ('id', 'course', 'title', 'video_reference')

class AdminCourseSerializer(serializers.ModelSerializer):
    """
    Serializer for admin management of Courses.
    Allows creating and updating course details.
    """
    class Meta:
        model = Course
        fields = ('id', 'title', 'description', 'price', 'thumbnail')
