import sqlite3
import os
from flask import Flask

# Define the path to the database
DATABASE_FOLDER = 'database'
DATABASE_PATH = os.path.join(DATABASE_FOLDER, 'quickdocs.db')

# Create a minimal Flask app 
app = Flask(__name__)

def init_db():
    
    if not os.path.exists(DATABASE_FOLDER):
        os.makedirs(DATABASE_FOLDER)
        print(f"Created directory: {DATABASE_FOLDER}")
    
    
    if os.path.exists(DATABASE_PATH):
        print(f"Database file '{DATABASE_PATH}' already exists. Skipping initialization.")
        return

    with app.app_context():
        conn = sqlite3.connect(DATABASE_PATH)
        print(f"Database file '{DATABASE_PATH}' created.")
        
        
        with app.open_resource('schema.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
            print("Executed schema.sql")
        
        
        with app.open_resource('sample_data.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
            print("Executed sample_data.sql")
            
        conn.commit()
        conn.close()
        print("Database initialization complete.")

if __name__ == '__main__':
    init_db()
