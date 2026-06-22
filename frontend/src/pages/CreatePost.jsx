import { useState, useEffect } from "react";
import { useNavigate, useParams } from "react-router-dom";
import ReactQuill from "react-quill-new";
import "react-quill-new/dist/quill.snow.css";
import api from "../api";

const toolbarOptions = [
  [{ header: [1, 2, 3, false] }],
  ["bold", "italic", "underline", "strike"],
  [{ list: "ordered" }, { list: "bullet" }],
  ["blockquote", "code-block"],
  ["link"],
  ["clean"],
];

function CreatePost() {
  const navigate = useNavigate();
  const { id } = useParams(); // If editing, id will be set
  const isEditing = Boolean(id);

  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [categoryId, setCategoryId] = useState("");
  const [summary, setSummary] = useState("");
  const [coverImageUrl, setCoverImageUrl] = useState("");
  const [categories, setCategories] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);

  useEffect(() => {
    api.get("/categories/").then((res) => setCategories(res.data)).catch(() => {});

    // If editing, load the existing post
    if (isEditing) {
      api.get("/posts/" + id).then((res) => {
        setTitle(res.data.title);
        setContent(res.data.content);
        setCategoryId(String(res.data.category_id));
        setSummary(res.data.summary || "");
        setCoverImageUrl(res.data.cover_image_url || "");
      }).catch(() => setError("Could not load post"));
    }
  }, [id, isEditing]);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    if (!title.trim()) { setError("Title is required"); return; }
    if (!content.trim() || content === "<p><br></p>") { setError("Content is required"); return; }
    if (!categoryId) { setError("Select a category"); return; }

    setLoading(true);
    try {
      const payload = {
        title: title.trim(), content, category_id: parseInt(categoryId),
        summary: summary || null, cover_image_url: coverImageUrl || null,
      };

      if (isEditing) {
        await api.put("/posts/" + id, payload);
      } else {
        await api.post("/posts/", payload);
      }
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to save post");
    }
    setLoading(false);
  }

  async function handleGenerateSummary() {
    // Require title, category, and content before generating
    if (!title.trim()) {
      setError("Please enter a title first");
      return;
    }
    if (!categoryId) {
      setError("Please select a category first");
      return;
    }
    if (!content.trim() || content === "<p><br></p>") {
      setError("Please write some content first before generating a summary");
      return;
    }

    setAiLoading(true);
    setError("");
    try {
      // Save (or update) the post first, then ask AI for a summary
      let postId = id;
      if (!postId) {
        // Creating: save the post as a draft first
        const res = await api.post("/posts/", {
          title: title.trim(), content,
          category_id: parseInt(categoryId), summary: null,
          cover_image_url: coverImageUrl || null,
        });
        postId = res.data.id;
      } else {
        // Editing: save current changes before generating
        await api.put("/posts/" + postId, {
          title: title.trim(), content, category_id: parseInt(categoryId),
          summary: null, cover_image_url: coverImageUrl || null,
        });
      }

      // Now call the AI summary endpoint
      const res = await api.post("/posts/" + postId + "/generate-summary");
      setSummary(res.data.summary);

      if (!id) {
        // Switch to edit mode so we don't double-create on next save
        navigate("/edit-post/" + postId, { replace: true });
      }
    } catch (err) {
      const detail = err.response?.data?.detail || "AI summary failed";
      if (detail.includes("GROQ_API_KEY")) {
        setError("AI summary needs an API key. Set GROQ_API_KEY in your backend .env file.");
      } else {
        setError(detail);
      }
    }
    setAiLoading(false);
  }

  return (
    <div className="create-post">
      <h2>{isEditing ? "Edit Post" : "Create New Post"}</h2>
      {error && <p className="error-msg">{error}</p>}

      <form onSubmit={handleSubmit}>
        <input type="text" placeholder="Post title" value={title}
          onChange={(e) => setTitle(e.target.value)} className="post-title-input" />

        <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)} className="category-select">
          <option value="">Select a category</option>
          {categories.map((cat) => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>

        <input type="url" placeholder="Cover image URL (optional)" value={coverImageUrl}
          onChange={(e) => setCoverImageUrl(e.target.value)} className="cover-url-input" />

        <div className="editor-wrapper">
          <ReactQuill theme="snow" value={content} onChange={setContent}
            modules={{ toolbar: toolbarOptions }} placeholder="Write your post here..." />
        </div>

        {/* AI Summary Section */}
        <div className="summary-section">
          <div className="summary-header">
            <label>Summary (shown on homepage cards)</label>
            <button type="button" onClick={handleGenerateSummary} className="btn-ai"
              disabled={aiLoading}>
              {aiLoading ? "Generating..." : "Generate with AI"}
            </button>
          </div>
          <textarea placeholder="Write a summary or click 'Generate with AI'..."
            value={summary} onChange={(e) => setSummary(e.target.value)} rows={3} />
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? "Publishing..." : (isEditing ? "Update Post" : "Publish Post")}
        </button>
      </form>
    </div>
  );
}

export default CreatePost;
