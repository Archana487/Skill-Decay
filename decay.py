from datetime import datetime

def calculate_decay(skill):
    """
    Calculates the decay score of a skill based on the time since it was last used
     and the user's actual performance score.
    
    Formula:
    - Decay increases by 2 points for every day since last_used.
    - Decay is reduced by 0.5 points for every unit of actual_score.
    - Clamped between 0 and 100.
    """
    days_since_used = (datetime.utcnow() - skill.last_used).days
    
    # Base decay from time
    decay_score = days_since_used * 2
    
    # Mitigation from actual skill level
    mitigation = skill.actual_score * 0.5
    
    final_score = decay_score - mitigation
    
    # Ensure the score stays within 0-100
    return max(0, min(100, final_score))

def forecast_decay(skill, days_ahead):
    """
    Predicts what the decay score will be in X days.
    """
    days_since_used = (datetime.utcnow() - skill.last_used).days + days_ahead
    
    # Base decay from time
    decay_score = days_since_used * 2
    
    # Mitigation from actual skill level
    mitigation = skill.actual_score * 0.5
    
    final_score = decay_score - mitigation
    
    return max(0, min(100, final_score))
