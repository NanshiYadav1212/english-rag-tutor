import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock } from 'lucide-react';
import { api } from '../utils/api';
import './LessonCard.css';


export default function LessonCard({ lesson, isSelected, onSelect, token }) {
  const [attemptCount, setAttemptCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [lastScore, setLastScore] = useState(null);
  const [recentGrades, setRecentGrades] = useState([]);

  useEffect(() => {
    const loadAttempts = async () => {
      setLoading(true);
      try {
        const res = await api(token).get(`/quiz/attempts/${lesson.slug}`);
        // setAttemptCount(res.data?.attempts || 0);
        setAttemptCount(res.data?.attempts?.length || 0);
        setLastScore(res.data?.last_score || null);
        setRecentGrades(res.data?.recent_grades || []);
      } catch (err) {
        setAttemptCount(0);
        setLastScore(null);
        setRecentGrades([]);
      } finally {
        setLoading(false);
      }
    };
    if (token) {
      loadAttempts();
    }
  }, [lesson.slug, token]);

  const hasCompleted = attemptCount > 0;

  return (
    <div 
      className={`lesson-card ${isSelected ? 'selected' : ''} ${hasCompleted ? 'completed' : ''}`}
      onClick={onSelect}
    >
      <div className="lesson-card-header">
        <h3 className="lesson-card-title">{lesson.title}</h3>
        {hasCompleted && <CheckCircle size={20} className="completed-icon" />}
      </div>

      <p className="lesson-card-description">{lesson.description}</p>


      <div className="lesson-card-stats">
        {!loading ? (
          <>
            <div className="stat-item">
              <span className="stat-label">Attempts</span>
              <span className="stat-value">{attemptCount}</span>
            </div>
            {hasCompleted && lastScore !== null && (
              <div className="stat-item">
                <span className="stat-label">Last Score</span>
                <span className="stat-value">{lastScore}%</span>
              </div>
            )}
          </>
        ) : (
          <div className="stat-item">
            <Clock size={14} />
            <span className="stat-label">Loading...</span>
          </div>
        )}
      </div>


      {/* Progress bar removed: getProgressPercentage is obsolete after refactor */}

      <button
        className="btn-start-lesson"
        onClick={(e) => {
          e.stopPropagation();
          console.log('LessonCard start clicked for', lesson.slug);
          if (onSelect) onSelect();
        }}
      >
        {hasCompleted ? 'Continue' : 'Start'} Lesson →
      </button>
    </div>
  );
}

