import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

function Profile() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!localStorage.getItem("token")) { navigate("/login"); return; }
    api.get("/auth/me")
      .then((res) => { setUser(res.data); setLoading(false); })
      .catch(() => navigate("/login"));
  }, [navigate]);

  async function handleChangePassword(e) {
    e.preventDefault();
    setMessage(""); setError("");
    try {
      await api.put("/auth/change-password", { old_password: oldPassword, new_password: newPassword });
      setMessage("Password changed successfully!");
      setOldPassword(""); setNewPassword("");
    } catch (err) {
      setError(err.response?.data?.detail || "Password change failed");
    }
  }

  if (loading) return <p className="loading">Loading profile...</p>;
  if (!user) return null;

  return (
    <div className="profile-page">
      <h2>My Profile</h2>
      <div className="profile-card">
        <div className="profile-avatar">{user.username[0].toUpperCase()}</div>
        <div className="profile-info">
          <h3>{user.username}</h3>
          <p>{user.email}</p>
          <span className="role-badge">{user.role_name}</span>
        </div>
      </div>

      <div className="password-section">
        <h3>Change Password</h3>
        {message && <p className="success-msg">{message}</p>}
        {error && <p className="error-msg">{error}</p>}
        <form onSubmit={handleChangePassword}>
          <label>Current password</label>
          <input type="password" value={oldPassword} onChange={(e) => setOldPassword(e.target.value)} required />
          <label>New password</label>
          <input type="password" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
          <button type="submit" className="btn-primary">Change Password</button>
        </form>
      </div>
    </div>
  );
}

export default Profile;
