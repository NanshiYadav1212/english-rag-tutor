import React, { useState } from "react";
import "./SmartTutorSection.css";
import ReactMarkdown from "react-markdown";
import { askQuestion, uploadFile } from "../utils/api";

export default function SmartTutorSection() {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    if (!q.trim()) return;
    setLoading(true);
    setAns("");
    try {
      const res = await askQuestion(q);
      setAns(res.answer);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="smart-tutor-section">
      <div className="section-header">
        <h2>Smart Learning AI</h2>
        <div className="section-subtext">
          Upload materials and ask questions
        </div>
      </div>

      <div className="upload-area">
        <input
          type="file"
          onChange={(e) => uploadFile(e.target.files[0])}
        />
      </div>

      <div className="chat-area">
        <input
          className="question-input"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          placeholder="Ask a complex question..."
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />
        <button
          className="ask-btn"
          onClick={handleAsk}
          disabled={loading}
        >
          {loading ? "Searching..." : "Ask"}
        </button>
      </div>

      {ans && (
        <div className="answer-box">
          <ReactMarkdown>{ans}</ReactMarkdown>
        </div>
      )}
    </div>
  );
}
