import streamlit as st
import pandas as pd
import mysql.connector

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False


# Function to fetch data from the database
def fetch_data(query, conn, params=None):
    try:
        if params:
            return pd.read_sql_query(query, conn, params=params)
        else:
            return pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"Error fetching data from the database: {e}")
        return pd.DataFrame()

# Function to execute SQL queries
def execute_query(query, conn, params=None):
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        conn.commit()
    except Exception as e:
        st.error(f"Error executing query: {e}")

# Function to authenticate user
def authenticate_user(username, password, conn):
    query = "SELECT user_id FROM user WHERE username = %s AND password = %s"
    params = (username, password)

    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    if result:
        return result[0][0]
    return None

# Function to fetch user skills
def fetch_user_skills(user_id, conn):
    if user_id is not None:
        query = "SELECT s.skill_name, us.skill_level FROM userskill us " \
                "JOIN skill s ON us.skill_id = s.skill_id " \
                "WHERE us.user_id = %s"
        params = (user_id,)
        return fetch_data(query, conn, params)
    else:
        return pd.DataFrame()


# Function to create a new user skill
def create_user_skill(user_id, skill_id, skill_level, conn):
    # Check if the user already has the skill
    check_query = "SELECT 1 FROM userskill WHERE user_id = %s AND skill_id = %s;"
    check_params = (int(user_id), int(skill_id))
    skill_exists = fetch_data(check_query, conn, params=check_params)

    if skill_exists.empty:
        # If the skill doesn't exist, insert it
        insert_query = "INSERT INTO userskill (user_id, skill_id, skill_level) VALUES (%s, %s, %s);"
        insert_params = (int(user_id), int(skill_id), str(skill_level))
        execute_query(insert_query, conn, params=insert_params)
        st.success(f"Skill added successfully!")
    else:
        st.warning("Duplicate skill.")

# Function to update an existing user skill
def update_user_skill(user_id, skill_id, skill_level, conn):
    query = "UPDATE userskill SET skill_level = %s WHERE user_id = %s AND skill_id = %s"
    params = (str(skill_level), int(user_id), int(skill_id))
    execute_query(query, conn, params)

# Function to delete a user skill
def delete_user_skill(user_id, skill_id, conn):
    query = "DELETE FROM userskill WHERE user_id = %s AND skill_id = %s"
    params = (int(user_id), int(skill_id))
    execute_query(query, conn, params)

# Connect to the MySQL database
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1202102192",
        database="temp"
    )
    st.success("Connected to the database successfully.")
except mysql.connector.Error as e:
    st.error(f"Error connecting to the database: {e}")

# Initialize session state
def initialize_session():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'page' not in st.session_state:
        st.session_state.page = 'Home'
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None  # Initialize session_id to None

# Sidebar
st.sidebar.title("Community Skill Sharing Platform")
selected_page = st.sidebar.radio("Select a page", ["Home", "User Skills","Community Forum", "Procedure", "Function","Trigger"])

# Home Page
if selected_page == 'Home':
    st.markdown(
        """
        <h1>Welcome to the Community Skill Sharing Platform!</h1>
        """
        "<div>Explore user skills and participate in discussions on the forum.</div>",
        unsafe_allow_html=True,
    )

    # Display login form
    if not st.session_state.authenticated:
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.button("Log In")

        if login_button:
            # Authenticate user
            user_id = authenticate_user(username, password, conn)
            if user_id is not None:
                st.session_state.authenticated = True
                st.session_state.session_id = user_id
                st.session_state.page = 'User Skills'  # Redirect to user skills page
                st.success("Login successful!")

elif selected_page == 'User Skills':
    st.title("User Skills")
    user_id = st.session_state.session_id
    user_skills_df = fetch_user_skills(user_id, conn)

    st.subheader("Your Skills")
    st.dataframe(user_skills_df)

    # CRUD operations
    st.sidebar.subheader("Manage Skills")
    selected_operation = st.sidebar.radio("Select operation", ["Add Skill", "Update Skill", "Delete Skill"])

    if selected_operation == "Add Skill":
        available_skill_names = fetch_data("SELECT skill_name FROM skill;", conn)["skill_name"].tolist()
        new_skill_name = st.selectbox("Select Skill", available_skill_names)
        new_skill_level = st.selectbox("Select skill level", ["Beginner", "Intermediate", "Advanced"])

        if st.button("Add Skill"):
            # Get the skill_id for the selected skill
            skill_id_query = "SELECT skill_id FROM skill WHERE skill_name = %s;"
            skill_id_result = fetch_data(skill_id_query, conn, params=(new_skill_name,))

            if not skill_id_result.empty:
                skill_id = skill_id_result.iloc[0]['skill_id']
                create_user_skill(user_id, skill_id, new_skill_level, conn)
                #st.success(f"Skill '{new_skill_name}' added successfully!")

                # Display the updated user skills table
                user_skills_df = fetch_user_skills(user_id, conn)
                st.subheader("Your Skills (Updated)")
                st.dataframe(user_skills_df)
            else:
                st.warning(f"Skill '{new_skill_name}' does not exist in the system.")



    elif selected_operation == "Update Skill":
        # Update Skill functionality
        st.subheader("Update Skill")
        skill_to_update = st.selectbox("Select skill to update", user_skills_df['skill_name'].unique())
        new_skill_level = st.selectbox("Select new skill level", ["Beginner", "Intermediate", "Advanced"])
        
        if st.button("Update Skill"):
            skill_id_query = "SELECT skill_id FROM skill WHERE skill_name = %s;"
            skill_id_result = fetch_data(skill_id_query, conn, params=(skill_to_update,))
            
            if not skill_id_result.empty:
                skill_id = skill_id_result.iloc[0]['skill_id']
                update_user_skill(user_id, skill_id, new_skill_level, conn)
                st.success(f"Skill '{skill_to_update}' updated successfully!")

                # Display the updated user skills table
                user_skills_df = fetch_user_skills(user_id, conn)
                st.subheader("Your Skills (Updated)")
                st.dataframe(user_skills_df)
            else:
                st.warning(f"Skill '{skill_to_update}' not found in the system.")

    elif selected_operation == "Delete Skill":
        # Delete Skill functionality
        st.subheader("Delete Skill")
        skill_to_delete = st.selectbox("Select skill to delete", user_skills_df['skill_name'].unique())
        
        if st.button("Delete Skill"):
            skill_id_query = "SELECT skill_id FROM skill WHERE skill_name = %s;"
            skill_id_result = fetch_data(skill_id_query, conn, params=(skill_to_delete,))
            
            if not skill_id_result.empty:
                skill_id = skill_id_result.iloc[0]['skill_id']
                delete_user_skill(user_id, skill_id, conn)
                st.success(f"Skill '{skill_to_delete}' deleted successfully!")

                # Display the updated user skills table
                user_skills_df = fetch_user_skills(user_id, conn)
                st.subheader("Your Skills (Updated)")
                st.dataframe(user_skills_df)
            else:
                st.warning(f"Skill '{skill_to_delete}' not found in the system.")


    # Community Forum Page
elif selected_page == "Community Forum":
    st.title("Community Forum")
    # Topics
    forum_topics_query = '''
    SELECT
    ft.thread_id,
    ft.title AS thread_title,
    u.first_name AS user_first_name,
    u.last_name AS user_last_name,
    COUNT(fp.post_id) AS num_posts
FROM
    forum_thread ft
    LEFT JOIN user u ON ft.user_id = u.user_id
    LEFT JOIN forum_post fp ON ft.thread_id = fp.thread_id
GROUP BY
    ft.thread_id, ft.title, u.first_name, u.last_name;   
    '''
    forum_topics_df = pd.read_sql_query(forum_topics_query, conn)

    st.write("## Forum Topics")
    st.dataframe(forum_topics_df)

    # Questions
    forum_questions_query = '''
SELECT
    u.first_name AS user_first_name,
    u.last_name AS user_last_name,
    ft.title AS thread_title,
    fp.content AS question,
    DATE_FORMAT(fp.post_date, '%Y-%m-%d') AS question_date,
    TIME_FORMAT(fp.post_date, '%H:%i:%s') AS question_time
FROM
    forum_thread ft
    JOIN forum_post fp ON ft.thread_id = fp.thread_id
    JOIN user u ON fp.user_id = u.user_id
WHERE
    fp.post_type = 'question';
'''
    forum_questions_df = pd.read_sql_query(forum_questions_query, conn)

    st.write("## Forum Questions")
    st.dataframe(forum_questions_df)

    # Answers
    forum_answers_query = '''
   SELECT
    ft.title AS thread_title,
    u.first_name AS user_first_name,
    u.last_name AS user_last_name,
    fp.content AS answer,
    DATE_FORMAT(fp.post_date, '%Y-%m-%d') AS answer_date,
    TIME_FORMAT(fp.post_date, '%H:%i:%s') AS answer_time
FROM
    forum_thread ft
    LEFT JOIN forum_post fp ON ft.thread_id = fp.thread_id
    LEFT JOIN user u ON fp.user_id = u.user_id
WHERE
    fp.post_type = 'answer';
'''
    forum_answers_df = pd.read_sql_query(forum_answers_query, conn)

    st.write("## Forum Answers")
    st.dataframe(forum_answers_df)


elif selected_page == "Procedure":
    with conn.cursor() as cursor:
        a = st.text_input("thread_id")
        if st.button("Retrieve posts"):
            q = "CALL GetPostsInThread(%s);"
            cursor.execute(q, (a,))
            # Fetch all result sets before committing
            res = cursor.fetchall()
            
            # Process the result
            columns = ['post_id', 'content', 'date', 'user_id', 'thread_id', 'forum_category_id', 'post_type', 'parent_post_id']
            df = pd.DataFrame(res, columns=columns)
            st.table(df)

elif selected_page == "Function":
    with conn.cursor() as cursor:
        a = st.text_input("user_id")
        if st.button("Get number of posts"):
            q = "SELECT GetTotalPosts(%s);"
            cursor.execute(q, (a,))
            # Fetch all result sets before displaying
            res = cursor.fetchall()
            
            # Process the result
            columns = ['count of number of posts']
            df = pd.DataFrame(res, columns=columns)
            st.table(df)


elif selected_page == "Trigger":
    st.title("Manage Triggers")

    # Display forum_post table before update
    with conn.cursor(dictionary=True) as cursor:
        show_before_update_query = "SELECT * FROM forum_post;"
        cursor.execute(show_before_update_query)
        before_update_data = cursor.fetchall()

        if before_update_data:
            st.write("## Forum Post Table Before Update")
            before_update_df = pd.DataFrame(before_update_data)
            st.table(before_update_df.rename(columns={'post_id': 'Post ID', 'content': 'Content', 'post_date': 'Post Date',
                                                     'user_id': 'User ID', 'thread_id': 'Thread ID',
                                                     'forum_category_id': 'Forum Category ID', 'post_type': 'Post Type',
                                                     'parent_post_id': 'Parent Post ID'}))
        else:
            st.write("No data found in the forum_post table before update.")

    # User input for content and post_id
    content = st.text_input("Enter Content:")
    post_id = st.text_input("Enter Post ID:")

    if st.button("Update Forum Post"):
        # Update the forum_post table
        with conn.cursor() as cursor:
            update_forum_post_query = f"UPDATE forum_post SET content = %s WHERE post_id = %s;"
            cursor.execute(update_forum_post_query, (content, post_id))
            st.success(f"forum_post table updated successfully for post_id {post_id}!")

        # Display forum_post table after update
        with conn.cursor(dictionary=True) as cursor:
            show_after_update_query = "SELECT * FROM forum_post;"
            cursor.execute(show_after_update_query)
            after_update_data = cursor.fetchall()

            if after_update_data:
                st.write("## Forum Post Table After Update")
                after_update_df = pd.DataFrame(after_update_data)
                st.table(after_update_df.rename(columns={'post_id': 'Post ID', 'content': 'Content', 'post_date': 'Post Date',
                                                          'user_id': 'User ID', 'thread_id': 'Thread ID',
                                                          'forum_category_id': 'Forum Category ID', 'post_type': 'Post Type',
                                                          'parent_post_id': 'Parent Post ID'}))
            else:
                st.write("No data found in the forum_post table after update.")

        # Commit after processing results
        conn.commit()


# Close the database connection
if conn:
    conn.close()




















