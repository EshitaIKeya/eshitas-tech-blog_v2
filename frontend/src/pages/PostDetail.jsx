import { useState, useEffect } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import hljs from "highlight.js/lib/core";
import python from "highlight.js/lib/languages/python";
import javascript from "highlight.js/lib/languages/javascript";
import bash from "highlight.js/lib/languages/bash";
import sql from "highlight.js/lib/languages/sql";
import "highlight.js/styles/github.css";
import ShareButtons from "../components/ShareButtons";
import ReadAloud from "../components/ReadAloud";
import api from "../api";

// Register only the languages we need (keeps bundle small)
hljs.registerLanguage("python", python);
hljs.registerLanguage("javascript", javascript);
hljs.registerLanguage("bash", bash);
hljs.registerLanguage("sql", sql);

const CATEGORY_COLORS = {
  Technology: "cat-indigo", Programming: "cat-emerald",
  FastAPI: "cat-amber", Database: "cat-pink", General: "cat-gray",
};

function PostDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const token = localStorage.getItem("token");

  const [post, setPost] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const [editingCommentId, setEditingCommentId] = useState(null);
  const [editCommentText, setEditCommentText] = useState("");
  const [reactions, setReactions] = useState([]);
  const [reactionTypes, setReactionTypes] = useState([]);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadPost();
    loadComments();
    loadReactions();
    api.get("/reaction-types").then((r) => setReactionTypes(r.data)).catch(() => {});
    if (token) api.get("/auth/me").then((r) => setCurrentUser(r.data)).catch(() => {});
  }, []);

  // Highlight code blocks after post content renders
  useEffect(() => {
    if (post) {
      document.querySelectorAll(".post-content pre code").forEach((block) => {
        hljs.highlightElement(block);
      });
    }
  }, [post]);

  async function loadPost() {
    try { const r = await api.get("/posts/" + id); setPost(r.data); }
    catch { setError("Post not found"); }
    setLoading(false);
  }
  async function loadComments() {
    try { const r = await api.get("/posts/" + id + "/comments"); setComments(r.data); }
    catch {}
  }
  async function loadReactions() {
    try { const r = await api.get("/posts/" + id + "/reaction"); setReactions(r.data); }
    catch {}
  }

  async function handleReaction(typeId) {
    if (!token) return;
    try {
      const mine = reactions.find((r) => r.user_id === currentUser?.id);
      if (mine && mine.reaction_type_id === typeId) {
        await api.delete("/posts/" + id + "/reaction");
      } else {
        await api.post("/posts/" + id + "/reaction", { reaction_type_id: typeId });
      }
      loadReactions();
    } catch {}
  }

  async function handleDeletePost() {
    if (!window.confirm("Delete this post permanently?")) return;
    try { await api.delete("/posts/" + id); navigate("/"); }
    catch { setError("Delete failed"); }
  }

  async function handleAddComment(e) {
    e.preventDefault();
    if (!token || !newComment.trim()) return;
    try { await api.post("/posts/" + id + "/comments", { content: newComment }); setNewComment(""); loadComments(); }
    catch { setError("Comment failed"); }
  }

  async function handleUpdateComment(cid) {
    try { await api.put("/comments/" + cid, { content: editCommentText }); setEditingCommentId(null); loadComments(); }
    catch { setError("Update failed"); }
  }

  async function handleDeleteComment(cid) {
    try { await api.delete("/comments/" + cid); loadComments(); }
    catch { setError("Delete failed"); }
  }

  function formatDate(d) {
    if (!d) return "";
    return new Date(d).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" });
  }
  function getReactionCount(tid) { return reactions.filter((r) => r.reaction_type_id === tid).length; }
  function isMyReaction(tid) { return reactions.some((r) => r.user_id === currentUser?.id && r.reaction_type_id === tid); }

  const isAdmin = currentUser?.role_name === "admin";
  const emojis = { like: "\uD83D\uDC4D", love: "\u2764\uFE0F", sad: "\uD83D\uDE22", angry: "\uD83D\uDE21" };

  if (loading) return <p className="loading">Loading post...</p>;
  if (!post) return <p className="error-msg">{error || "Post not found"}</p>;

  return (
    <article className="post-detail">
      {error && <p className="error-msg">{error}</p>}

      {/* Header */}
      <span className={"category-pill " + (CATEGORY_COLORS[post.category_name] || "cat-gray")}>
        {post.category_name}
      </span>
      <h1>{post.title}</h1>
      <div className="post-meta">
        <span>by {post.author_name}</span>
        <span>&middot;</span>
        <span>{formatDate(post.created_at)}</span>
        <span>&middot;</span>
        <span>{post.reading_time} min read</span>
        <span>&middot;</span>
        <span>{post.views} views</span>
      </div>

      {/* Admin actions */}
      {isAdmin && (
        <div className="admin-actions">
          <Link to={"/edit-post/" + post.id} className="btn-secondary">Edit</Link>
          <button onClick={handleDeletePost} className="btn-danger">Delete</button>
        </div>
      )}

      {/* TL;DR summary */}
      {post.summary && (
        <div className="tldr-box">
          <strong>TL;DR</strong>
          <p>{post.summary}</p>
        </div>
      )}

      {/* Read aloud + share */}
      <div className="post-actions-bar">
        <ReadAloud content={post.content} />
        <ShareButtons title={post.title} />
      </div>

      {/* Cover image */}
      {post.cover_image_url && (
        <img src={post.cover_image_url} alt="" className="post-cover-detail" />
      )}

      {/* Content */}
      <div className="post-content" dangerouslySetInnerHTML={{ __html: post.content }} />

      {/* Reactions */}
      <div className="reactions">
        {reactionTypes.map((type) => (
          <button key={type.id} onClick={() => handleReaction(type.id)} disabled={!token}
            className={"reaction-btn" + (isMyReaction(type.id) ? " active" : "")}>
            {emojis[type.name] || type.name} {getReactionCount(type.id)}
          </button>
        ))}
      </div>

      {/* Comments */}
      <section className="comments-section">
        <h3>Comments ({comments.length})</h3>
        <form onSubmit={handleAddComment} className="comment-form">
          <textarea placeholder={token ? "Write a comment..." : "Log in to comment"}
            value={newComment} onChange={(e) => setNewComment(e.target.value)} disabled={!token} />
          <button type="submit" className="btn-primary" disabled={!token}>Post Comment</button>
        </form>

        {comments.map((c) => (
          <div key={c.id} className="comment">
            {editingCommentId === c.id ? (
              <div className="comment-edit">
                <textarea value={editCommentText} onChange={(e) => setEditCommentText(e.target.value)} />
                <div className="comment-edit-actions">
                  <button onClick={() => handleUpdateComment(c.id)} className="btn-primary btn-sm">Save</button>
                  <button onClick={() => setEditingCommentId(null)} className="btn-secondary btn-sm">Cancel</button>
                </div>
              </div>
            ) : (
              <>
                <div className="comment-header">
                  <strong>{c.commenter_name || "User " + c.created_by}</strong>
                  <span>{formatDate(c.created_at)}</span>
                </div>
                <p>{c.content}</p>
                {(c.created_by === currentUser?.id || isAdmin) && (
                  <div className="comment-actions">
                    {c.created_by === currentUser?.id && (
                      <button onClick={() => { setEditingCommentId(c.id); setEditCommentText(c.content); }}>Edit</button>
                    )}
                    <button onClick={() => handleDeleteComment(c.id)} className="btn-danger-text">Delete</button>
                  </div>
                )}
              </>
            )}
          </div>
        ))}
      </section>
    </article>
  );
}

export default PostDetail;
