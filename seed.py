from app import app, db, Skill, PracticeLog
from datetime import datetime, timedelta
import random

def seed_data():
    with app.app_context():
        # db.drop_all() # Optional: Don't drop, just add if empty, or clear to ensure clean state? 
        # Better to just add if empty.
        
        if Skill.query.count() > 0:
            print("Database already has data. Skipping seed.")
            return

        print("Seeding database...")
        
        skills_data = [
            ("Python Programming", 90, 85, 2, 5),    # Good
            ("System Design", 75, 70, 30, 0),       # Warning
            ("Machine Learning", 60, 50, 60, 0),    # Critical
            ("React.js", 85, 80, 5, 3),             # Good
            ("Kubernetes", 40, 30, 45, 0)           # Warning
        ]

        for name, conf, act, days_ago, streak in skills_data:
            last_used = datetime.utcnow() - timedelta(days=days_ago)
            skill = Skill(
                skill_name=name,
                confidence_score=conf,
                actual_score=act,
                last_used=last_used,
                date_learned=datetime.utcnow() - timedelta(days=100),
                xp=random.randint(50, 500),
                level=random.randint(1, 5),
                streak=streak,
                last_practice_date=last_used
            )
            db.session.add(skill)
            
            # Add some logs
            if streak > 0:
                log = PracticeLog(
                    skill_id=skill.id, # This won't work before commit? 
                    # Actually valid object reference usually works in session, but let's commit first or add to relationships.
                    activity_type="Practice",
                    notes="Seeded session",
                    date=last_used
                )
                skill.logs.append(log)

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
