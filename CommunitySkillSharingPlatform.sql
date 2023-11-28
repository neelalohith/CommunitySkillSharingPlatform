-- Create the 'user' table
CREATE TABLE IF NOT EXISTS user (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL
);

-- Create the 'skill' table
CREATE TABLE IF NOT EXISTS skill (
  skill_id INT AUTO_INCREMENT PRIMARY KEY,
  skill_name VARCHAR(255) NOT NULL
);

-- Create the 'userskill' table
CREATE TABLE IF NOT EXISTS userskill (
  user_id INT NOT NULL,
  skill_id INT NOT NULL,
  skill_level VARCHAR(255) NOT NULL,
  PRIMARY KEY (user_id, skill_id)
);

-- Create the 'forum_thread' table
CREATE TABLE IF NOT EXISTS forum_thread (
  thread_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  user_id INT NOT NULL
);

-- Create the 'forum_category' table
CREATE TABLE IF NOT EXISTS forum_category (
  forum_category_id INT AUTO_INCREMENT PRIMARY KEY,
  category_name VARCHAR(255) NOT NULL
);

-- Create the 'forum_post' table
CREATE TABLE IF NOT EXISTS forum_post (
  post_id INT AUTO_INCREMENT PRIMARY KEY,
  content TEXT NOT NULL,
  post_date DATETIME NOT NULL,
  user_id INT NOT NULL,
  thread_id INT NOT NULL,
  forum_category_id INT NOT NULL,
  post_type VARCHAR(50),
  parent_post_id INT
);


-- Add foreign keys to 'userskill' table
ALTER TABLE userskill
  ADD CONSTRAINT u FOREIGN KEY (user_id) REFERENCES user(user_id),
  ADD CONSTRAINT v FOREIGN KEY (skill_id) REFERENCES skill(skill_id);

-- Add foreign keys to 'forum_thread' table
ALTER TABLE forum_thread
  ADD FOREIGN KEY (user_id) REFERENCES user(user_id);

-- Add foreign keys to 'forum_post' table
ALTER TABLE forum_post
  ADD CONSTRAINT p FOREIGN KEY (user_id) REFERENCES user(user_id),
  ADD CONSTRAINT q FOREIGN KEY (thread_id) REFERENCES forum_thread(thread_id),
  ADD CONSTRAINT r FOREIGN KEY (forum_category_id) REFERENCES forum_category(forum_category_id);



INSERT INTO user (first_name, last_name, username, password) VALUES
('John', 'Doe', 'john_doe', 'password123'),
('Jane', 'Smith', 'jane_smith', 'pass456'),
('Bob', 'Johnson', 'bob_j', 'securepass');

INSERT INTO skill (skill_name) VALUES
('Programming'),
('Data Analysis'),
('Graphic Design'),
('Project Management');

INSERT INTO userskill (user_id, skill_id, skill_level) VALUES
(1, 1, 'Intermediate'),
(1, 2, 'Advanced'),
(2, 3, 'Beginner'),
(3, 4, 'Expert')
ON DUPLICATE KEY UPDATE skill_level = VALUES(skill_level);

INSERT INTO forum_thread (title, user_id) VALUES
('Introduction', 1),
('Project Discussion', 2),
('General Chat', 3);

INSERT INTO forum_category (category_name) VALUES
('Technology'),
('Art and Design'),
('General Discussion');

INSERT INTO forum_post (content, post_date, user_id, thread_id, forum_category_id, post_type, parent_post_id) VALUES
('Hello, everyone!', '2023-01-01 10:00:00', 1, 1, 3, 'Comment', NULL),
('I have a question about programming.', '2023-01-02 12:30:00', 2, 2, 1, 'Question', NULL),
('Nice to meet you all!', '2023-01-03 15:45:00', 3, 1, 3, 'Comment', NULL),
('Reply to the programming question.', '2023-01-04 09:15:00', 1, 2, 1, 'Answer', 2);






