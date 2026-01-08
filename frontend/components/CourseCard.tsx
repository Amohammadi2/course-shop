'use client';

import { motion } from 'framer-motion';
import Link from 'next/link';

interface Course {
  id: number;
  title: string;
  description: string;
  price: number;
}

const CourseCard = ({ course }: { course: Course }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="overflow-hidden rounded-lg bg-white shadow-md"
    >
      <div className="p-6">
        <h3 className="text-xl font-bold">{course.title}</h3>
        <p className="mt-2 text-gray-600">{course.description}</p>
        <div className="mt-4 flex items-center justify-between">
          <span className="text-lg font-bold text-indigo-600">
            {course.price} credits
          </span>
          <Link href={`/courses/${course.id}`}>
            <span className="rounded-md bg-indigo-600 px-4 py-2 font-bold text-white hover:bg-indigo-700">
              View Course
            </span>
          </Link>
        </div>
      </div>
    </motion.div>
  );
};

export default CourseCard;
