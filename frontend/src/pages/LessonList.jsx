
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

export default function LessonList() {
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    axios.get("/api/lessons/").then(res => setLessons(res.data));
  }, []);

  return (
    <div>
      <h2>Lessons</h2>
      <ul>
        {lessons.map(lesson => (
          <li key={lesson.slug}>
            <Link to={`/lessons/${lesson.slug}`}>{lesson.title}</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
