# Community Skill Sharing Platform

A full-stack web application that lets users register their skills, browse a community skill directory, and participate in a categorized discussion forum — all backed by a relational MySQL database.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend / UI | Python · Streamlit |
| Backend Logic | Python |
| Database | MySQL |
| DB Connector | `mysql-connector-python` |
| Data Handling | Pandas |

---

## Features

### Authentication
- Session-based login with username and password
- Authenticated state persisted across Streamlit pages via `st.session_state`

### User Skills (Full CRUD)
- **Add** a skill from a predefined catalogue with a proficiency level (Beginner / Intermediate / Advanced)
- **Update** the proficiency level of an existing skill
- **Delete** a skill from your profile
- Duplicate skill entries are prevented at the application level

### Community Forum
- Browse all **forum threads** with post counts and author info
- View **questions** and **answers** separately, with timestamps
- Post types supported: `Question`, `Answer`, `Comment`

### Advanced SQL Features (exposed via UI)
- **Stored Procedure** — `GetPostsInThread(thread_id)`: retrieves all posts belonging to a thread
- **Stored Function** — `GetTotalPosts(user_id)`: returns the total number of posts by a user
- **Trigger** — demonstrates a `BEFORE UPDATE` trigger on `forum_post`; the UI shows the table state before and after an update to make the trigger's effect visible

---

## Database Schema

```
user           — user_id, first_name, last_name, username, password
skill          — skill_id, skill_name
userskill      — (user_id, skill_id) PK, skill_level
forum_thread   — thread_id, title, user_id
forum_category — forum_category_id, category_name
forum_post     — post_id, content, post_date, user_id, thread_id,
                 forum_category_id, post_type, parent_post_id
```

Foreign key relationships enforce referential integrity across all tables.

---

## Setup & Installation

### Prerequisites
- Python 3.8+
- MySQL Server running locally

### 1. Clone the repository
```bash
git clone https://github.com/neelalohith/CommunitySkillSharingPlatform.git
cd CommunitySkillSharingPlatform
```

### 2. Install dependencies
```bash
pip install streamlit pandas mysql-connector-python
```

### 3. Set up the database
Import the SQL schema and seed data:
```bash
mysql -u root -p < CommunitySkillSharingPlatform.sql
```

### 4. Configure the DB connection
Open `CommunitySkillSharingPlatform.py` and update the connection block with your credentials:
```python
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="your_password",   # <-- change this
    database="temp"
)
```

### 5. Run the app
```bash
streamlit run CommunitySkillSharingPlatform.py
```

The app will open at `http://localhost:8501`.

### Default Login Credentials (seed data)
| Username | Password |
|---|---|
| john_doe | password123 |
| jane_smith | pass456 |
| bob_j | securepass |

---

## Project Structure

```
CommunitySkillSharingPlatform/
├── CommunitySkillSharingPlatform.py   # Main Streamlit application
├── CommunitySkillSharingPlatform.sql  # Schema DDL + seed data
├── details.txt                        # Project notes
└── README.md
```

---

## Pages Overview

| Page | Description |
|---|---|
| Home | Login screen; authenticates user and sets session |
| User Skills | View, add, update, and delete skills for the logged-in user |
| Community Forum | Read-only view of threads, questions, and answers |
| Procedure | UI to call `GetPostsInThread` stored procedure |
| Function | UI to call `GetTotalPosts` stored function |
| Trigger | Demonstrates a DB trigger with before/after table views |
