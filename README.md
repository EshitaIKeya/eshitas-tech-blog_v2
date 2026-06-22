# Eshita's Tech Blog

A full-stack personal blog with **AI-powered summaries**, **read-aloud**, and **syntax-highlighted code blocks** — built with FastAPI, React, and PostgreSQL, running in Docker.

## What makes this blog different

- **AI-generated summaries** — admin clicks a button, Groq writes a 2-3 sentence TL;DR (optional, uses your own free API key)
- **Read aloud** — any visitor can listen to a post via the browser's built-in speech engine (free, no API)
- **Syntax highlighting** — code blocks render with proper colors (highlight.js)
- **Rich text editor** — write posts with bold, headings, lists, code blocks (Quill editor)
- **3 themes** — Light, Dark, and Eye Care mode
- **Share buttons** — copy link, share to X/Twitter, LinkedIn
- **View counter** — tracks how many times each post is read
- **Category color-coding** — each category gets a colored pill badge

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI, SQLAlchemy, Pydantic, JWT |
| Database | PostgreSQL (7 tables) |
| Frontend | React, React Router, Axios |
| Editor | react-quill-new (Quill) |
| Code highlighting | highlight.js |
| AI summaries | Groq API (optional, free tier) |
| Read aloud | Web Speech API (free, built into browsers) |
| Containerization | Docker + docker-compose |
| Tests | pytest + FastAPI TestClient |

## Quick Start — Docker (Recommended)

**You need:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash
# 1. Clone or unzip the project
cd eshitas-tech-blog

# 2. Start everything
docker-compose up --build

# 3. Wait ~2 minutes for first build, then open:
#    Frontend:  http://localhost:3000
#    API docs:  http://localhost:8000/docs
```

**Default admin:** username `Eshita` / password `changeme123`

Stop: `docker-compose down`
Reset database: `docker-compose down -v`

## Quick Start — Manual (Without Docker)

Recommended for your defense board demo if you don't have Docker installed.

### Step 1: Create the database

Open **pgAdmin 4** (or use psql), connect to your PostgreSQL server, and run:

```sql
CREATE DATABASE eshita_blog;
```

### Step 2: Start the backend

**You need:** Python 3.11+ and PostgreSQL installed.

Open a terminal in the project folder:

```powershell
# Go into backend folder
cd backend

# Create a virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate          # Windows PowerShell
# source venv/bin/activate     # Mac/Linux

# Install dependencies (takes ~1 minute)
pip install -r requirements.txt

# Create .env from the example
copy .env.example .env         # Windows
# cp .env.example .env         # Mac/Linux

# Open .env in a text editor and update DATABASE_URL with your PostgreSQL password
# Example: postgresql://postgres:YOUR_PASSWORD@localhost:5432/eshita_blog

# Start the server
uvicorn app.main:app --reload
```

Backend runs at **http://localhost:8000** and the API docs are at **http://localhost:8000/docs**.

The first time you start it, the seed script automatically creates:
- Default admin user (username `Eshita`)
- 5 categories, 4 reaction types
- 5 sample blog posts

### Step 3: Start the frontend

**You need:** Node.js 18+ installed.

Open a **second terminal** (keep backend running in the first one):

```powershell
cd frontend
npm install        # takes 2-3 minutes the first time
npm start
```

Frontend opens automatically at **http://localhost:3000**.

### Step 4: Log in as admin

- Username: `Eshita`
- Password: `changeme123` (you can change this in `.env` before running)

You're done. Click "+ New Post" in the navbar to write your first post.

## Running Tests

```bash
cd backend
pip install pytest
pytest tests/ -v
```

## Deployment (Free)

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions using Neon + Render + Vercel (all free tier).

## AI Summary Setup (Optional)

The AI feature uses **Groq**, a fast and free LLM API (different from a paid chat subscription — no credit card needed).

**How to get your free API key:**

1. Go to [console.groq.com](https://console.groq.com) and sign up (free account, no credit card required)
2. Once logged in, click **API Keys** in the left sidebar
3. Click **Create API Key**, give it a name like "blog-project", and copy the key (starts with `gsk_...`)
4. Save it immediately — you can't view it again after closing the dialog
5. Open your backend `.env` file and paste it:
   ```
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx...
   ```
6. Restart the backend (`Ctrl+C` then `uvicorn app.main:app --reload`, or `docker-compose restart backend`)

**Cost note:** Groq's free tier is generous (30 requests/minute) and requires no billing setup at all. This blog uses `llama-3.3-70b-versatile`, a fast, high-quality model well suited for short summaries.

**How to use:** When writing a post in the editor, click the "**Generate with AI**" button next to the Summary field. The AI reads your content and writes a 2-3 sentence TL;DR automatically.

The blog works perfectly without an API key — the AI button just shows an error if the key is missing. Everything else (writing posts, comments, reactions, themes, read-aloud, share) keeps working.

**Security note:** Never commit your real API key to GitHub. Keep it only in your local `.env` file, which is already excluded via `.gitignore`. If a key is ever exposed (pasted in chat, committed by mistake, shared in a screenshot), revoke it immediately from the Groq console and generate a new one.

## Project Structure

```
eshitas-tech-blog/
├── backend/
│   ├── app/
│   │   ├── models/         # Database tables (SQLAlchemy)
│   │   ├── schemas/        # Request/response validation (Pydantic)
│   │   ├── routers/        # API endpoints (FastAPI)
│   │   ├── utils/          # Hashing, JWT, AI summary
│   │   ├── main.py         # App entry + CORS + router registration
│   │   ├── database.py     # DB connection
│   │   ├── config.py       # Environment variables
│   │   ├── dependencies.py # Auth (Bearer token)
│   │   └── seed.py         # Default data + sample posts
│   ├── tests/              # pytest API tests
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # Navbar, Footer, ThemeToggle, ShareButtons, ReadAloud
│   │   ├── pages/          # Home, Login, Register, CreatePost, PostDetail, etc.
│   │   ├── api.js          # Axios with Bearer token interceptor
│   │   ├── App.jsx         # Routes
│   │   └── App.css         # Design system (3 themes, category colors)
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
├── docker-compose.yml
├── DEPLOYMENT.md
└── README.md
```

## API Endpoints (33+)

| Area | Endpoints | Auth |
|------|----------|------|
| Auth | register, login, me, change-password | Public / Bearer |
| Posts | CRUD + pagination + search + generate-summary | Public / Admin |
| Comments | CRUD per post | Public / Bearer |
| Reactions | add/remove per post, reaction types | Public / Bearer |
| Categories | CRUD | Public / Admin |
| Roles | list, create | Admin |
| Users | list, get, delete | Admin |

Full interactive docs at `/docs` (Swagger UI).

## Built By

**Eshita Islam** — CS student, intern at Apurba Technologies Inc.

Built from scratch as a learning project covering: database design, REST APIs, JWT authentication, React frontend, Docker containerization, and AI integration.

[LinkedIn](https://www.linkedin.com/in/eshita-islam-keya-5504b230a/) · [GitHub](https://github.com/EshitaIKeya) · [Email](mailto:eshita.isk@gmail.com)
