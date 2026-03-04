// import React, { useState } from 'react';
// import Dashboard from './pages/Dashboard';
// import Auth from './pages/Auth';
// import LandingPage from './pages/LandingPage';

// export default function App() {
//   const [token, setToken] = useState(localStorage.getItem('token'));
//   const [showAuth, setShowAuth] = useState(false); // controls whether to show login form

//   const handleLogin = (t) => {
//     localStorage.setItem('token', t);
//     setToken(t);
//   };

//   const handleLogout = () => {
//     localStorage.removeItem('token');
//     setToken(null);
//     setShowAuth(false); // reset to landing page after logout
//   };

//   const startAuth = () => setShowAuth(true); // called from LandingPage "Get Started" button

//   if (token) {
//     return <Dashboard token={token} onLogout={handleLogout} />;
//   }

//   return (
//     <div className="min-h-screen">
//       {!showAuth ? (
//         // Landing Page
//         <LandingPage onGetStarted={startAuth} />
//       ) : (
//         // Auth Page
//         <div className="flex items-center justify-center min-h-screen px-4">
//           <div className="w-full max-w-md">
//             <Auth 
//               onLogin={handleLogin} 
//               onBackToLanding={() => setShowAuth(false)} 
//             />
//           </div>
//         </div>
//       )}
//     </div>
//   );
// }



import React, { useState, useEffect } from 'react';
import Dashboard from './pages/Dashboard';
import Auth from './pages/Auth';
import LandingPage from './pages/LandingPage';

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [showAuth, setShowAuth] = useState(false);
  const [loading, setLoading] = useState(true);

  // Optional: validate token on mount
  useEffect(() => {
    const validateToken = async () => {
      if (token) {
        try {
          // Optionally, call a backend endpoint to verify token validity
          // await api(token).get('/auth/validate');
          setLoading(false);
        } catch (err) {
          console.warn('Invalid token, logging out.');
          handleLogout();
        }
      } else {
        setLoading(false);
      }
    };
    validateToken();
  }, [token]);

  const handleLogin = (t) => {
    localStorage.setItem('token', t);
    setToken(t);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setShowAuth(false);
  };

  const startAuth = () => setShowAuth(true);

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>;
  }

  if (token) {
    return <Dashboard token={token} onLogout={handleLogout} />;
  }

  return (
    <div className="min-h-screen transition-all duration-300 ease-in-out">
      {!showAuth ? (
        // Landing Page
        <LandingPage onGetStarted={startAuth} />
      ) : (
        // Auth Page
        <div className="flex items-center justify-center min-h-screen px-4">
          <div className="w-full max-w-md">
            <Auth 
              onLogin={handleLogin} 
              onBackToLanding={() => setShowAuth(false)} 
            />
          </div>
        </div>
      )}
    </div>
  );
}
