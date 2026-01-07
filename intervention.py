def suggest_intervention(skill, decay_score):
    """
    Suggests a micro-task if the skill's decay score is too high.
    
    In a real app, these suggestions might come from a database or AI.
    For this demo, we use a simple mapping.
    """
    if decay_score > 60:
        return f"Time for a quick refresh! Practice a 10-minute micro-task for '{skill.skill_name}' to boost your score."
    return None
