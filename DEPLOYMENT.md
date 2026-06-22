# Deploying Eshita's Tech Blog (Free Tier)

This guide deploys your blog for free using:
- **Neon** — free PostgreSQL database
- **Render** — free backend hosting
- **Vercel** — free frontend hosting

Total cost: $0

---

## Step 1: Push to GitHub

```bash
# In the project root folder
git init
git add .
git commit -m "Initial commit"

# Create a repo on github.com, then:
git remote add origin https://github.com/EshitaIKeya/eshitas-tech-blog.git
git branch -M main
git push -u origin main
```

---

## Step 2: Database (Neon)

1. Go to [neon.tech](https://neon.tech) and create a free account
2. Click **New Project** → name it `blog-db`
3. Copy the **connection string** (looks like `postgresql://user:pass@host/dbname`)
4. Save this — you will need it in Step 3

---

## Step 3: Backend (Render)

1. Go to [render.com](https://render.com) and create a free account
2. Click **New** → **Web Service**
3. Connect your GitHub repo
4. Settings:
   - **Name**: `eshitas-blog-api`
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add **Environment Variables**:
   - `DATABASE_URL` = your Neon connection string from Step 2
   - `SECRET_KEY` = any random string (e.g. `my-super-secret-key-2025`)
   - `ADMIN_PASSWORD` = your admin password
   - `FRONTEND_URL` = `https://your-app.vercel.app` (update after Step 4)
   - `GROQ_API_KEY` = your key (optional, for AI summaries — free, get one at console.groq.com)
6. Click **Create Web Service**
7. Wait for it to deploy (~3-5 minutes)
8. Copy your backend URL (e.g. `https://eshitas-blog-api.onrender.com`)

---

## Step 4: Frontend (Vercel)

1. Go to [vercel.com](https://vercel.com) and create a free account
2. Click **New Project** → Import your GitHub repo
3. Settings:
   - **Framework**: Create React App
   - **Root Directory**: `frontend`
4. Add **Environment Variable**:
   - `REACT_APP_API_URL` = your Render backend URL from Step 3
5. Click **Deploy**
6. Copy your frontend URL (e.g. `https://eshitas-tech-blog.vercel.app`)

---

## Step 5: Update CORS

Go back to Render → your backend service → Environment Variables.
Update `FRONTEND_URL` to your actual Vercel URL from Step 4.
Render will auto-redeploy.

---

## Done!

Your blog is now live at your Vercel URL.

- **Admin login**: username `Eshita`, password = whatever you set as `ADMIN_PASSWORD`
- **API docs**: `https://your-render-url.onrender.com/docs`

### Important notes:
- Render free tier sleeps after 15 minutes of inactivity. First visit after sleep takes ~30 seconds.
- Neon free tier has 500MB storage limit (plenty for a blog).
- Vercel free tier allows 100 deployments per day.
- AI summaries only work if you set `GROQ_API_KEY` (free at console.groq.com).
