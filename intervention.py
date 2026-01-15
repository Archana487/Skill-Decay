def suggest_intervention(skill_name, stability_zone, proficiency_score):
    """
    Suggests tiered micro-tasks based on the skill's stability zone and proficiency.
    Returns a list of suggestion objects.
    """
    if stability_zone == 'stable':
        return []
        
    suggestions = []

    # Drift Zone Interventions (Proficiency < 80)
    if stability_zone == 'drift':
        suggestions.append({
            "tier": "Micro-Task",
            "task": f"Review top 3 key equations/concepts of {skill_name}.",
            "time": "5m",
            "xp": 10
        })
        suggestions.append({
            "tier": "Maintenance",
            "task": f"Complete a quick 10-minute refresh quiz on {skill_name}.",
            "time": "15m",
            "xp": 30
        })

    # Critical Zone Interventions (Proficiency < 60)
    if stability_zone == 'critical':
        suggestions.append({
            "tier": "Rescue Operation",
            "task": f"Re-read the core documentation or tutorial for {skill_name}.",
            "time": "30m",
            "xp": 50
        })
        suggestions.append({
            "tier": "Deep Dive",
            "task": f"Build a small mini-project specifically focusing on weak areas of {skill_name}.",
            "time": "1h+",
            "xp": 100
        })
        
    return suggestions

