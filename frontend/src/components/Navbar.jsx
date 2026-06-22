import { Link, useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import ThemeToggle from "./ThemeToggle";
import api from "../api";

function Navbar() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [menuOpen, setMenuOpen] = useState(false);
  const token = localStorage.getItem("token");

  useEffect(() => {
    if (token) {
      api.get("/auth/me")
        .then((res) => setUser(res.data))
        .catch(() => { localStorage.removeItem("token"); setUser(null); });
    }
  }, [token]);

  function handleLogout() {
    localStorage.removeItem("token");
    setUser(null);
    navigate("/");
    window.location.reload();
  }

  return (
    <nav className="navbar">
      <Link to="/" className="nav-logo">
        <span className="logo-icon">E</span>
        <span className="logo-text">Eshita's Tech Blog</span>
      </Link>

      <button className="menu-toggle" onClick={() => setMenuOpen(!menuOpen)}>
        {menuOpen ? "\u2715" : "\u2630"}
      </button>

      <div className={"nav-links" + (menuOpen ? " open" : "")}>
        <Link to="/" onClick={() => setMenuOpen(false)}>Home</Link>
        <Link to="/about" onClick={() => setMenuOpen(false)}>About</Link>
        <Link to="/contact" onClick={() => setMenuOpen(false)}>Contact</Link>
        {user && user.role_name === "admin" && (
          <Link to="/create-post" className="btn-new-post" onClick={() => setMenuOpen(false)}>
            + New Post
          </Link>
        )}
        {user ? (
          <>
            <Link to="/profile" onClick={() => setMenuOpen(false)}>{user.username}</Link>
            <button onClick={handleLogout} className="btn-link">Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" onClick={() => setMenuOpen(false)}>Login</Link>
            <Link to="/register" onClick={() => setMenuOpen(false)}>Register</Link>
          </>
        )}
        <ThemeToggle />
      </div>
    </nav>
  );
}

export default Navbar;
