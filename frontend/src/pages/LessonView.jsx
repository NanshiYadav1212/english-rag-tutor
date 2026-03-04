

// // import React, { useEffect, useState } from 'react';
// // import FeedbackPanel from '../components/FeedbackPanel';
// // import LessonContent from '../components/LessonContent';
// // import { api } from '../utils/api';
// // import './lessonview.css';

// // export default function LessonView({ lessonId, token }) {
// //   const [input, setInput] = useState('');
// //   const [submissions, setSubmissions] = useState([]);
// //   const [loading, setLoading] = useState(true);
// //   const [errorMsg, setErrorMsg] = useState(null);

// //   useEffect(() => {
// import React, { useEffect, useState } from 'react';
// import FeedbackPanel from '../components/FeedbackPanel';
// import LessonContent from '../components/LessonContent';
// import Quiz from '../components/Quiz';
// import { api } from '../utils/api';
// import './lessonview.css';

// export default function LessonView({ lessonId, token }) {
//   const [submissions, setSubmissions] = useState([]);
//   const [loading, setLoading] = useState(true);
//   const [errorMsg, setErrorMsg] = useState(null);
//   const [lesson, setLesson] = useState(null);

//   // Fetch lesson content
//   useEffect(() => {
//     const fetchLesson = async () => {
//       if (!lessonId) return;
//       try {
//         const res = await api(token).get(`/lessons/${lessonId}`);
//         setLesson(res.data);
//       } catch (err) {
//         console.error('Failed to load lesson:', err);
//         setErrorMsg('Failed to load lesson content.');
//       }
//     };
//     fetchLesson();
//   }, [lessonId, token]);

//   // Fetch previous submissions
//   useEffect(() => {
//     const fetchSubmissions = async () => {
//       if (!lessonId) return;
//       setLoading(true);
//       setErrorMsg(null);
//       try {
//         const res = await api(token).get('/progress');
//         const recent = res.data.recent
//           .filter((s) => s.lesson_id === lessonId)
//           .reverse();
//         setSubmissions(recent);
//       } catch (err) {
//         console.error('Failed to fetch progress:', err);
//         setErrorMsg('Failed to load previous submissions.');
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchSubmissions();
//   }, [lessonId, token]);

//   if (!lesson) return <p>Loading lesson...</p>;

//   return (
//     <div className="lessonview-wrapper">
//       {/* Lesson Content */}
//       <LessonContent lessonId={lessonId} token={token} />

//       {/* User Input / Quiz Section */}
//       <div className="answer-box">
//         <Quiz lessonId={lessonId} exercises={lesson.content?.exercises || []} token={token} />
//       </div>

//       {/* Feedback / History */}
//       <div className="feedback-list">
//         {loading ? (
//           <p>Loading previous submissions...</p>
//         ) : submissions.length === 0 ? (
//           <p>No submissions yet. Be the first!</p>
//         ) : (
//           submissions.map((fb, i) => (
//             <FeedbackPanel key={i} feedback={fb} token={token} />
//           ))
//         )}
//       </div>
//     </div>
//   );
// }
//   const [lesson, setLesson] = useState(null);

//   // Fetch lesson content
//   useEffect(() => {
//     const fetchLesson = async () => {
//       if (!lessonId) return;
//       try {
//         const res = await api(token).get(`/lessons/${lessonId}`);
//         setLesson(res.data);
//       } catch (err) {
//         console.error('Failed to load lesson:', err);
//         setErrorMsg('Failed to load lesson content.');
//       }
//     };
//     fetchLesson();
//   }, [lessonId, token]);

//   // Fetch previous submissions
//   useEffect(() => {
//     const fetchSubmissions = async () => {
//       if (!lessonId) return;
//       setLoading(true);
//       setErrorMsg(null);
//       try {
//         const res = await api(token).get('/progress');
//         const recent = res.data.recent
//           .filter((s) => s.lesson_id === lessonId)
//           .reverse();
//         setSubmissions(recent);
//       } catch (err) {
//         console.error('Failed to fetch progress:', err);
//         setErrorMsg('Failed to load previous submissions.');
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchSubmissions();
//   }, [lessonId, token]);

//   // (Quiz handles submissions now)

//   if (!lesson) return <p>Loading lesson...</p>;

//   return (
//     <div className="lessonview-wrapper">
//       {/* Lesson Content */}
//       <LessonContent lessonId={lessonId} token={token} />

//       {/* User Input / Quiz Section */}
//       <div className="answer-box">
//         <Quiz lessonId={lessonId} exercises={lesson.content?.exercises || []} token={token} />
//       </div>

//       {/* Feedback / History */}
//       <div className="feedback-list">
//         {loading ? (
//           <p>Loading previous submissions...</p>
//         ) : submissions.length === 0 ? (
//           <p>No submissions yet. Be the first!</p>
//         ) : (
//           submissions.map((fb, i) => (
//             <FeedbackPanel key={i} feedback={fb} token={token} />
//           ))
//         )}
//       </div>
//     </div>
//   );


import React, { useEffect, useState } from 'react';
import FeedbackPanel from '../components/FeedbackPanel';
import LessonContent from '../components/LessonContent';
import Quiz from '../components/Quiz';
import { api } from '../utils/api';
import './lessonview.css';

export default function LessonView({ lessonId, token }) {
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [errorMsg, setErrorMsg] = useState(null);
  const [lesson, setLesson] = useState(null);

  // Fetch lesson content
  useEffect(() => {
    if (!lessonId) return;
    const fetchLesson = async () => {
      try {
        const res = await api(token).get(`/lessons/${lessonId}`);
        setLesson(res.data);
      } catch (err) {
        console.error('Failed to load lesson:', err);
        setErrorMsg('Failed to load lesson content.');
      }
    };
    fetchLesson();
  }, [lessonId, token]);

  // Fetch previous submissions
  useEffect(() => {
    if (!lessonId) return;
    const fetchSubmissions = async () => {
      setLoading(true);
      setErrorMsg(null);
      try {
        const res = await api(token).get('/progress');
        const recent = res.data.recent
          .filter((s) => s.lesson_id === lessonId)
          .reverse();
        setSubmissions(recent);
      } catch (err) {
        console.error('Failed to fetch progress:', err);
        setErrorMsg('Failed to load previous submissions.');
      } finally {
        setLoading(false);
      }
    };
    fetchSubmissions();
  }, [lessonId, token]);

  if (!lesson) return <p>Loading lesson...</p>;
  if (errorMsg) return <p className="error-text">{errorMsg}</p>;

  return (
    <div className="lessonview-wrapper">
      {/* Lesson Content */}
      <LessonContent lessonId={lessonId} token={token} />

      {/* User Input / Quiz Section */}
      <div className="answer-box">
        <Quiz lessonId={lessonId} exercises={lesson.content?.exercises || []} token={token} />
      </div>

      {/* Feedback / History */}
      <div className="feedback-list">
        {loading ? (
          <p>Loading previous submissions...</p>
        ) : submissions.length === 0 ? (
          <p>No submissions yet. Be the first!</p>
        ) : (
          submissions.map((fb, i) => <FeedbackPanel key={i} feedback={fb} token={token} />)
        )}
      </div>
    </div>
  );
}
