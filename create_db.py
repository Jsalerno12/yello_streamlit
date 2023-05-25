import sqlite3

conn = sqlite3.connect('data.db')

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS USERS")
cursor.execute("DROP TABLE IF EXISTS DOCUMENTS")
cursor.execute("DROP TABLE IF EXISTS QUESTIONS")
cursor.execute("DROP TABLE IF EXISTS RESPONSES")

cursor.execute('''
    CREATE TABLE USERS (
      id INTEGER PRIMARY KEY,
      first_name VARCHAR(255),
      last_name VARCHAR(255),
      email VARCHAR(255),
      phone VARCHAR(255),
      user_type VARCHAR(255),
      deleted BOOLEAN,
      created_at TIMESTAMP,
      updated_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE DOCUMENTS (
      id INTEGER PRIMARY KEY,
      user_id INT,
      document_type VARCHAR(255),
      document_name VARCHAR(255),
      deleted BOOLEAN,
      created_at TIMESTAMP,
      updated_at TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES USERS (id)
    )
''')

cursor.execute('''
    CREATE TABLE QUESTIONS (
      id INTEGER PRIMARY KEY,
      name VARCHAR(255),
      deleted BOOLEAN,
      created_at TIMESTAMP,
      updated_at TIMESTAMP
    )
''')

cursor.execute('''
    CREATE TABLE RESPONSES (
      id INTEGER PRIMARY KEY,
      user_id INT,
      question_id INT,
      answer TEXT,
      deleted BOOLEAN,
      created_at TIMESTAMP,
      updated_at TIMESTAMP,
      FOREIGN KEY (user_id) REFERENCES USERS (id),
      FOREIGN KEY (question_id) REFERENCES QUESTIONS (id)
    )
''')

users_insert = '''
INSERT INTO users VALUES
    (1, 'first_1', 'last_1', 'first_last1@gmail.com', '555-555-5555', 'candidate', false, datetime('now'), datetime('now')),
    (2, 'first_2', 'last_2', 'first_last2@gmail.com', '555-555-5555', 'candidate', false, datetime('now'), datetime('now')),
    (3, 'first_3', 'last_3', 'first_last3@gmail.com', '555-555-5555', 'candidate', false, datetime('now'), datetime('now')),
    (4, 'first_4', 'last_4', 'first_last4@gmail.com', '555-555-5555', 'candidate', false, datetime('now'), datetime('now')),
    (5, 'first_5', 'last_5', 'first_last5@gmail.com', '555-555-5555', 'candidate', false, datetime('now'), datetime('now')),
    (6, 'first_6', 'last_6', 'first_last6@example.com', '555-555-5555', 'admin', false, '2023-01-01', datetime('now')),
    (7, 'first_7', 'last_7', 'first_last7@example.com', '555-555-5555', 'admin', false, '2018-12-31', datetime('now')), 
    (8, 'first_8', 'last_8', 'first_last8@example.com', '555-555-5555', 'admin', false, '2019-12-31', datetime('now')), 
    (9, 'first_9', 'last_9', 'first_last9@example.com', '555-555-5555', 'admin', false, '2020-01-01', datetime('now')),
    (10, 'first_10', 'last_10', 'first_last10@example.com', '555-555-5555', 'admin', false, '2021-01-01', datetime('now'));
'''

documents_insert = '''
INSERT INTO documents VALUES
    (1, 1, 'resume', 'first_last1 resume', false, datetime('now'), datetime('now')), 
    (2, 2, 'resume', 'first_last2 resume', false, datetime('now'), datetime('now')), 
    (3, 3, 'resume', 'first_last3 resume', false, datetime('now'), datetime('now')), 
    (4, 4, 'resume', 'first_last4 resume', false, datetime('now'), datetime('now')), 
    (5, 5, 'spreadsheet', 'first_last5 sheet', false, datetime('now'), datetime('now'));
'''

questions_insert = '''
INSERT INTO questions VALUES
    (1, 'What is your favorite color?', false, datetime('now'), datetime('now')),
    (2, 'What is the name of your first pet?', false, datetime('now'), datetime('now')),
    (3, 'Are you allowed to work in the United States?', false, datetime('now'), datetime('now')), 
    (4, 'Tell us a story', false, datetime('now'), datetime('now'));
'''

responses_insert = '''
INSERT INTO responses VALUES
    (1, 1, 1, 'green', false, datetime('now'), datetime('now')),
    (2, 2, 1, 'violet', false, datetime('now'), datetime('now')),
    (3, 3, 1, '0000000000000000000', false, datetime('now'), datetime('now')),
    (4, 1, 2, 'George', false, datetime('now'), datetime('now')),
    (5, 1, 3, 'Yes', false, datetime('now'), datetime('now')),
    (6, 1, 4, '0000000000000000000111111', false, datetime('now'), datetime('now')), 
    (7, 2, 4, '0000000000000000000111111', false, datetime('now'), datetime('now')), 
    (8, 3, 4, '0000000000000000000111111', false, datetime('now'), datetime('now'));
'''


cursor.executescript(users_insert)
cursor.executescript(documents_insert)
cursor.executescript(questions_insert)
cursor.executescript(responses_insert)

conn.commit()
conn.close()

print("SQLite database 'data.db' created successfully.")