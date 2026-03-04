import React, { useState, useEffect } from 'react';
import { api } from '../utils/api';
import './Quiz.css';
import { CheckCircle, XCircle, Loader } from 'lucide-react';

export default function Quiz({ lesson, token, onSubmitSuccess }) {
  const [quizzes, setQuizzes] = useState({});
  const [selectedQuizType, setSelectedQuizType] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const QUIZ_TYPES = [
    { id: 'multiple_choice', label: 'Multiple Choice', icon: '◯' },
    { id: 'fill_blank', label: 'Fill in the Blank', icon: '✏' },
    { id: 'true_false', label: 'True / False', icon: '⊕' },
    { id: 'match', label: 'Match the Following', icon: '↔' },
    { id: 'short_answer', label: 'Short Answer', icon: '📝' }
  ];

  useEffect(() => {
    if (!lesson) return;
    
    const loadQuizzes = async () => {
      setLoading(true);
      try {
        const res = await api(token).get(`/quiz/lesson/${lesson.slug}`);
        setQuizzes(res.data?.quizzes || {});
        if (!selectedQuizType && res.data?.quizzes) {
          const firstType = Object.keys(res.data.quizzes)[0];
          setSelectedQuizType(firstType);
        }
      } catch (err) {
        console.error('Failed to load quizzes:', err);
      } finally {
        setLoading(false);
      }
    };

    loadQuizzes();
  }, [lesson, token]);

  if (!lesson) return <div className="quiz-section">Select a lesson to begin</div>;

  const currentQuiz = selectedQuizType ? quizzes[selectedQuizType] : null;
  const currentQuizType = QUIZ_TYPES.find(t => t.id === selectedQuizType);

  const handleAnswerChange = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmitQuiz = async () => {
    if (!currentQuiz || !currentQuizType) return;

    // Check all questions answered
    const unanswered = currentQuiz.questions.filter(q => !answers[q.question_id]);
    if (unanswered.length > 0) {
      alert(`Please answer all ${unanswered.length} question(s)`);
      return;
    }

    setSubmitting(true);
    try {
      const questionsWithAnswers = currentQuiz.questions.map(q => ({
        question_id: q.question_id,
        user_answer: answers[q.question_id]
      }));

      const res = await api(token).post('/quiz/submit', {
        lesson_slug: lesson.slug,
        quiz_type: selectedQuizType,
        questions_with_answers: questionsWithAnswers
      });

      setResults(res.data);
      setSubmitted(true);
      if (onSubmitSuccess) onSubmitSuccess();
    } catch (err) {
      console.error('Failed to submit quiz:', err);
      alert('Failed to submit quiz');
    } finally {
      setSubmitting(false);
    }
  };

  const renderQuestion = (question) => {
    const baseClasses = "quiz-question";

    switch (selectedQuizType) {
      case 'multiple_choice':
        return (
          <div key={question.question_id} className={baseClasses}>
            <p className="question-text">{question.question_text}</p>
            <div className="options-group">
              {question.options.map((opt, idx) => (
                <label key={idx} className="option-label">
                  <input
                    type="radio"
                    name={question.question_id}
                    value={opt}
                    checked={answers[question.question_id] === opt}
                    onChange={(e) => handleAnswerChange(question.question_id, e.target.value)}
                  />
                  <span>{opt}</span>
                </label>
              ))}
            </div>
          </div>
        );

      case 'fill_blank':
        return (
          <div key={question.question_id} className={baseClasses}>
            <p className="question-text">Complete: <em>{question.sentence}</em></p>
            <input
              type="text"
              className="answer-input"
              placeholder="Type the missing word..."
              value={answers[question.question_id] || ''}
              onChange={(e) => handleAnswerChange(question.question_id, e.target.value)}
            />
          </div>
        );

      case 'true_false':
        return (
          <div key={question.question_id} className={baseClasses}>
            <p className="question-text">{question.statement}</p>
            <div className="tf-buttons">
              <button
                className={`tf-btn ${answers[question.question_id] === 'true' ? 'selected' : ''}`}
                onClick={() => handleAnswerChange(question.question_id, 'true')}
              >
                True
              </button>
              <button
                className={`tf-btn ${answers[question.question_id] === 'false' ? 'selected' : ''}`}
                onClick={() => handleAnswerChange(question.question_id, 'false')}
              >
                False
              </button>
            </div>
          </div>
        );

      case 'match':
        return (
          <div key={question.question_id} className={baseClasses}>
            <p className="question-text">{question.question_text}</p>
            <div className="matching-group">
              <div className="left-column">
                {question.left_items.map((item, idx) => (
                  <div key={idx} className="match-item">{item}</div>
                ))}
              </div>
              <div className="right-column">
                {question.right_items.map((item, idx) => (
                  <div key={idx} className="match-item">{item}</div>
                ))}
              </div>
            </div>
            <p className="hint-text">Drag or type matching pairs (e.g., "phrasal verb -> definition")</p>
            <textarea
              className="matching-answer"
              placeholder="Enter your matches..."
              value={answers[question.question_id] || ''}
              onChange={(e) => handleAnswerChange(question.question_id, e.target.value)}
            />
          </div>
        );

      case 'short_answer':
        return (
          <div key={question.question_id} className={baseClasses}>
            <p className="question-text">{question.question_text}</p>
            <textarea
              className="short-answer-input"
              placeholder="Type your answer..."
              rows="3"
              value={answers[question.question_id] || ''}
              onChange={(e) => handleAnswerChange(question.question_id, e.target.value)}
            />
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="quiz-section">
      <h3 className="quiz-section-title">Practice Quiz</h3>

      {!submitted ? (
        <>
          {/* Quiz Type Selector */}
          <div className="quiz-type-selector">
            <p className="selector-label">Choose a quiz type:</p>
            <div className="type-buttons">
              {QUIZ_TYPES.map(qtype => (
                <button
                  key={qtype.id}
                  className={`type-btn ${selectedQuizType === qtype.id ? 'active' : ''}`}
                  onClick={() => {
                    setSelectedQuizType(qtype.id);
                    setAnswers({});
                    setSubmitted(false);
                  }}
                  disabled={!quizzes[qtype.id]}
                >
                  <span className="btn-icon">{qtype.icon}</span>
                  <span className="btn-label">{qtype.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Quiz Content */}
          {loading ? (
            <div className="loading-state">
              <Loader className="spinner" />
              <p>Loading quiz...</p>
            </div>
          ) : currentQuiz ? (
            <div className="quiz-content">
              <div className="quiz-info">
                <span className="quiz-type-badge">{currentQuizType.label}</span>
                <span className="quiz-count">{currentQuiz.total_questions} questions • {currentQuiz.total_marks} marks</span>
              </div>

              <div className="questions-container">
                {currentQuiz.questions.map(renderQuestion)}
              </div>

              <div className="quiz-actions">
                <button
                  className="btn btn-submit"
                  onClick={handleSubmitQuiz}
                  disabled={submitting}
                >
                  {submitting ? 'Submitting...' : 'Submit Quiz'}
                </button>
              </div>
            </div>
          ) : (
            <p className="no-quiz">No quiz available for this type.</p>
          )}
        </>
      ) : results ? (
        <div className="quiz-results">
          <div className="results-header">
            <h4>Quiz Results</h4>
            <div className={`score-display ${results.quiz_score >= 70 ? 'pass' : 'fail'}`}>
              <div className="score-number">{results.quiz_score}%</div>
              <div className="score-label">{results.quiz_score >= 70 ? '✓ Great!' : 'Try again'}</div>
            </div>
          </div>

          <div className="results-stats">
            <div className="result-stat">
              <span className="stat-label">Score Earned</span>
              <span className="stat-value">{results.score_earned}/{results.total_marks}</span>
            </div>
            <div className="result-stat">
              <span className="stat-label">Correct Answers</span>
              <span className="stat-value">{results.detailed_results.filter(r => r.correct).length}/{results.detailed_results.length}</span>
            </div>
          </div>

          <div className="results-detail">
            {results.detailed_results.map((result, idx) => (
              <div key={idx} className={`result-item ${result.correct ? 'correct' : 'incorrect'}`}>
                <div className="result-icon">
                  {result.correct ? <CheckCircle size={20} /> : <XCircle size={20} />}
                </div>
                <div className="result-content">
                  <p className="result-question">Question {idx + 1}</p>
                  <p className="result-answer">Your answer: <strong>{result.user_answer}</strong></p>
                  <p className="result-marks">+{result.marks_awarded} marks</p>
                </div>
              </div>
            ))}
          </div>

          <div className="quiz-actions">
            <button
              className="btn btn-again"
              onClick={() => {
                setSubmitted(false);
                setResults(null);
                setAnswers({});
              }}
            >
              Try Again
            </button>
          </div>
        </div>
      ) : null}
    </div>
  );
}
