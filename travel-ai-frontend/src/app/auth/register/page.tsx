'use client';

import Link from 'next/link';
import AuthForm from '@/components/AuthForm';
import { motion } from 'framer-motion';

export default function RegisterPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center px-6">
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900" />
        <div className="absolute inset-0 bg-gradient-to-r from-blue-600/10 via-purple-600/10 to-pink-600/10 animate-pulse" />
      </div>

      <div className="relative z-10 w-full max-w-md">
        <AuthForm mode="register" />
        <motion.p
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 text-center text-white/70"
        >
          Already have an account?{' '}
          <Link href="/auth/login" className="text-blue-300 hover:text-blue-200">
            Sign in
          </Link>
        </motion.p>
      </div>
    </div>
  );
}


