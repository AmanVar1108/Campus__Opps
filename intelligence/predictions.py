import json

def predict_final_registrations(current_registrations, days_form_open, days_remaining, capacity):
    # Prevent division by zero if the form just opened today
    if days_form_open == 0:
        days_form_open = 1
        
    # Calculate velocity (how many people register per day)
    daily_velocity = current_registrations / days_form_open
    
    # Predict the final count
    predicted_additional = daily_velocity * days_remaining
    final_prediction = int(current_registrations + predicted_additional)
    
    # Cap the prediction if it exceeds the hard capacity limit
    is_sellout_risk = False
    if final_prediction >= capacity:
        final_prediction = capacity
        is_sellout_risk = True

    return {
        "daily_registration_velocity": round(daily_velocity, 1),
        "predicted_final_registrations": final_prediction,
        "sellout_risk_detected": is_sellout_risk
    }


def predict_advanced_attendance(current_registrations, is_weekend, event_type):
    # Base drop-off rates for college events
    base_rate = 0.65 if is_weekend else 0.75
    
    # Dynamic Modifiers based on event type
    modifiers = {
        "workshop": 0.10,  # High commitment, higher turnout
        "seminar": -0.05,  # Passive listening, lower turnout
        "hackathon": 0.15, # Very high commitment
        "social": 0.00
    }
    
    # Apply the modifier if the event type is known
    event_type = event_type.lower()
    if event_type in modifiers:
        base_rate += modifiers[event_type]
        
    # Cap the rate at a maximum of 95% (always expect some no-shows)
    base_rate = min(base_rate, 0.95)
    
    expected_attendees = int(current_registrations * base_rate)

    return {
        "event_type_analyzed": event_type,
        "adjusted_turnout_rate_pct": round(base_rate * 100, 1),
        "predicted_attendees": expected_attendees
    }

# --- Mock Data and Testing ---

# Scenario: 50 people registered in the first 2 days. There are 5 days left. Room holds 200.
reg_prediction = predict_final_registrations(
    current_registrations=50, 
    days_form_open=2, 
    days_remaining=5, 
    capacity=200
)

# Scenario: Predicting turnout for a "Workshop" on a Weekend with 150 expected final registrations.
attendance_prediction = predict_advanced_attendance(
    current_registrations=150, 
    is_weekend=True, 
    event_type="Workshop"
)

print("--- Registration Prediction ---")
print(json.dumps(reg_prediction, indent=4))
print("\n--- Attendance Prediction ---")
print(json.dumps(attendance_prediction, indent=4))
