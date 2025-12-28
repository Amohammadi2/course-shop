from django.db import transaction
from django.http import FileResponse, Http404
from django.conf import settings
from rest_framework import generics, viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Course, Lesson, Enrollment
from .serializers import (
    CourseSerializer, CourseDetailSerializer, AdminCourseSerializer, AdminLessonSerializer
)
from .permissions import IsEnrolled
from wallet.models import Wallet, Transaction
import os

@extend_schema(
    summary="List all available courses",
    description="Provides a public list of all courses available for enrollment."
)
class CourseListView(generics.ListAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(
    summary="Retrieve a single course's details",
    description="Fetches detailed information for a specific course, including its lesson list. Access is restricted to enrolled users."
)
class CourseDetailView(generics.RetrieveAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer
    permission_classes = [permissions.IsAuthenticated, IsEnrolled]

@extend_schema(
    summary="Enroll in a course",
    description="Allows an authenticated user to enroll in a course by spending credits from their wallet. The cost of the course is deducted from the user's wallet, and an enrollment record is created."
)
class EnrollCourseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, course_id):
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({"error": "You are already enrolled in this course."}, status=status.HTTP_400_BAD_REQUEST)

        if user.wallet.balance < course.price:
            return Response({"error": "Insufficient credits."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                user.wallet.balance -= course.price
                user.wallet.save()

                Transaction.objects.create(
                    wallet=user.wallet,
                    amount=-course.price,
                    transaction_type=Transaction.TransactionType.PURCHASE,
                    description=f"Purchase of course: {course.title}"
                )

                Enrollment.objects.create(user=user, course=course)

            return Response({"success": "Successfully enrolled in the course."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@extend_schema(
    summary="Stream a lesson's video",
    description="Securely streams the video file for a specific lesson. Access is restricted to authenticated users who are enrolled in the corresponding course."
)
class StreamVideoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, lesson_id):
        try:
            lesson = Lesson.objects.select_related('course').get(id=lesson_id)
        except Lesson.DoesNotExist:
            raise Http404

        is_enrolled = Enrollment.objects.filter(user=request.user, course=lesson.course).exists()
        if not is_enrolled:
            return Response({"error": "You are not enrolled in this course."}, status=status.HTTP_403_FORBIDDEN)

        video_path = os.path.join(settings.MEDIA_ROOT, lesson.video_reference)
        if not os.path.exists(video_path):
            return Response({"error": "Video file not found."}, status=status.HTTP_404_NOT_FOUND)

        return FileResponse(open(video_path, 'rb'), as_attachment=True, filename=os.path.basename(video_path))

# --- Admin ViewSets ---

@extend_schema(summary="Admin: Manage courses")
class AdminCourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = AdminCourseSerializer
    permission_classes = [permissions.IsAdminUser]

@extend_schema(summary="Admin: Manage lessons")
class AdminLessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = AdminLessonSerializer
    permission_classes = [permissions.IsAdminUser]
