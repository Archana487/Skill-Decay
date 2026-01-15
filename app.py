from flask import Flask, request, jsonify, render_template
from models import db, Skill, PracticeLog
from intervention import suggest_intervention
from datetime import datetime
import os

app = Flask(__name__)

# Configuring SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'skills.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Initialize database
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    """
    Serve the frontend dashboard.
    """
    from flask import render_template
    return render_template('index.html')

@app.route('/add-skill', methods=['POST'])
def add_skill():
    """
    Endpoint to add a new skill to the tracker.
    Expects: skill_name, confidence_score, actual_score
    """
    data = request.get_json()
    
    if not data or 'skill_name' not in data:
        return jsonify({"error": "Missing skill_name"}), 400
        
    new_skill = Skill(
        skill_name=data['skill_name'],
        confidence_score=data.get('confidence_score', 50),
        actual_score=data.get('actual_score', 50),
        last_used=datetime.utcnow()
    )
    
    db.session.add(new_skill)
    db.session.commit()
    
    return jsonify({"message": "Skill added successfully!", "id": new_skill.id}), 201

from datetime import datetime, timedelta
from engine import compute_skill_metrics

# ... imports ...

@app.route('/skills', methods=['GET'])
def get_skills():
    """
    Endpoint to retrieve all skills using the Skill Decay Intelligence Engine.
    """
    skills = Skill.query.all()
    output = []
    
    for skill in skills:
        # Calculate Input Metrics
        now = datetime.utcnow()
        days_since_practice = (now - skill.last_used).days
        
        # Count practice logs in last 30 days
        practice_count_30d = PracticeLog.query.filter(
            PracticeLog.skill_id == skill.id,
            PracticeLog.date >= (now - timedelta(days=30))
        ).count()
        
        # Construct Engine Input
        engine_input = {
            "skill_name": skill.skill_name,
            "current_proficiency": skill.actual_score,
            "last_practice_days_ago": days_since_practice,
            "practice_events_last_30_days": practice_count_30d,
            "real_world_usage_last_30_days": practice_count_30d, # Approx
            "avg_task_time_seconds": getattr(skill, 'avg_task_time_seconds', 300),
            "error_rate": getattr(skill, 'error_rate', 0.0),
            "context_quality": getattr(skill, 'context_quality', 'low')
        }
        
        # Get Engine Computation
        metrics = compute_skill_metrics(engine_input)
        
        # Calculate Intervention Suggestions (Unified Engine Approach)
        from intervention import suggest_intervention
        
        suggestions = suggest_intervention(skill.skill_name, metrics['stability_zone'], metrics['proficiency_score'])

        # Merge with System ID and Gamification Data
        metrics.update({
            "id": skill.id,
            "date_learned": skill.date_learned.isoformat(),
            "last_used": skill.last_used.isoformat(),
            "xp": skill.xp,
            "level": skill.level,
            "streak": skill.streak,
            # Backward compatibility for frontend
            "decay_score": 100 - metrics['proficiency_score'], # Approx inverse for frontend compatibility if needed
            "forecast_7d": metrics['proficiency_score'], # Temp placeholder
            "interventions": suggestions # New field for specific tasks
        })
        
        output.append(metrics)
        
    return jsonify(output)

@app.route('/intervention', methods=['GET'])
def get_interventions():
    """
    Endpoint to get suggested micro-tasks for skills needing practice.
    """
    skills = Skill.query.all()
    suggestions = []
    
    for skill in skills:
        # Re-compute minimal metrics for intervention check
        # (Ideal world: we extract this calculation to a helper, but duplicating for safety in this refactor)
        days_since_practice = (datetime.utcnow() - skill.last_used).days
        engine_input = {
            "skill_name": skill.skill_name,
            "current_proficiency": skill.actual_score,
            "last_practice_days_ago": days_since_practice
        }
        metrics = compute_skill_metrics(engine_input)
        
        items = suggest_intervention(skill.skill_name, metrics['stability_zone'], metrics['proficiency_score'])
        
        for item in items:
            suggestions.append({
                "skill_name": skill.skill_name,
                "decay_score": 100 - metrics['proficiency_score'],
                "suggestion": item
            })
            
    return jsonify(suggestions)

@app.route('/simulate-decay/<int:skill_id>', methods=['POST'])
def simulate_decay(skill_id):
    """
    Endpoint to simulate time passing for a specific skill.
    """
    from datetime import timedelta
    skill = Skill.query.get_or_404(skill_id)
    skill.last_used = skill.last_used - timedelta(days=30)
    db.session.commit()
    return jsonify({"message": "Simulated decay", "new_last_used": skill.last_used.isoformat()})

@app.route('/practice', methods=['POST'])
def log_practice():
    """
    Endpoint to record a practice session and reset the skill's last_used timer.
    """
    data = request.get_json()
    if not data or 'skill_id' not in data:
        return jsonify({"error": "Missing skill_id"}), 400
    
    skill = Skill.query.get_or_404(data['skill_id'])
    
    # Record the log
    new_log = PracticeLog(
        skill_id=skill.id,
        activity_type=data.get('activity_type', 'General Practice'),
        notes=data.get('notes', ''),
        date=datetime.utcnow()
    )
    
    # Reset last_used for decay calculation
    now = datetime.utcnow()
    
    # Calculate XP Gain
    xp_gain = 25 # Base XP
    if data.get('activity_type') == 'Project Implementation': xp_gain = 50
    elif data.get('activity_type') == 'Mentoring Others': xp_gain = 40
    
    skill.xp += xp_gain
    
    # Level Up Logic (approximate: Level * 100 XP)
    if skill.xp >= (skill.level * 100):
        skill.level += 1
        level_up = True
    else:
        level_up = False
        
    # Streak Logic
    if skill.last_practice_date:
        delta = (now.date() - skill.last_practice_date.date()).days
        if delta == 1:
            skill.streak += 1
        elif delta > 1:
            skill.streak = 1
    else:
        skill.streak = 1
        
    skill.last_practice_date = now
    skill.last_used = now
    
    db.session.add(new_log)
    db.session.commit()
    
    return jsonify({
        "message": "Practice logged successfully", 
        "id": new_log.id,
        "xp_gain": xp_gain,
        "level_up": level_up,
        "new_level": skill.level,
        "new_streak": skill.streak
    }), 201

@app.route('/history', methods=['GET'])
def get_history():
    """
    Endpoint to fetch the global learning history across all skills.
    """
    logs = PracticeLog.query.order_by(PracticeLog.date.desc()).limit(20).all()
    output = []
    for log in logs:
        output.append({
            "id": log.id,
            "skill_name": log.skill.skill_name,
            "date": log.date.isoformat(),
            "activity_type": log.activity_type,
            "notes": log.notes
        })
    return jsonify(output)

if __name__ == '__main__':
    # Running in debug mode as requested
    app.run(debug=True)
