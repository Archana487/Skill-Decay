import math

def compute_skill_metrics(data):
    """
    Computes skill decay metrics based on the provided input data.
    
    Input:
        data (dict): {
            "skill_name": str,
            "current_proficiency": float,
            "last_practice_days_ago": float,
            "practice_events_last_30_days": int,
            "real_world_usage_last_30_days": int,
            "avg_task_time_seconds": float,
            "error_rate": float,
            "context_quality": str ("low", "medium", "high")
        }
        
    Output:
        dict: JSON-compliant structure with metrics and forecast.
    """
    
    # 1. Base Parameters
    skill_name = data.get("skill_name", "Unknown")
    P0 = float(data.get("current_proficiency", 0))
    t = float(data.get("last_practice_days_ago", 0))
    practice_30d = data.get("practice_events_last_30_days", 0)
    context_quality = data.get("context_quality", "low").lower()
    error_rate = data.get("error_rate", 0.0)
    
    # 2. explicit Decay Logic
    decay_model = data.get("decay_model", "exponential")
    decay_rate = data.get("decay_rate", 0.1)
    
    # Validation
    if decay_model not in ["linear", "exponential"]:
        decay_model = "exponential"
        
    def calculate_linear_decay(initial, days, rate):
        """
        Linear: Level = max(0, Initial - (Rate * Days))
        """
        # Assume rate is points per day. 
        # If rate is 0.1 means 0.1 points per day? No, usually rate is faster.
        # Let's adhere to the user request: current_level = max(0, initial_level - (decay_rate * days_inactive))
        # Rate probably needs to be higher for linear to make sense, e.g. 1-2 points/day. 
        # But we use the stored parameter.
        val = initial - (rate * days)
        return max(0.0, min(100.0, val))

    def calculate_exponential_decay(initial, days, rate):
        """
        Exponential: Level = Initial * e^(-Rate * Days)
        """
        if initial <= 0: return 0.0
        val = initial * math.exp(-rate * days)
        return max(0.0, min(100.0, val))

    # Calculate Proficiency
    if decay_model == "linear":
        proficiency_score = calculate_linear_decay(P0, t, decay_rate)
    else:
        proficiency_score = calculate_exponential_decay(P0, t, decay_rate)
    
    # Apply penalty for high error rate (Direct impact reduces score further)
    if error_rate > 0.05:
        proficiency_score -= (error_rate * 100) * 0.5
        
    proficiency_score = max(0.0, min(100.0, proficiency_score))
    
    # H (Half-Life) for consistency in other metrics
    # In exponential, Half-Life = ln(2) / decay_rate
    if decay_rate > 0:
        H = math.log(2) / decay_rate
    else:
        H = 999.0 # Practically infinite
    
    # Decay Rate (points per day approx at current t) derived from slope or just 1/H relation?
    # Simple metric: Rate = (P0 - Pt) / t if t > 0, else theoretical loss in 1 day
    decay_rate = proficiency_score * (math.log(2) / H) # Instantaneous decay amount per day
    
    # 4. Context Freshness
    # 0 to 1 score. 
    # High if t is low and context is high.
    context_freshness_score = 1.0 / (1.0 + (t / 10.0)) 
    if context_quality == "high": context_freshness_score *= 1.2
    context_freshness_score = min(1.0, context_freshness_score)

    # 5. Skill Debt
    # Increasing when proficiency < 70.
    # Debt = (70 - proficiency) * duration_factor
    skill_debt = 0.0
    if proficiency_score < 70:
        deficit = 70 - proficiency_score
        # Compound it slightly based on how long it's been decaying (t)
        skill_debt = deficit * (1 + (t / 30.0))
        
    # 6. Failure Probability
    # Derived from proficiency (low prof -> high fail) and error rate.
    # Base fail prob from proficiency:
    # 100 -> 0%, 50 -> 50%, 0 -> 100% linear approx for simplicity, then adjusted.
    fail_prob_base = (100 - proficiency_score) / 100.0
    
    # Adjust with error rate
    fail_prob = fail_prob_base + (error_rate * 2) 
    
    # Adjust with debt momentum
    if skill_debt > 20:
        fail_prob += 0.1
        
    fail_prob = min(1.0, max(0.0, fail_prob))
    
    # 7. Stability Zone
    # Stable: proficiency >= 80 AND failure_probability < 0.25
    # Drift: proficiency 60-79 OR failure_probability 0.25-0.5
    # Critical: proficiency < 60 OR failure_probability > 0.5
    
    if proficiency_score >= 80 and fail_prob < 0.25:
        stability_zone = "stable"
    elif proficiency_score < 60 or fail_prob > 0.5:
        stability_zone = "critical"
    else:
        stability_zone = "drift"
        
    # 8. Maintenance Dose
    # Minutes per week needed to maintain current level.
    # Higher for lower H.
    # Base 30 mins.
    maintenance_dose = 30.0 * (30.0 / H)
    if stability_zone == "critical":
        maintenance_dose *= 2.0 # Need aggressive relearning
        
    # 9. Forecast
    # Days to reach Drift (< 80) or Critical (< 60)
    # Solve P(d) = Target for d
    # Target = P_now * 2^(-d/H)  -> d = -H * log2(Target/P_now)
    
    def days_to_target(target_score):
        if proficiency_score <= target_score: return 0
        return -H * math.log2(target_score / proficiency_score)
        
    days_to_drift = days_to_target(80) if proficiency_score > 80 else 0
    days_to_critical = days_to_target(60) if proficiency_score > 60 else 0
    
    # 10. Explainability
    factors = []
    if t > 14: factors.append("High time since last practice")
    if context_quality == "low": factors.append("Low context quality accelerates decay")
    if practice_30d < 2: factors.append("Infrequent practice schedule")
    if error_rate > 0.1: factors.append("High error rate indicates capability gap")
    
    if not factors: factors.append("Routine maintenance interval")
    
    corrective_action = "Maintain current schedule."
    if stability_zone == "drift":
        corrective_action = "Schedule a 30-minute refresher session this week."
    elif stability_zone == "critical":
        corrective_action = "Immediate deep-dive intervention required to reset capability baseline."

    return {
        "skill_name": skill_name,
        "proficiency_score": round(proficiency_score, 1),
        "decay_rate": round(decay_rate, 2),
        "skill_half_life_days": round(H, 1),
        "skill_debt": round(skill_debt, 1),
        "failure_probability": round(fail_prob, 2),
        "maintenance_dose_minutes_per_week": round(maintenance_dose, 0),
        "context_freshness_score": round(context_freshness_score, 2),
        "stability_zone": stability_zone,
        "forecast": {
            "days_to_drift": round(days_to_drift, 1),
            "days_to_critical": round(days_to_critical, 1)
        },
        "explainability": {
            "primary_factors": factors[:3],
            "corrective_action": corrective_action
        }
    }
