import sqlite3

class Tasks():
    # Connect to the database for the tasks
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist yet
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        completed INTEGER DEFAULT 0,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                        due_date TEXT
                   )
                   ''')
    conn.commit()
    conn.close()
    
    print("Database up and running")
    