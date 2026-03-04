import React, { useEffect, useState } from 'react';
import { api } from '../utils/api';
import { Book, Clock, Zap, ArrowLeft, Play } from 'lucide-react';
import './LessonDetail.css';

export default function LessonDetail({ lessonSlug, token, onBack, onStartQuiz }) {
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLesson = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api(token).get(`/lessons/${lessonSlug}`);
        setLesson(response.data);
      } catch (err) {
        console.error('Failed to load lesson:', err);
        setError('Failed to load lesson. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (lessonSlug) {
      fetchLesson();
    }
  }, [lessonSlug, token]);

  if (loading) {
    return (
      <div className="lesson-detail">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} /> Back
        </button>
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="lesson-detail">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} /> Back
        </button>
        <div className="error-message">
          <p>{error || 'Lesson not found'}</p>
        </div>
      </div>
    );
  }

  const difficultyColors = {
    Beginner: '#10b981',
    Intermediate: '#f59e0b',
    Advanced: '#ef4444'
  };

  return (
    <div className="lesson-detail">
      {/* Header with Back Button */}
      <button className="btn-back" onClick={onBack}>
        <ArrowLeft size={20} /> Back to Lessons
      </button>

      {/* Lesson Meta */}
      <div className="lesson-header">
        <h1>{lesson.title}</h1>
        <div className="lesson-meta">
          <span className="difficulty" style={{ 
            backgroundColor: difficultyColors[lesson.difficulty] || '#6b7280'
          }}>
            <Zap size={16} />
            {lesson.difficulty}
          </span>
          <span className="time">
            <Clock size={16} />
            ~{lesson.estimated_time} min
          </span>
        </div>
        <p className="lesson-description">{lesson.description}</p>
      </div>

      {/* Main Content */}
      <div className="lesson-content">
        {/* Notes Section */}
        <section className="notes-section">
          <h2>Key Concepts</h2>
          <div className="notes-text">
            {lesson.notes ? (
              lesson.notes.split('\n\n').map((para, idx) => (
                <p key={idx}>{para}</p>
              ))
            ) : (
              <p>No detailed notes available</p>
            )}
          </div>
        </section>

        {/* Examples Section */}
        {lesson.examples && lesson.examples.length > 0 && (
          <section className="examples-section">
            <h2>Practical Examples</h2>
            <div className="examples-grid">
              {lesson.examples.map((ex, idx) => (
                <div key={idx} className="example-card">
                  <div className="example-header">
                    <h3>Example {idx + 1}</h3>
                  </div>
                  <div className="example-content">
                    <div className="example-item">
                      <strong>Question/Statement:</strong>
                      <p>{ex.example}</p>
                    </div>
                    <div className="example-item">
                      <strong>Answer/Explanation:</strong>
                      <p>{ex.answer}</p>
                    </div>
                    <div className="example-item">
                      <strong>Details:</strong>
                      <p>{ex.explanation}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </div>

      {/* CTA Section */}
      <div className="lesson-cta">
        <button 
          className="btn-quiz"
          onClick={() => { console.log('LessonDetail Start Quiz for', lesson.slug); onStartQuiz(lesson.slug); }}
        >
          <Play size={20} />
          Start Practice Quiz
        </button>
        <p className="cta-subtitle">50 questions across 5 different formats</p>
      </div>
    </div>
  );
}
