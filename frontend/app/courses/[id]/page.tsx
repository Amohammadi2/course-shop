'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import api from '@/services/api';
import { useWallet } from '@/hooks/useWallet';

interface Course {
  id: number;
  title: string;
  description: string;
  price: number;
}

export default function CourseDetailPage() {
  const [course, setCourse] = useState<Course | null>(null);
  const [loading, setLoading] = useState(true);
  const { id } = useParams();
  const { balance, fetchBalance } = useWallet();
  const router = useRouter();

  useEffect(() => {
    const fetchCourse = async () => {
      try {
        const response = await api.get(`/courses/${id}/`);
        setCourse(response.data);
      } catch (error) {
        console.error('Failed to fetch course:', error);
      } finally {
        setLoading(false);
      }
    };

    if (id) {
      fetchCourse();
    }
  }, [id]);

  const handlePurchase = async () => {
    if (course && balance >= course.price) {
      try {
        await api.post(`/courses/${id}/purchase/`);
        fetchBalance();
        router.push('/courses');
      } catch (error) {
        console.error('Failed to purchase course:', error);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <p>Course not found.</p>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-4xl font-bold mb-4">{course.title}</h1>
      <p className="text-lg text-gray-600 mb-8">{course.description}</p>
      <div className="flex items-center justify-between">
        <span className="text-2xl font-bold text-indigo-600">
          {course.price} credits
        </span>
        <button
          onClick={handlePurchase}
          disabled={balance < course.price}
          className="rounded-md bg-indigo-600 px-6 py-3 font-bold text-white hover:bg-indigo-700 disabled:bg-gray-400"
        >
          {balance >= course.price ? 'Purchase Course' : 'Not enough credits'}
        </button>
      </div>
    </div>
  );
}
