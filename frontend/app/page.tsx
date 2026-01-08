'use client';

import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import animationData from '@/public/animation.json'; // You'll need to add a Lottie animation file

export default function LandingPage() {
  return (
    <div className="bg-gray-900 text-white">
      {/* Hero Section */}
      <motion.section
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
        className="container mx-auto flex min-h-screen items-center justify-between px-4"
      >
        <div className="max-w-xl">
          <motion.h1
            initial={{ y: -50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-5xl font-bold"
          >
            Unlock Your Potential with Our Courses
          </motion.h1>
          <motion.p
            initial={{ y: -30, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            className="mt-4 text-lg"
          >
            Learn from industry experts and take your skills to the next level.
          </motion.p>
          <motion.button
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="mt-8 rounded-md bg-indigo-600 px-6 py-3 font-bold text-white hover:bg-indigo-700"
          >
            Get Started
          </motion.button>
        </div>
        <div className="w-1/2">
          <Lottie animationData={animationData} />
        </div>
      </motion.section>

      {/* Features Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <h2 className="mb-12 text-center text-4xl font-bold">
            Why Choose Us?
          </h2>
          <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="rounded-lg bg-gray-800 p-8"
            >
              <h3 className="text-2xl font-bold">Expert Instructors</h3>
              <p className="mt-4">
                Our courses are taught by industry professionals with years of
                experience.
              </p>
            </motion.div>
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="rounded-lg bg-gray-800 p-8"
            >
              <h3 className="text-2xl font-bold">Flexible Learning</h3>
              <p className="mt-4">
                Learn at your own pace with our on-demand video lessons.
              </p>
            </motion.div>
            <motion.div
              initial={{ y: 50, opacity: 0 }}
              whileInView={{ y: 0, opacity: 1 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="rounded-lg bg-gray-800 p-8"
            >
              <h3 className="text-2xl font-bold">Community Support</h3>
              <p className="mt-4">
                Join our community of learners and get help when you need it.
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Call to Action Section */}
      <section className="bg-gray-800 py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-4xl font-bold">Ready to Get Started?</h2>
          <p className="mt-4 text-lg">
            Create an account and start learning today.
          </p>
          <button className="mt-8 rounded-md bg-indigo-600 px-6 py-3 font-bold text-white hover:bg-indigo-700">
            Sign Up Now
          </button>
        </div>
      </section>
    </div>
  );
}
