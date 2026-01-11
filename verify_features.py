from app import app, db, Skill, PracticeLog
from datetime import datetime, timedelta

def verify_features():
    client = app.test_client()
    
    with app.app_context():
        # Clear DB
        db.session.remove()
        db.drop_all()
        db.create_all()
        
        # 1. Add Skill
        print("Testing Add Skill...")
        resp = client.post('/add-skill', json={
            'skill_name': 'Test Skill',
            'confidence_score': 80,
            'actual_score': 80
        })
        assert resp.status_code == 201
        skill_id = resp.json['id']
        
        # 2. Check Initial Global State
        print("Testing Initial State...")
        resp = client.get('/skills')
        data = resp.json[0]
        assert data['xp'] == 0
        assert data['level'] == 1
        assert data['streak'] == 0 # Should start at 0 or 1 depending on logic, let's see. 
        # In my logic, streak is updated on practice, so 0 initially is correct.
        
        # 3. Test Forecast Logic
        print("Testing Forecast...")
        # forecast_7d should be > decay_score
        assert 'forecast_7d' in data
        assert data['forecast_7d'] >= data['decay_score']
        
        # 4. Test Practice & XP Gain
        print("Testing Practice & XP...")
        resp = client.post('/practice', json={
            'skill_id': skill_id,
            'activity_type': 'Project Implementation', # +50 XP
            'notes': 'Test'
        })
        assert resp.status_code == 201
        assert resp.json['xp_gain'] == 50
        assert resp.json['new_level'] == 1 # 50 < 100
        assert resp.json['new_streak'] == 1
        
        # 5. Test Streak Increment (Mocking time/logic would be hard in integration test without mocking datetime)
        # For now, just test that another practice on same day keeps streak at 1? 
        # Actually my logic: if delta == 1: streak+=1. if delta==0: no change to streak usually, or maybe it sets it?
        # My code:
        # if skill.last_practice_date:
        #    delta = ...
        #    if delta == 1: streak+=1
        #    elif delta > 1: streak=1
        # else: streak=1
        # So same day practice won't increment streak, which is correct.
        
        print("Testing Level Up...")
        # Need 50 more XP to level up (Threshold 100 for Lvl 1->2)
        resp = client.post('/practice', json={
            'skill_id': skill_id,
            'activity_type': 'Project Implementation', # +50 XP
            'notes': 'Test 2'
        })
        assert resp.json['xp_gain'] == 50
        assert resp.json['level_up'] == True
        assert resp.json['new_level'] == 2
        
        print("ALL TESTS PASSED!")

if __name__ == '__main__':
    verify_features()
