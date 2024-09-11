import sqlite3
import uuid
import datetime
import pandas as pd

from flask import jsonify


class Livedb:
    def __init__(self, db_name="livedb.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

        # Create the users table if it doesn't exist
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                email TEXT PRIMARY KEY,
                user_code TEXT,
                num_keys INTEGER DEFAULT 100,
                premium BOOLEAN DEFAULT 0,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        self.conn.commit()

    def insert_user(self, email):
        self.cursor.execute("SELECT user_code FROM users WHERE email=?", (email,))
        existing_user_code = self.cursor.fetchone()

        if existing_user_code:
            return existing_user_code[0], False  # Return the existing user_code

        # Generate a unique user code using a loop to ensure uniqueness
        unique_user_code = None
        while not unique_user_code:
            temp_user_code = uuid.uuid4().hex
            self.cursor.execute(
                "SELECT * FROM users WHERE user_code=?", (temp_user_code,)
            )
            if not self.cursor.fetchone():
                unique_user_code = temp_user_code

        # Insert the new user
        self.cursor.execute(
            "INSERT INTO users (email, user_code) VALUES (?, ?)",
            (email, unique_user_code),
        )
        self.conn.commit()

        return unique_user_code, True

    def user_exist(self, user_code):
        self.cursor.execute(
            "SELECT user_code,num_keys FROM users WHERE user_code=?", (user_code,)
        )
        result = self.cursor.fetchone()

        if not result:
            return True, 0
        else:
            return False, result[1]

    def update_last_used(self, email):
        self.cursor.execute(
            "UPDATE users SET last_used=CURRENT_TIMESTAMP WHERE email=?", (email,)
        )
        self.conn.commit()

    def list_users(self):
        query = (
            "SELECT email, num_keys, premium, last_used FROM users"  # Define the query
        )
        self.cursor.execute(query)  # Execute the query with the cursor
        users = pd.read_sql_query(
            query, self.conn
        )  # Use the query string with read_sql_query
        return users

    def close_connection(self):
        self.conn.close()

    def delete_all_users(self):
        self.cursor.execute("DELETE FROM users")
        self.conn.commit()

    def drop_table(self):
        self.cursor.execute("DROP TABLE users")
        self.conn.commit()
