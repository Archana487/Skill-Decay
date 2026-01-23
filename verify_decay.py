import math
from engine import compute_skill_metrics

def verify_logic_only():
    print("--- Verifying Decay Logic (Unit Test) ---")
    
    # Test 1: Linear Decay
    # Requirement: current_level = max(0, initial_level - (decay_rate * days_inactive))
    # Scenario: Initial=100, Rate=2.0, Days=10 -> Target=80
    inputs_lin = {
        "skill_name": "Linear Test",
        "current_proficiency": 100,
        "last_practice_days_ago": 10,
        "decay_model": "linear",
        "decay_rate": 2.0,
        "context_quality": "medium", # Should be ignored or handle H differently, but decay override takes precedence?
        # Note: In my implementation, H is calculated for other metrics, but proficiency_score comes from the model.
    }
    metrics_lin = compute_skill_metrics(inputs_lin)
    score_lin = metrics_lin['proficiency_score']
    print(f"Linear (100 - 2.0*10): Expected 80.0. Got: {score_lin}")
    
    if abs(score_lin - 80.0) < 0.1:
        print(">> PASS: Linear Decay Check")
    else:
        print(f">> FAIL: Linear Decay Check (Got {score_lin})")

    # Test 2: Exponential Decay
    # Requirement: current_level = initial_level * e^(-decay_rate * days_inactive)
    # Scenario: Initial=100, Rate=0.1, Days=10 -> Target=36.7879
    inputs_exp = {
        "skill_name": "Exp Test",
        "current_proficiency": 100,
        "last_practice_days_ago": 10,
        "decay_model": "exponential",
        "decay_rate": 0.1
    }
    metrics_exp = compute_skill_metrics(inputs_exp)
    score_exp = metrics_exp['proficiency_score']
    expected_exp = 100 * math.exp(-0.1 * 10) # 100 * e^-1
    
    print(f"Exponential (100 * e^-1): Expected {expected_exp:.4f}. Got: {score_exp}")
    
    if abs(score_exp - expected_exp) < 0.1:
        print(">> PASS: Exponential Decay Check")
    else:
        print(f">> FAIL: Exponential Decay Check (Got {score_exp})")

    # Test 3: Limits (Linear < 0)
    inputs_limit = {
        "skill_name": "Limit Test",
        "current_proficiency": 50,
        "last_practice_days_ago": 100,
        "decay_model": "linear",
        "decay_rate": 1.0 # 50 - 100 = -50 -> 0
    }
    score_limit = compute_skill_metrics(inputs_limit)['proficiency_score']
    print(f"Linear Limit (<0): Expected 0.0. Got: {score_limit}")
    
    if score_limit == 0.0:
        print(">> PASS: Limit Check")
    else:
        print(">> FAIL: Limit Check")

if __name__ == "__main__":
    verify_logic_only()
