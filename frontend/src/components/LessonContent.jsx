
import React, { useEffect, useState } from 'react';
import { api } from '../utils/api';
import './lessoncontent.css';

export default function LessonContent({ lessonId, token }) {
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLesson = async () => {
      try {
        const res = await api(token).get(`/lessons/${lessonId}`);
        setLesson(res.data);
      } catch (err) {
        console.error('Failed to load lesson:', err);
      } finally {
        setLoading(false);
      }
    };

    if (lessonId) fetchLesson();
  }, [lessonId, token]);

  if (loading) return <p className="lesson-loading">Loading lesson...</p>;
  if (!lesson) return <p className="lesson-error">Lesson not found.</p>;

  return (
    <div className="lesson-box">
      <h1 className="lesson-title">{lesson.title}</h1>
      <p className="lesson-description">{lesson.description}</p>

      {lesson.content?.examples && (
        <div className="examples-container">
          <h3 className="examples-title">Examples:</h3>
          <ul className="examples-list">
            {lesson.content.examples.map((ex, i) => (
              <li key={i} className="example-item">
                <span className="example-sentence">{ex.sentence}</span>
                {ex.translation && (
                  <p className="example-translation">→ {ex.translation}</p>
                )}
              </li>
            ))}
          </ul>
        </div>
      )}

      <div className="practice-box">
        <p>Practice below by writing full sentences!</p>
      </div>
    </div>
  );
}
