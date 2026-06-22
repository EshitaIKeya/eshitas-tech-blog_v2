from datetime import datetime
from app.database import SessionLocal
from app.models.role import Role
from app.models.category import Category
from app.models.reaction_type import ReactionType
from app.models.user import User
from app.models.post import Post
from app.utils.hashing import hash_password
from app.config import ADMIN_PASSWORD


def add_if_missing(db, model, field, values):
    for value in values:
        exists = db.query(model).filter(field == value).first()
        if not exists:
            db.add(model(**{field.key: value}))
            print(f"  Added {model.__tablename__}: {value}")


SEED_POSTS = [
    {
        "title": "What is an API? My Journey Begins",
        "category": "General",
        "created_at": datetime(2025, 4, 5),
        "summary": "A beginner-friendly introduction to APIs using the restaurant analogy, written on my first week learning backend development at my internship.",
        "content": """<h2>My First Day Learning Backend</h2>
<p>When I started my internship at Apurba Technologies, the first thing my team lead asked me was: <strong>\"Do you know what an API is?\"</strong> I said \"kind of\" but honestly, I had no idea.</p>
<p>So here is what I learned, explained the way I wish someone had explained it to me.</p>
<h3>The Restaurant Analogy</h3>
<p>Think of a restaurant. You (the <strong>client</strong>) sit at a table and look at a menu. You tell the <strong>waiter</strong> what you want. The waiter goes to the <strong>kitchen</strong>, gets your food, and brings it back to you.</p>
<p>In this analogy:</p>
<ul>
<li><strong>You</strong> = the frontend (browser, mobile app)</li>
<li><strong>Waiter</strong> = the API</li>
<li><strong>Kitchen</strong> = the backend server + database</li>
<li><strong>Menu</strong> = the API documentation (what you can order)</li>
</ul>
<p>An API is just a <strong>set of rules</strong> that lets two pieces of software talk to each other. When your browser shows you Instagram posts, it is calling Instagram\'s API to fetch that data.</p>
<h3>Why FastAPI?</h3>
<p>My team uses Python, and they recommended <strong>FastAPI</strong> because:</p>
<ul>
<li>It is fast to learn (Python, not Java)</li>
<li>It automatically generates API documentation at <code>/docs</code></li>
<li>It validates your data automatically with Pydantic</li>
</ul>
<p>I started with a simple \"Hello World\" endpoint and it felt like magic seeing <code>{\"message\": \"Hello World\"}</code> appear in my browser. This is going to be a fun journey.</p>""",
    },
    {
        "title": "Setting Up PostgreSQL: My First Real Database",
        "category": "Database",
        "created_at": datetime(2025, 4, 25),
        "summary": "How I set up PostgreSQL and pgAdmin for the first time, and learned why databases are better than storing data in files.",
        "content": """<h2>Why Not Just Use a File?</h2>
<p>Before learning databases, I thought: why not just save data in a JSON file? My team lead gave me a simple answer: <strong>\"What happens when two users try to write to the same file at the same time?\"</strong></p>
<p>That is why we use databases. They handle multiple users, searching, filtering, and data integrity for us.</p>
<h3>Installing PostgreSQL + pgAdmin</h3>
<p>I downloaded PostgreSQL from the official site and installed <strong>pgAdmin 4</strong> as a visual tool to see my tables and data. The installation was straightforward on Windows.</p>
<h3>Key Concepts I Learned</h3>
<p><strong>Tables</strong> are like Excel spreadsheets. Each table has columns (fields) and rows (records). For my blog project, I designed these tables:</p>
<ul>
<li><code>users</code> - who can log in</li>
<li><code>posts</code> - blog articles</li>
<li><code>comments</code> - what readers write</li>
<li><code>categories</code> - how posts are organized</li>
</ul>
<p>I used <strong>dbdiagram.io</strong> to visually design my tables before writing any code. It lets you draw relationships between tables and then export to SQL. This was incredibly helpful for planning.</p>
<h3>What is SQLAlchemy?</h3>
<p>Instead of writing raw SQL like <code>SELECT * FROM users WHERE id = 1</code>, SQLAlchemy lets me write Python: <code>db.query(User).filter(User.id == 1).first()</code>. Same result, but in Python. It is called an <strong>ORM</strong> (Object Relational Mapper).</p>""",
    },
    {
        "title": "Building CRUD Endpoints: Create, Read, Update, Delete",
        "category": "FastAPI",
        "created_at": datetime(2025, 5, 15),
        "summary": "A walkthrough of building my first CRUD API with FastAPI, including what each HTTP method does and how to test them in Swagger UI.",
        "content": """<h2>The Four Operations Every App Needs</h2>
<p>Almost every application in the world does four basic things with data:</p>
<ul>
<li><strong>C</strong>reate - add new data (POST)</li>
<li><strong>R</strong>ead - get existing data (GET)</li>
<li><strong>U</strong>pdate - change data (PUT)</li>
<li><strong>D</strong>elete - remove data (DELETE)</li>
</ul>
<p>These four operations map to <strong>HTTP methods</strong>. When you fill out a signup form, your browser sends a POST request. When you scroll through posts, it sends GET requests.</p>
<h3>My First Endpoint</h3>
<pre><code>@router.get("/categories/")
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()</code></pre>
<p>This is a <strong>GET endpoint</strong> that returns all categories from the database. The <code>Depends(get_db)</code> part is FastAPI\'s way of giving each request its own database connection (called <strong>dependency injection</strong>).</p>
<h3>Testing with Swagger UI</h3>
<p>The best part of FastAPI is the automatic docs at <code>/docs</code>. I can test every endpoint right in the browser without writing any frontend code. Click \"Try it out\", fill in the data, hit \"Execute\", and see the response. This made development so much faster.</p>
<h3>What I Learned</h3>
<p>The hardest part was not the code itself, but understanding <strong>how data flows</strong>: the request comes in, FastAPI validates it with Pydantic schemas, the router function processes it, SQLAlchemy talks to PostgreSQL, and the response goes back. Once I understood that flow, everything clicked.</p>""",
    },
    {
        "title": "React Basics: Building the Frontend",
        "category": "Programming",
        "created_at": datetime(2025, 6, 5),
        "summary": "My experience learning React as a backend-first developer, covering components, state, props, and the moment my API data appeared on screen.",
        "content": """<h2>From Backend to Frontend</h2>
<p>After building the API, I needed a way for users to actually <em>see</em> the blog. That meant learning <strong>React</strong>.</p>
<p>Coming from Python, JavaScript felt strange at first. But React\'s component-based approach actually made sense: everything on the page is a reusable building block.</p>
<h3>Components = Building Blocks</h3>
<p>A <strong>component</strong> is a JavaScript function that returns HTML (well, JSX). My blog has components like <code>Navbar</code>, <code>PostCard</code>, <code>Footer</code>, and pages like <code>Home</code>, <code>Login</code>, <code>PostDetail</code>.</p>
<h3>State = Data That Changes</h3>
<p>The <code>useState</code> hook lets a component remember things. For example, my Home page tracks the list of posts:</p>
<pre><code>const [posts, setPosts] = useState([]);
const [loading, setLoading] = useState(true);</code></pre>
<p>When the page loads, I fetch posts from my API using <strong>Axios</strong> and update the state. React automatically re-renders the page with the new data.</p>
<h3>The Magical Moment</h3>
<p>The first time I saw my API data appear on a real webpage with styling and navigation, it felt like everything connected. Backend creates the data, API serves it, frontend displays it. <strong>That is full-stack development.</strong></p>
<p>I followed Dave Gray\'s React playlist on YouTube to learn the basics, and it was perfect for my learning style.</p>""",
    },
    {
        "title": "JWT Authentication: How Login Actually Works",
        "category": "Technology",
        "created_at": datetime(2025, 6, 22),
        "summary": "Understanding JWT tokens, why Bearer tokens are important for security, and a real bug I caught where tokens were being leaked in URLs.",
        "content": """<h2>The Problem: Who Is Making This Request?</h2>
<p>My blog has admin features (creating posts) and user features (commenting). The backend needs to know <strong>who</strong> is making each request. That is what authentication does.</p>
<h3>How JWT Works</h3>
<p>When you log in with your username and password:</p>
<ol>
<li>The server checks your credentials against the database</li>
<li>If correct, it creates a <strong>JWT token</strong> (a long encoded string)</li>
<li>The token contains your user ID and an expiration time</li>
<li>Your browser stores this token and sends it with every future request</li>
</ol>
<p>The server can decode the token to know who you are, without asking for your password every time.</p>
<h3>A Security Bug I Caught</h3>
<p>In my first version, I was passing the token as a URL parameter: <code>/auth/me?token=abc123</code>. This seems to work, but it is actually a <strong>security vulnerability</strong>. URL parameters get saved in browser history, server logs, and can leak through the Referer header.</p>
<p>The correct way is to send tokens in the <strong>Authorization header</strong>:</p>
<pre><code>Authorization: Bearer eyJhbGciOiJIUzI1NiIs...</code></pre>
<p>I fixed this by adding an Axios interceptor that automatically attaches the token to every request header. This was one of the most important lessons I learned: <strong>security matters from day one</strong>, not as an afterthought.</p>
<h3>Role-Based Access</h3>
<p>My blog checks the user\'s role dynamically: <code>db.query(Role).filter(Role.role_name == \"admin\")</code>. I never hardcode role IDs like <code>if role_id == 1</code> because IDs can change between databases. Always check by name.</p>""",
    },
]


def seed_data():
    db = SessionLocal()
    try:
        print("Seeding database...")

        add_if_missing(db, Role, Role.role_name, ["user", "admin"])
        db.commit()

        add_if_missing(db, Category, Category.name, [
            "Technology", "Programming", "FastAPI", "Database", "General"
        ])

        add_if_missing(db, ReactionType, ReactionType.name, [
            "like", "love", "sad", "angry"
        ])

        # Create admin user if none exists
        admin_role = db.query(Role).filter(Role.role_name == "admin").first()
        admin_exists = db.query(User).filter(User.role_id == admin_role.id).first()

        if not admin_exists:
            admin_user = User(
                username="Eshita",
                email="admin@blog.com",
                hashed_password=hash_password(ADMIN_PASSWORD),
                role_id=admin_role.id,
            )
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            print("  Default admin created: username=Eshita")
        else:
            admin_user = db.query(User).filter(User.role_id == admin_role.id).first()

        # Seed blog posts if none exist
        if db.query(Post).count() == 0:
            for post_data in SEED_POSTS:
                category = db.query(Category).filter(
                    Category.name == post_data["category"]
                ).first()
                if category:
                    post = Post(
                        title=post_data["title"],
                        content=post_data["content"],
                        summary=post_data["summary"],
                        user_id=admin_user.id,
                        category_id=category.id,
                        created_at=post_data["created_at"],
                    )
                    db.add(post)
                    print(f"  Added post: {post_data['title']}")

        db.commit()
        print("Seed complete!")

    except Exception as e:
        db.rollback()
        print(f"Seed error: {e}")
    finally:
        db.close()
