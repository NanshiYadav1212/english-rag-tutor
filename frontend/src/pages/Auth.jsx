import React, { useState } from 'react';
import { api } from '../utils/api';
import './Auth.css';

export default function Auth({ onLogin, onBackToLanding }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [isLogin, setIsLogin] = useState(true); // Toggle between login and signup

  const handleAuth = async () => {
    setLoading(true);
    try {
      const type = isLogin ? 'login' : 'signup';
      const res = await api().post(`/auth/${type}`, { email, password });
      onLogin(res.data.access_token);
    } catch (err) {
      alert(err.response?.data?.detail || 'Error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      

      {/* Background blobs */}
      <div className="blob animation-delay-2000"></div>
      <div className="blob animation-delay-4000"></div>
      <div className="blob animation-delay-6000"></div>

      {/* Glass card */}
      <div className="relative z-10 glass p-12 w-full max-w-md transform hover:scale-105 transition-all duration-500">

        {/* Back Button */}
        <button
          onClick={onBackToLanding}
          className="back-btn"
        >
          ← Back to Home
        </button>

        {/* Header */}
        <div className="card-header text-center mb-8">
          <h1 className="text-6xl font-black gradient-text mb-2">AI Language Tutor</h1>
          <p className="text-xl text-black/80 mb-4 font-bold">
            {isLogin ? 'Login to your account' : 'Create a new account'}
          </p>
        </div>

        {/* Form */}
        <div className="form-fields">
          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="input-field"
          />
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="input-field"
          />

          <button
            onClick={handleAuth}
            disabled={loading}
            className={`btn ${isLogin ? 'btn-login' : 'btn-signup'}`}
          >
            {isLogin ? 'Login' : 'Sign Up'}
          </button>

          {/* Toggle form */}
          <p
            className="toggle-link text-center"
            onClick={() => setIsLogin(!isLogin)}
          >
            {isLogin ? "Don't have an account? Sign Up" : "Already have an account? Login"}
          </p>

          <p className="quote text-center">
            “Write. Get feedback. Improve instantly.”
          </p>
        </div>
      </div>
    </div>
  );
}
