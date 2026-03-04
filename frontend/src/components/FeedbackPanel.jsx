
import React, { useState } from 'react';
import { Sparkles, Star, Download } from 'lucide-react';
import { api } from '../utils/api';
import './feedbackpanel.css';

export default function FeedbackPanel({ feedback, token }) {
  const parsed = feedback?.evaluation || {
    correction: feedback?.user_input || 'Good job!',
    explanations: ['Keep practicing.'],
    score: 0.8,
    suggested_exercises: []
  };

  const score = Math.round((parsed.score || 0) * 100);
  const [favorite, setFavorite] = useState(feedback?.favorite || false);
  const resultId = feedback?._id;

  const toggleFavorite = async () => {
    try {
      await api(token).post('/progress/favorite', { result_id: resultId, favorite: !favorite });
      setFavorite(!favorite);
    } catch (e) {
      console.error('Failed to toggle favorite', e);
    }
  };

  return (
    <div className="fb-card">
      {parsed.fallback && (
        <div style={{ background: '#fff4e5', padding: '8px 12px', borderRadius: 8, marginBottom: 12, color: '#6a4b00' }}>
          <strong>Note:</strong> Service unavailable — showing fallback result (original input).
        </div>
      )}

      <div className="fb-score-wrapper">
        <div className="fb-score-circle">
          <span className="fb-score-number">{score}</span>
        </div>
        <div className="fb-score-icon">
          {score >= 90 ? <Sparkles className="fb-icon-spark" /> : null}
        </div>
      </div>

      <h3 className="fb-correction-title">Corrected Version</h3>
      <p className="fb-correction-text">{parsed.correction}</p>

      <div className="fb-original-box">
        <h4 className="fb-original-title">Original Input</h4>
        <p className="fb-original-text">{feedback?.user_input}</p>
      </div>

      {parsed.explanations?.length > 0 && (
        <div className="fb-insights-box">
          <h4 className="fb-insights-title">Key Insights</h4>
          {parsed.explanations.map((e, i) => <p key={i}>→ {e}</p>)}
        </div>
      )}

      {parsed.suggested_exercises?.length > 0 && (
        <div className="fb-suggested-box">
          <h4>Suggested Exercises</h4>
          <ul>
            {parsed.suggested_exercises.map((s, i) => <li key={i}>{s}</li>)}
          </ul>
        </div>
      )}

      <div style={{ marginTop: '0.75rem', display: 'flex', gap: '0.5rem' }}>
        <button className="fb-fav-btn" onClick={toggleFavorite}>
          <Star className={favorite ? 'fav-on' : 'fav-off'} /> {favorite ? 'Favorited' : 'Favorite'}
        </button>
        <button className="fb-export-btn" onClick={() => navigator.clipboard?.writeText(parsed.correction || '')}>
          <Download /> Copy
        </button>
      </div>
    </div>
  );
}
