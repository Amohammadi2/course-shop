'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import api from '@/services/api';
import VideoPlayer from '@/components/VideoPlayer';

interface Lesson {
  id: number;
  title: string;
  video_url: string;
}

export default function LessonPage() {
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const { id, lessonId } = useParams();

  useEffect(() => {
    const fetchLesson = async () => {
      try {
        const response = await api.get(`/courses/lessons/${lessonId}/stream/`);
        setLesson(response.data);
      } catch (error) {
        console.error('Failed to fetch lesson:', error);
      } finally {
        setLoading(false);
      }
    };

    if (id && lessonId) {
      fetchLesson();
    }
  }, [id, lessonId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p>Lesson not found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4">{lesson.title}</h1>
      <VideoPlayer src={lesson.video_url} />
    </div>
  );
}
