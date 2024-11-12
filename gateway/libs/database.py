import pickle
import sqlite3
import time
import numpy as np

from libs.facial import validate_user

def connect_db():
    return sqlite3.connect('my_database.db')

def create_session_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS SESSION (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        lock_id TEXT NOT NULL,
        startAt INTEGER NOT NULL,
        endAt INTEGER NOT NULL
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()
    print('created session')

def insert_session(user_id, lock_id, startAt, endAt):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO SESSION (user_id, lock_id, startAt, endAt)
    VALUES (?, ?, ?, ?)
    ''', (user_id, lock_id, startAt, endAt))
    conn.commit()
    cursor.close()
    conn.close()

def fetch_session(user_id, lock_id, currentTime):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    SELECT startAt, endAt FROM SESSION
    WHERE user_id = ? AND lock_id = ? AND startAt <= ? AND endAt >= ?
    ''', (user_id, lock_id, currentTime, currentTime))
    rows = cursor.fetchall()  # Fetch a single row that matches the criteria
    cursor.close()
    conn.close()
    return rows  # Returns None if no match is found, or a tuple with the row data


def create_users_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USER (
        user_id INT PRIMARY KEY,
        embedding BLOB NOT NULL
    )
    ''')
    conn.commit()
    cursor.close()
    conn.close()

def insert_user(user_id, embedding):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Serialize the numpy array
    embedding_blob = pickle.dumps(embedding)
    
    cursor.execute('''
    INSERT OR REPLACE INTO USER (user_id, embedding)
    VALUES (?, ?)
    ''', (user_id, embedding_blob))
    conn.commit()
    cursor.close()
    conn.close()

def search_user_by_embedding(unknown_face):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Fetch all embeddings from the database
    cursor.execute('SELECT user_id, embedding FROM USER')
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Check each embedding against the input_embedding using isMatch
    for user_id, embedding_blob in results:
        # Deserialize the numpy array
        valid_user: np.array = pickle.loads(embedding_blob)
        if validate_user([valid_user], unknown_face):
            return user_id  # Return the matching user_id
    
    return ""  # Return None if no match is found



if __name__ == '__main__':
    insert_session(user_id=1, lock_id=1, startAt=time.time(), endAt=time.time()+3600)