import React, { useEffect, useState } from 'react';
import { api } from '../utils/api';
import { ArrowLeft, Check, X, Volume2, Clock } from 'lucide-react';
import './QuizInterface.css';

export default function QuizInterface({ lessonSlug, token, userEmail, onBack, onComplete }) {
  const [quiz, setQuiz] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [currentQuizType, setCurrentQuizType] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [results, setResults] = useState(null);
  const [timeStarted] = useState(Date.now());

  // Fetch available quiz types for this lesson
  useEffect(() => {
    const fetchQuiz = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await api(token).get(`/quiz/lesson/${lessonSlug}`);
        setQuiz(response.data);
        // Set first quiz type as default
        const firstType = Object.keys(response.data.quiz_types)[0];
        setCurrentQuizType(firstType);
      } catch (err) {
        console.error('Failed to load quiz:', err);
        setError('Failed to load quiz. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    if (lessonSlug) {
      fetchQuiz();
    }
  }, [lessonSlug, token]);

  const handleAnswerChange = (questionId, value) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: value
    }));
  };

  const handleSubmitQuiz = async () => {
    if (!currentQuizType) return;

    try {
      // Build answers array: [{ question_id: string, answer: any }]
      const answersArray = Object.entries(answers).map(([key, value]) => {
        // key is like 'q7' — extract digits to form the id; fallback to raw key
        const digits = key.replace(/\D/g, '');
        const qid = digits.length ? digits : key;
        return { question_id: String(qid), answer: value };
      });


      const response = await api(token).post('/quiz/submit', {
        lesson_slug: lessonSlug,
        quiz_type: currentQuizType,
        answers: answersArray,
        time_taken: Math.round((Date.now() - timeStarted) / 1000),
        user_email: userEmail || undefined
      });

      setResults(response.data);
      setSubmitted(true);
    } catch (err) {
      console.error('Failed to submit quiz:', err);
      setError('Failed to submit quiz. Please try again.');
    }
  };

  const getQuizTypeLabel = (type) => {
    const labels = {
      multiple_choice: 'Multiple Choice',
      true_false: 'True / False',
      fill_in_blanks: 'Fill in the Blanks',
      match_following: 'Match the Following',
      short_answer: 'Short Answer'
    };
    return labels[type] || type;
  };

  const renderQuestion = (question, idx, quizType) => {
    const answerId = `q${question.question_id}`;
    const currentAnswer = answers[answerId];

    if (quizType === 'multiple_choice') {
      return (
        <div key={idx} className="question multiple-choice">
          <h4>{question.question}</h4>
          <div className="options">
            {question.options?.map((option, optIdx) => (
              <label key={optIdx} className="option">
                <input
                  type="radio"
                  name={answerId}
                  value={option}
                  checked={currentAnswer === option}
                  onChange={(e) => handleAnswerChange(answerId, e.target.value)}
                  disabled={submitted}
                />
                <span>{option}</span>
              </label>
            ))}
          </div>
        </div>
      );
    }

    if (quizType === 'true_false') {
      return (
        <div key={idx} className="question true-false">
          <h4>{question.question}</h4>
          <div className="tf-options">
            <label className="tf-option">
              <input
                type="radio"
                name={answerId}
                value="true"
                checked={currentAnswer === 'true'}
                onChange={(e) => handleAnswerChange(answerId, e.target.value)}
                disabled={submitted}
              />
              <span>True</span>
            </label>
            <label className="tf-option">
              <input
                type="radio"
                name={answerId}
                value="false"
                checked={currentAnswer === 'false'}
                onChange={(e) => handleAnswerChange(answerId, e.target.value)}
                disabled={submitted}
              />
              <span>False</span>
            </label>
          </div>
        </div>
      );
    }

    if (quizType === 'fill_in_blanks') {
      return (
        <div key={idx} className="question fill-blank">
          <h4>{question.question}</h4>
          <input
            type="text"
            className="answer-input"
            value={currentAnswer || ''}
            onChange={(e) => handleAnswerChange(answerId, e.target.value)}
            placeholder="Type your answer..."
            disabled={submitted}
          />
        </div>
      );
    }

    if (quizType === 'match_following') {
      return (
        <div key={idx} className="question match">
          <h4>{question.question}</h4>
          <div className="matching-pairs">
            {question.pairs?.map((pair, pIdx) => (
              <div key={pIdx} className="match-row">
                <span className="left-item">{pair.left}</span>
                <span className="arrow">→</span>
                <select
                  className="match-select"
                  value={currentAnswer?.[pIdx] || ''}
                  onChange={(e) => {
                    const newAnswers = currentAnswer || [];
                    newAnswers[pIdx] = e.target.value;
                    handleAnswerChange(answerId, newAnswers);
                  }}
                  disabled={submitted}
                >
                  <option value="">Select...</option>
                  {question.pairs.map((p, idx) => (
                    <option key={idx} value={p.right}>{p.right}</option>
                  ))}
                </select>
              </div>
            ))}
          </div>
        </div>
      );
    }

    if (quizType === 'short_answer') {
      return (
        <div key={idx} className="question short-answer">
          <h4>{question.question}</h4>
          <textarea
            className="answer-textarea"
            value={currentAnswer || ''}
            onChange={(e) => handleAnswerChange(answerId, e.target.value)}
            placeholder="Type your answer..."
            disabled={submitted}
            rows="3"
          />
        </div>
      );
    }

    return null;
  };

  if (loading) {
    return (
      <div className="quiz-interface">
        <div className="loading">
          <div className="spinner"></div>
          <p>Loading quiz...</p>
        </div>
      </div>
    );
  }

  if (error || !quiz) {
    return (
      <div className="quiz-interface">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} /> Back
        </button>
        <div className="error-message">
          <p>{error || 'Quiz not found'}</p>
        </div>
      </div>
    );
  }

  if (submitted && results) {
    return (
      <div className="quiz-interface results-view">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} /> Back
        </button>

        <div className="results-header">
          <h2>Quiz Results</h2>
          <div className={`score-display ${results.passed ? 'passed' : 'failed'}`}>
            <div className="score-number">{results.percentage.toFixed(1)}%</div>
            <div className="score-label">{results.passed ? 'PASSED' : 'NEEDS IMPROVEMENT'}</div>
            <div className="score-detail">{results.score_earned} / {results.total_marks} points</div>
          </div>
        </div>

        <div className="results-details">
          {Array.isArray(results.detailed_results) && results.detailed_results.length > 0 ? (
            results.detailed_results.map((result, idx) => (
              <div key={idx} className={`result-item ${result.is_correct ? 'correct' : 'incorrect'}`}>
                <div className="result-header">
                  <span className="result-icon">
                    {result.is_correct ? <Check size={20} /> : <X size={20} />}
                  </span>
                  <span className="result-marks">{result.marks_awarded} pts</span>
                </div>
                <div className="result-body">
                  <p><strong>Your answer:</strong> {result.user_answer}</p>
                  {!result.is_correct && (
                    <p><strong>Correct answer:</strong> {result.correct_answer}</p>
                  )}
                  {result.explanation && (
                    <p><strong>Explanation:</strong> {result.explanation}</p>
                  )}
                </div>
              </div>
            ))
          ) : (
            <div className="result-item">
              <p>No detailed results available.</p>
            </div>
          )}
        </div>

        <div className="results-actions">
          <button className="btn-primary" onClick={onBack}>
            Try Another Quiz Type
          </button>
          <button className="btn-secondary" onClick={() => onComplete?.()}>
            Return to Dashboard
          </button>
        </div>
      </div>
    );
  }

  if (!currentQuizType || !quiz.quiz_types[currentQuizType]) {
    return (
      <div className="quiz-interface">
        <button className="btn-back" onClick={onBack}>
          <ArrowLeft size={20} /> Back
        </button>
        <p>Invalid quiz type selected</p>
      </div>
    );
  }

  const currentQuiz = quiz.quiz_types[currentQuizType];
  const answeredCount = Object.keys(answers).length;

  return (
    <div className="quiz-interface">
      <button className="btn-back" onClick={onBack}>
        <ArrowLeft size={20} /> Back
      </button>

      {/* Quiz Header */}
      <div className="quiz-header">
        <div>
          <h1>{quiz.lesson_title}</h1>
          <p className="quiz-type">{getQuizTypeLabel(currentQuizType)}</p>
        </div>
        <div className="quiz-stats">
          <span className="stat">
            <Clock size={18} />
            {currentQuiz.total_questions} Questions
          </span>
          <span className="stat">
            Answered: {answeredCount} / {currentQuiz.total_questions}
          </span>
        </div>
      </div>

      {/* Quiz Type Selector */}
      {Object.keys(quiz.quiz_types).length > 1 && (
        <div className="quiz-type-selector">
          <p>Quiz Types:</p>
          <div className="type-buttons">
            {Object.keys(quiz.quiz_types).map(type => (
              <button
                key={type}
                className={`type-btn ${currentQuizType === type ? 'active' : ''}`}
                onClick={() => {
                  setCurrentQuizType(type);
                  setAnswers({});
                  setSubmitted(false);
                  setResults(null);
                }}
              >
                {getQuizTypeLabel(type)}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Questions */}
      <div className="questions-container">
        {currentQuiz.questions.map((q, idx) =>
          renderQuestion(q, idx, currentQuizType)
        )}
      </div>

      {/* Submit Button */}
      <div className="quiz-footer">
        <button
          className="btn-submit"
          onClick={handleSubmitQuiz}
          disabled={answeredCount === 0}
        >
          Submit Quiz ({answeredCount} / {currentQuiz.total_questions} answered)
        </button>
      </div>
    </div>
  );
}

