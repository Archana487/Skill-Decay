from app import app, db
from sqlalchemy import inspect

def check_schema():
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [c['name'] for c in inspector.get_columns('skill')]
        print("Columns in 'skill' table:", columns)
        
        required = ['xp', 'level', 'streak', 'last_practice_date']
        missing = [c for c in required if c not in columns]
        
        if missing:
            print("MISSING COLUMNS:", missing)
            exit(1)
        else:
            print("Schema looks correct.")

if __name__ == '__main__':
    check_schema()
