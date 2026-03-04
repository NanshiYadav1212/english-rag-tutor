import React from 'react';
import './LandingPage.css'; // We'll define all styles here

const LandingPage = ({ onGetStarted }) => {
  return (
    <div className="landing-wrapper">
      
      {/* --- Navbar --- */}
      <nav className="navbar">
        <div className="logo-section">
          <div className="logo-icon">🧠</div>
          <span className="logo-text">Language Tutor</span>
        </div>
        {/* <button className="btn btn-login-top" onClick={onGetStarted}>
          Login Page
        </button> */}
      </nav>

      {/* --- Hero Section --- */}
      <header className="hero-section">
        <h1 className="hero-title">
          Language Tutor: Master English <br />
          <span className="gradient-text">with Smart Feedback</span>
        </h1>
        <p className="hero-description">
          Master English with clear, actionable feedback from your tutor backend. <br/>
          Get personalized recommendations, correct your grammar, and track your progress effortlessly.
        </p>
        <button className="btn-land btn-land-login hero-btn" onClick={onGetStarted}>
          Get Started &nbsp;→&nbsp; Login
        </button>

      </header>

      {/* --- Feature Cards Section --- */}
      <section className="features-section">
        <FeatureCard
          icon="🖥️"
          title="Real-time Feedback"
          description="Get instant, contextual feedback from your tutor backend to help you learn faster and correct mistakes." 
        />
        <FeatureCard
          icon="🗺️"
          title="Personalized Path"
          // description="Personalized path ensures your growth in tasks, and navigated learning tailored to you."
          description="Follow a personalized learning path built around your level, goals, and progress, so you always know what to learn next."
        />
        <FeatureCard
          icon="💬"
          title="Instant Feedback"
          description="Receive instant, clear feedback on answers, helping you improve accuracy, build confidence, and learn effectively."
        />
      </section>
      
    </div>
  );
};

// Reusable Card Component
const FeatureCard = ({ icon, title, description }) => {
  return (
    <div className="glass feature-card">
      <div className="feature-icon">{icon}</div>
      <h3 className="feature-title">{title}</h3>
      <p className="feature-desc">{description}</p>
    </div>
  );
};

export default LandingPage;
