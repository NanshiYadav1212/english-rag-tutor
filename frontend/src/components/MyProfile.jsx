
import React, { useState } from 'react';
import { User, Calendar, School, GraduationCap, Mail, Phone, Edit3, Save, X } from 'lucide-react';
import './MyProfile.css';

const academicStages = [
  'Primary',
  'Secondary',
  'Higher Secondary',
  'Undergraduate',
  'Postgraduate',
  'Other',
];


export default function MyProfile({ profile, onProfileChange }) {
  const [editMode, setEditMode] = useState(false);
  const [form, setForm] = useState(profile || {
    fullName: '',
    dob: '',
    institute: '',
    academicStage: '',
    email: '',
    phone: '',
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = () => {
    setEditMode(false);
    onProfileChange(form);
  };

  // Helper for avatar initials
  const getInitials = (name) => {
    if (!name) return 'U';
    const parts = name.trim().split(' ');
    if (parts.length === 1) return parts[0][0].toUpperCase();
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  };

  return (
    <div className={`my-profile-section${editMode ? ' editing' : ''}`}>  
      <div className="profile-header">
        <div className="profile-avatar">
          <User size={48} className="avatar-icon-bg" />
          <span className="avatar-initials">{getInitials(form.fullName)}</span>
        </div>
        <div>
          <h2>My Profile</h2>
          <div className="profile-subtext">Personal details and information</div>
        </div>
      </div>
      {editMode ? (
        <form className="profile-form animate-pop" onSubmit={e => { e.preventDefault(); handleSave(); }}>
          <label>
            <User size={18} className="field-icon" /> Full Name
            <input name="fullName" value={form.fullName} onChange={handleChange} required />
          </label>
          <label>
            <Calendar size={18} className="field-icon" /> Date of Birth
            <input name="dob" type="date" value={form.dob} onChange={handleChange} required />
          </label>
          <label>
            <School size={18} className="field-icon" /> Institute
            <input name="institute" value={form.institute} onChange={handleChange} required />
          </label>
          <label>
            <GraduationCap size={18} className="field-icon" /> Academic Stage
            <select name="academicStage" value={form.academicStage} onChange={handleChange} required>
              <option value="">Select...</option>
              {academicStages.map(stage => (
                <option key={stage} value={stage}>{stage}</option>
              ))}
            </select>
          </label>
          <label>
            <Mail size={18} className="field-icon" /> Email
            <input name="email" type="email" value={form.email} onChange={handleChange} />
          </label>
          <label>
            <Phone size={18} className="field-icon" /> Phone
            <input name="phone" type="tel" value={form.phone} onChange={handleChange} />
          </label>
          <div className="profile-btn-row">
            <button type="submit" className="btn save"><Save size={16} style={{marginRight:4}}/>Save</button>
            <button type="button" className="btn cancel" onClick={() => setEditMode(false)}><X size={16} style={{marginRight:4}}/>Cancel</button>
          </div>
        </form>
      ) : (
        <div className="profile-details animate-fadein">
          <div><User size={16} className="field-icon" /> <b>Full Name:</b> {form.fullName || <span className="placeholder">Not set</span>}</div>
          <div><Calendar size={16} className="field-icon" /> <b>Date of Birth:</b> {form.dob || <span className="placeholder">Not set</span>}</div>
          <div><School size={16} className="field-icon" /> <b>Institute:</b> {form.institute || <span className="placeholder">Not set</span>}</div>
          <div><GraduationCap size={16} className="field-icon" /> <b>Academic Stage:</b> {form.academicStage || <span className="placeholder">Not set</span>}</div>
          <div><Mail size={16} className="field-icon" /> <b>Email:</b> {form.email || <span className="placeholder">Not set</span>}</div>
          <div><Phone size={16} className="field-icon" /> <b>Phone:</b> {form.phone || <span className="placeholder">Not set</span>}</div>
          <button className="btn edit" onClick={() => setEditMode(true)}><Edit3 size={16} style={{marginRight:4}}/>Edit Profile</button>
        </div>
      )}
    </div>
  );
}
