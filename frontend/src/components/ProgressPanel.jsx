import React, { useState, useEffect } from 'react';
import { TrendingUp, BookOpen, Target, Award, Zap } from 'lucide-react';
import { api } from '../utils/api';
import './ProgressPanel.css';

export default function ProgressPanel({ progress, token }) {
  const [lessonStats, setLessonStats] = useState([]);

  useEffect(() => {
    if (progress?.lessons_stats) {
      setLessonStats(progress.lessons_stats);
    }
  }, [progress]);

  const metrics = progress?.metrics || {};
  const predictedLevel = progress?.predicted_level || 'Beginner';
  const confidence = progress?.confidence || 0;
  const difficulty = progress?.difficulty_adjustment || 'Maintain';
  const recommendedLessons = progress?.recommended_lessons || [];

  const getLevelColor = (level) => {
    switch(level) {
      case 'Beginner': return '#fbbf24';
      case 'Intermediate': return '#60a5fa';
      case 'Advanced': return '#34d399';
      default: return '#d1d5db';
    }
  };

  const getDifficultyEmoji = (diff) => {
    switch(diff) {
      case 'Decrease': return '📉';
      case 'Increase': return '📈';
      default: return '➡️';
    }
  };

  return (
    <div className="progress-panel">
      {/* ML Prediction Section */}
      <section className="progress-section">
        <h2 className="section-heading">
          <Award size={20} />
          Your Learning Level
        </h2>
        
        <div className="level-card">
          <div className="level-display">
            <div 
              className="level-badge"
              style={{ borderColor: getLevelColor(predictedLevel) }}
            >
              <div 
                className="level-circle"
                style={{ backgroundColor: getLevelColor(predictedLevel) }}
              ></div>
              <span className="level-text">{predictedLevel}</span>
            </div>
          </div>

          <div className="prediction-details">
            <div className="detail-item">
              <span className="detail-label">Model Confidence</span>
              <div className="confidence-bar">
                <div 
                  className="confidence-fill"
                  style={{ width: `${confidence * 100}%` }}
                ></div>
              </div>
              <span className="confidence-value">{Math.round(confidence * 100)}%</span>
            </div>

            <div className="detail-item">
              <span className="detail-label">Recommended Action</span>
              <div className="difficulty-badge">
                <span>{getDifficultyEmoji(difficulty)}</span>
                <span>{difficulty} Difficulty</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Metrics Section */}
      <section className="progress-section">
        <h2 className="section-heading">
          <TrendingUp size={20} />
          Your Metrics
        </h2>

        <div className="metrics-grid">
          <div className="metric-card">
            <div className="metric-icon" style={{ background: '#e0e7ff' }}>
              <Target size={24} style={{ color: '#4f46e5' }} />
            </div>
            <div className="metric-content">
              <p className="metric-label">Average Score</p>
              <p className="metric-value">{(metrics.avg_score * 100 || 0).toFixed(1)}%</p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon" style={{ background: '#f0fdf4' }}>
              <BookOpen size={24} style={{ color: '#16a34a' }} />
            </div>
            <div className="metric-content">
              <p className="metric-label">Quiz Attempts</p>
              <p className="metric-value">{metrics.attempts || 0}</p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon" style={{ background: '#fef3c7' }}>
              <Zap size={24} style={{ color: '#d97706' }} />
            </div>
            <div className="metric-content">
              <p className="metric-label">Completion Rate</p>
              <p className="metric-value">{(metrics.completion_rate * 100 || 0).toFixed(0)}%</p>
            </div>
          </div>

          <div className="metric-card">
            <div className="metric-icon" style={{ background: '#fecaca' }}>
              <TrendingUp size={24} style={{ color: '#dc2626' }} />
            </div>
            <div className="metric-content">
              <p className="metric-label">Recent Trend</p>
              <p className="metric-value">
                {metrics.recent_score_trend > 0 ? '+' : ''}{(metrics.recent_score_trend * 100 || 0).toFixed(1)}%
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Lesson Performance */}
      <section className="progress-section">
        <h2 className="section-heading">
          <BookOpen size={20} />
          Lesson Performance
        </h2>

        {lessonStats.length > 0 ? (
          <div className="lessons-table">
            {lessonStats.map((stat, idx) => (
              <div key={idx} className="lesson-row">
                <div className="lesson-name">{stat.lesson_slug}</div>
                <div className="lesson-stats">
                  <span className="badge attempts">
                    {stat.attempts} attempt{stat.attempts !== 1 ? 's' : ''}
                  </span>
                  <span className="badge score">
                    {stat.average_score}% avg
                  </span>
                  <span className="badge best">
                    {stat.best_score}% best
                  </span>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-state">No quiz attempts yet. Start with a lesson!</p>
        )}
      </section>

      {/* Recommended Lessons */}
      {recommendedLessons.length > 0 && (
        <section className="progress-section">
          <h2 className="section-heading">
            <Target size={20} />
            Recommended for You
          </h2>

          <div className="recommendations">
            {recommendedLessons.map((lesson, idx) => (
              <div key={idx} className="recommendation-item">
                <span className="rec-badge">💡</span>
                <p>{lesson}</p>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Summary */}
      <section className="progress-section summary">
        <h3>Summary</h3>
        <p>
          You've completed <strong>{metrics.attempts || 0}</strong> quiz attempts with an average score of 
          <strong> {((metrics.avg_score || 0) * 100).toFixed(1)}%</strong>. Your current level is 
          <strong> {predictedLevel}</strong> with <strong>{Math.round(confidence * 100)}%</strong> confidence.
        </p>
      </section>
    </div>
  );
}

