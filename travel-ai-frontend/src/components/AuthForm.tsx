'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';
import { Mail, Lock, User } from 'lucide-react';

interface AuthFormProps {
  mode: 'login' | 'register';
  onSubmit?: (data: { name?: string; email: string; password: string }) => Promise<void> | void;
}

export default function AuthForm({ mode, onSubmit }: AuthFormProps) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const title = mode === 'login' ? 'Welcome back' : 'Create your account';
  const button = mode === 'login' ? 'Sign in' : 'Sign up';

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (loading) return;
    setLoading(true);
    try {
      if (onSubmit) {
        await onSubmit({ name: name || undefined, email, password });
      } else {
        const base = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
        const url = mode === 'login' ? `${base}/auth/login` : `${base}/auth/register`;
        const res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, email, password }),
        });
        if (!res.ok) {
          const msg = await res.json().catch(() => ({} as any));
          throw new Error(msg?.detail || 'Authentication failed');
        }
        const data = await res.json();
        // Store token for later calls (simple client-side session)
        if (data?.token) localStorage.setItem('auth_token', data.token);
        if (data?.user) localStorage.setItem('auth_user', JSON.stringify(data.user));
        // Redirect to home after auth
        window.location.href = '/';
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="w-full max-w-md mx-auto"
    >
      <div className="bg-white/5 backdrop-blur-md border border-white/10 rounded-2xl p-8">
        <h1 className="text-2xl font-bold text-white mb-6">{title}</h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          {mode === 'register' && (
            <div>
              <label className="block text-white/70 text-sm mb-2">Name</label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/50" />
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  placeholder="Your name"
                  className="w-full pl-10 pr-3 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
                />
              </div>
            </div>
          )}

          <div>
            <label className="block text-white/70 text-sm mb-2">Email</label>
            <div className="relative">
              <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/50" />
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                className="w-full pl-10 pr-3 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
              />
            </div>
          </div>

          <div>
            <label className="block text-white/70 text-sm mb-2">Password</label>
            <div className="relative">
              <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/50" />
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full pl-10 pr-3 py-3 bg-white/10 border border-white/20 rounded-lg text-white placeholder-white/50 focus:outline-none focus:ring-2 focus:ring-white/30"
              />
            </div>
          </div>

          <motion.button
            type="submit"
            whileHover={{ scale: loading ? 1 : 1.02 }}
            whileTap={{ scale: loading ? 1 : 0.98 }}
            disabled={loading}
            className="w-full py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white font-semibold rounded-lg hover:shadow-lg transition-all duration-300 disabled:opacity-60"
          >
            {loading ? 'Please wait…' : button}
          </motion.button>
        </form>
      </div>
    </motion.div>
  );
}


