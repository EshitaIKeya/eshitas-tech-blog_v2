import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";

// Map category names to CSS color classes
const CATEGORY_COLORS = {
  Technology: "cat-indigo",
  Programming: "cat-emerald",
  FastAPI: "cat-amber",
  Database: "cat-pink",
  General: "cat-gray",
};

function Home() {
  const [posts, setPosts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    api.get("/categories/").then((res) => setCategories(res.data)).catch(() => {});
  }, []);

  useEffect(() => { loadPosts(); }, [page, selectedCategory]);

  async function loadPosts() {
    setLoading(true);
    setError("");
    try {
      let url = "/posts/?page=" + page + "&limit=10";
      if (selectedCategory) url += "&category_id=" + selectedCategory;
      if (searchQuery.trim()) url += "&q=" + searchQuery;
      const res = await api.get(url);
      setPosts(res.data.posts);
      setTotalPages(res.data.pages);
    } catch (err) {
      setError("Failed to load posts. Is the backend running?");
    }
    setLoading(false);
  }

  function handleSearch(e) {
    e.preventDefault();
    setPage(1);
    loadPosts();
  }

  function stripHtml(html) {
    const div = document.createElement("div");
    div.innerHTML = html;
    return div.textContent || div.innerText || "";
  }

  function formatDate(d) {
    if (!d) return "";
    return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "short", day: "numeric" });
  }

  return (
    <div className="home">
      {/* Hero section */}
      <div className="hero">
        <h1>Eshita's Tech Blog</h1>
        <p className="hero-tagline">Learning web development in public. FastAPI, React, PostgreSQL, and everything in between.</p>
      </div>

      {/* Filters */}
      <div className="filters">
        <form onSubmit={handleSearch} className="search-form">
          <input type="text" placeholder="Search posts..." value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)} />
          <button type="submit">Search</button>
        </form>
        <select value={selectedCategory} className="category-filter"
          onChange={(e) => { setSelectedCategory(e.target.value); setPage(1); }}>
          <option value="">All Categories</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>
      </div>

      {loading && <p className="loading">Loading posts...</p>}
      {error && <p className="error-msg">{error}</p>}
      {!loading && posts.length === 0 && <p className="empty-state">No posts yet. Check back soon!</p>}

      {/* Post cards */}
      <div className="post-list">
        {posts.map((post) => (
          <article key={post.id} className="post-card">
            {post.cover_image_url && (
              <img src={post.cover_image_url} alt="" className="post-cover" />
            )}
            <div className="post-card-body">
              <span className={"category-pill " + (CATEGORY_COLORS[post.category_name] || "cat-gray")}>
                {post.category_name}
              </span>
              <Link to={"/posts/" + post.id}><h2>{post.title}</h2></Link>
              <p className="post-excerpt">
                {post.summary || stripHtml(post.content).substring(0, 180) + "..."}
              </p>
              <div className="post-meta">
                <span>{post.author_name}</span>
                <span>&middot;</span>
                <span>{formatDate(post.created_at)}</span>
                <span>&middot;</span>
                <span>{post.reading_time} min read</span>
                <span>&middot;</span>
                <span>{post.views || 0} views</span>
              </div>
              <div className="post-stats">
                <span>{post.comment_count} comments</span>
                <span>&middot;</span>
                <span>{post.reaction_count} reactions</span>
              </div>
            </div>
          </article>
        ))}
      </div>

      {totalPages > 1 && (
        <div className="pagination">
          <button onClick={() => setPage(page - 1)} disabled={page <= 1}>Previous</button>
          <span>Page {page} of {totalPages}</span>
          <button onClick={() => setPage(page + 1)} disabled={page >= totalPages}>Next</button>
        </div>
      )}
    </div>
  );
}

export default Home;
