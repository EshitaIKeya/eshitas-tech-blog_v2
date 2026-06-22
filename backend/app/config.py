import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/eshita_blog")
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-to-a-random-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme123")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
