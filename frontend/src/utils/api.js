import axios from 'axios';

/* ==============================
   BASE URL
   Change this after deployment
============================== */
const BASE_URL = 'http://localhost:8000';

/* ==============================
   Auth / Protected APIs
============================== */
export function api(token) {
  return axios.create({
    baseURL: `${BASE_URL}/api`,
    headers: {
      Authorization: token ? `Bearer ${token}` : '',
    },
  });
}

/* ==============================
   Smart Tutor APIs (No Auth)
============================== */

// Upload learning material
export async function uploadFile(file) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${BASE_URL}/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!res.ok) {
    throw new Error('File upload failed');
  }

  return res.json();
}

// Ask tutor a question
export async function askQuestion(question) {
  const res = await fetch(
    `${BASE_URL}/ask?question=${encodeURIComponent(question)}`,
    {
      method: 'POST',
      headers: {
        Accept: 'application/json',
      },
    }
  );

  if (!res.ok) {
    throw new Error('Failed to get answer');
  }

  return res.json();
}