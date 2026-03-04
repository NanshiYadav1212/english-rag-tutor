// import React, { useEffect, useState } from 'react';
// import LessonCard from '../components/LessonCard';
// import LessonDetail from '../components/LessonDetail';
// import QuizInterface from '../components/QuizInterface';
// // ...existing code...
// import { api } from '../utils/api';
// import './Dashboard.css';

// import { Book, BarChart3, Download, LogOut } from 'lucide-react';
// import MyProfile from '../components/MyProfile';


// export default function Dashboard({ token, onLogout }) {
//   const [lessons, setLessons] = useState([]);
//   // view: 'lessons', 'lesson-detail', 'quiz', 'profile'
//   const [view, setView] = useState('lessons');
//   const [selectedLessonSlug, setSelectedLessonSlug] = useState(null);
//   const [loading, setLoading] = useState(true);
//   const [errorMsg, setErrorMsg] = useState(null);
//   const [profile, setProfile] = useState(() => {
//     // Optionally, load from localStorage or API in the future
//     const saved = localStorage.getItem('userProfile');
//     return saved ? JSON.parse(saved) : null;
//   });

//   // Save profile to localStorage on change
//   useEffect(() => {
//     if (profile) {
//       localStorage.setItem('userProfile', JSON.stringify(profile));
//     }
//   }, [profile]);

//   // Fetch lessons only
//   useEffect(() => {
//     const loadData = async () => {
//       setLoading(true);
//       setErrorMsg(null);
//       try {
//         const lessonsRes = await api(token).get('/lessons');
//         const serverLessons = lessonsRes.data || [];
//         setLessons(serverLessons);
//       } catch (err) {
//         console.error('Failed to load lessons:', err);
//         setErrorMsg('Failed to load lessons. Please try again.');
//       } finally {
//         setLoading(false);
//       }
//     };
//     loadData();
//   }, [token]);

//   // ...existing code...

//   const handleStartQuiz = (lessonSlug) => {
//     console.log('handleStartQuiz called for', lessonSlug);
//     setSelectedLessonSlug(lessonSlug);
//     setView('quiz');
//   };

//   const handleBack = () => {
//     setView('lessons');
//     setSelectedLessonSlug(null);
//   };


//   const handleQuizComplete = async () => {
//     setView('lessons');
//     setSelectedLessonSlug(null);
//   };

//   if (loading) {
//     return (
//       <div className="dashboard-wrapper">
//         <div style={{ textAlign: 'center', padding: '3rem' }}>
//           <div className="spinner"></div>
//           <p style={{ marginTop: '1rem', color: '#666' }}>Loading dashboard...</p>
//         </div>
//       </div>
//     );
//   }

//   if (errorMsg) {
//     return (
//       <div className="dashboard-wrapper">
//         <div className="error-banner">{errorMsg}</div>
//       </div>
//     );
//   }

//   return (
//     <div className="dashboard-wrapper">
//       {/* Header */}
//       <header className="dashboard-header">
//         <div className="header-content">
//           <h1 className="app-title">Language Tutor</h1>
//           <p className="app-subtitle">Master English with interactive lessons</p>
//         </div>
//         <div className="header-actions">
//           <button 
//             className="btn-icon danger" 
//             onClick={onLogout}
//             title="Logout"
//           >
//             <LogOut size={18} />
//             Logout
//           </button>
//         </div>
//       </header>

//       {/* Navigation Tabs */}

//       <div className="dashboard-nav">
//         <button
//           className={`nav-tab ${view === 'profile' ? 'active' : ''}`}
//           onClick={() => setView('profile')}
//         >
//           <span role="img" aria-label="profile" style={{marginRight: 6}}>👤</span>
//           My Profile
//         </button>
//         <button
//           className={`nav-tab ${view === 'lessons' ? 'active' : ''}`}
//           onClick={() => setView('lessons')}
//         >
//           <Book size={18} />
//           Lessons
//         </button>
 
//       </div>

//       {/* Content Area */}
//       <div className="dashboard-content">
//         {view === 'profile' && (
//           <MyProfile profile={profile} onProfileChange={setProfile} />
//         )}

//         {view === 'lessons' && (
//           <div className="lessons-view">
//             <h2 className="section-title">Available Lessons</h2>
//             <div className="cards-grid">
//               {lessons.map((lesson) => (
//                 <LessonCard
//                   key={lesson._id || lesson.slug}
//                   lesson={lesson}
//                   onSelect={() => {
//                     setSelectedLessonSlug(lesson.slug);
//                     setView('lesson-detail');
//                   }}
//                   token={token}
//                 />
//               ))}
//             </div>
//           </div>
//         )}

//         {view === 'lesson-detail' && selectedLessonSlug && (
//           <LessonDetail
//             lessonSlug={selectedLessonSlug}
//             token={token}
//             onBack={handleBack}
//             onStartQuiz={handleStartQuiz}
//           />
//         )}

//         {view === 'quiz' && selectedLessonSlug && (
//           <QuizInterface
//             lessonSlug={selectedLessonSlug}
//             token={token}
//             onBack={handleBack}
//             onComplete={handleQuizComplete}
//           />
//         )}

//         {/* Progress view removed */}
//       </div>
//     </div>
//   );
// }


import React, { useEffect, useState } from 'react';
import { Book, BarChart3, LogOut } from 'lucide-react';

import LessonCard from '../components/LessonCard';
import LessonDetail from '../components/LessonDetail';
import QuizInterface from '../components/QuizInterface';
import MyProfile from '../components/MyProfile';
import SmartTutorSection from '../components/SmartTutorSection';

import { api } from '../utils/api';
import './Dashboard.css';

export default function Dashboard({ token, onLogout }) {
  const [view, setView] = useState('lessons');
  const [lessons, setLessons] = useState([]);
  const [selectedLessonSlug, setSelectedLessonSlug] = useState(null);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);

  const [profile, setProfile] = useState(() => {
    const saved = localStorage.getItem('userProfile');
    return saved ? JSON.parse(saved) : null;
  });

  /* ---------------- Save profile ---------------- */
  useEffect(() => {
    if (profile) {
      localStorage.setItem('userProfile', JSON.stringify(profile));
    }
  }, [profile]);

  /* ---------------- Load lessons ---------------- */
  useEffect(() => {
    const loadLessons = async () => {
      setLoading(true);
      setErrorMsg(null);
      try {
        const res = await api(token).get('/lessons');
        setLessons(res.data || []);
      } catch (err) {
        console.error(err);
        setErrorMsg('Failed to load lessons. Please try again.');
      } finally {
        setLoading(false);
      }
    };
    loadLessons();
  }, [token]);

  /* ---------------- Handlers ---------------- */
  const openLesson = (slug) => {
    setSelectedLessonSlug(slug);
    setView('lesson-detail');
  };

  const startQuiz = (slug) => {
    setSelectedLessonSlug(slug);
    setView('quiz');
  };

  const goBackToLessons = () => {
    setSelectedLessonSlug(null);
    setView('lessons');
  };

  const onQuizComplete = () => {
    setSelectedLessonSlug(null);
    setView('lessons');
  };

  /* ---------------- Loading & Error ---------------- */
  if (loading) {
    return (
      <div className="dashboard-wrapper">
        <div className="center-box">
          <div className="spinner"></div>
          <p>Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (errorMsg) {
    return (
      <div className="dashboard-wrapper">
        <div className="error-banner">{errorMsg}</div>
      </div>
    );
  }

  /* ---------------- UI ---------------- */
  return (
    <div className="dashboard-wrapper">
      {/* Header */}
      <header className="dashboard-header">
        <div>
          <h1 className="app-title">Language Tutor</h1>
          <p className="app-subtitle">Master English with interactive lessons</p>
        </div>
        <button className="btn-icon danger" onClick={onLogout}>
          <LogOut size={18} />
          Logout
        </button>
      </header>

      {/* Navigation */}
      <div className="dashboard-nav">
        <button
          className={`nav-tab ${view === 'profile' ? 'active' : ''}`}
          onClick={() => setView('profile')}
        >
          👤 My Profile
        </button>

        <button
          className={`nav-tab ${view === 'lessons' ? 'active' : ''}`}
          onClick={() => setView('lessons')}
        >
          <Book size={18} /> Lessons
        </button>

        <button
          className={`nav-tab ${view === 'smart-tutor' ? 'active' : ''}`}
          onClick={() => setView('smart-tutor')}
        >
          <BarChart3 size={18} /> Smart Learning
        </button>
      </div>

      {/* Content */}
      <div className="dashboard-content">
        {view === 'profile' && (
          <MyProfile profile={profile} onProfileChange={setProfile} />
        )}

        {view === 'smart-tutor' && (
          <SmartTutorSection />
        )}

        {view === 'lessons' && (
          <div className="lessons-view">
            <h2 className="section-title">Available Lessons</h2>
            <div className="cards-grid">
              {lessons.map((lesson) => (
                <LessonCard
                  key={lesson._id || lesson.slug}
                  lesson={lesson}
                  token={token}
                  onSelect={() => openLesson(lesson.slug)}
                />
              ))}
            </div>
          </div>
        )}

        {view === 'lesson-detail' && selectedLessonSlug && (
          <LessonDetail
            lessonSlug={selectedLessonSlug}
            token={token}
            onBack={goBackToLessons}
            onStartQuiz={startQuiz}
          />
        )}

        {view === 'quiz' && selectedLessonSlug && (
          <QuizInterface
            lessonSlug={selectedLessonSlug}
            token={token}
            onBack={goBackToLessons}
            onComplete={onQuizComplete}
          />
        )}
      </div>
    </div>
  );
}
