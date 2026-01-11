def suggest_intervention(skill, decay_score):
    """
    Suggests tiered micro-tasks if the skill's decay score is too high.
    Returns a list of suggestion objects.
    """
    if decay_score < 20:
        return []
        
    suggestions = [
        {
            "tier": "Micro-Task",
            "task": f"Review top 5 key concepts of {skill.skill_name}.",
            "time": "5m",
            "xp": 10
        },
        {
            "tier": "Maintenance",
            "task": f"Complete one small practice exercise in {skill.skill_name}.",
            "time": "15m",
            "xp": 30
        }
    ]
    
    if decay_score > 60:
        suggestions.append({
            "tier": "Deep Dive",
            "task": f"Build a small mini-project specifically focusing on weak areas of {skill.skill_name}.",
            "time": "1h+",
            "xp": 100
        })
        
    return suggestions
