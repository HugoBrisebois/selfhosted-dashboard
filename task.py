import sqlite3
from typing import Optional


class Tasks:
     DB_PATH = 'tasks.db'

     @classmethod
     def _ensure_table(cls) -> None:
          with sqlite3.connect(cls.DB_PATH) as conn:
               cursor = conn.cursor()
               cursor.execute(
                    '''
                    CREATE TABLE IF NOT EXISTS tasks (
                         id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT NOT NULL,
                         completed INTEGER DEFAULT 0,
                         created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                         due_date TEXT
                    )
                    '''
               )
               conn.commit()

     @classmethod
     def add_task(cls, title: str, due_date: Optional[str] = None) -> int:
          """Insert a new task and return its id.

          Raises ValueError if `title` is empty.
          """
          if not isinstance(title, str) or not title.strip():
               raise ValueError('title must be a non-empty string')

          cls._ensure_table()
          with sqlite3.connect(cls.DB_PATH) as conn:
               cursor = conn.cursor()
               cursor.execute(
                    'INSERT INTO tasks (title, due_date) VALUES (?, ?)',
                    (title.strip(), due_date),
               )
               conn.commit()
               return cursor.lastrowid


if __name__ == '__main__':
     Tasks._ensure_table()
     print('Database up and running')
    
    
    