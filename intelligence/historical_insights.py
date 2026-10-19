import pandas as pd
import json

def analyze_historical_events(past_events_data):
    df = pd.DataFrame(past_events_data)
    
    if df.empty:
        return {"message": "No historical data available."}
        
    # Step 1: Group the data by Event Type to find averages
    summary = df.groupby('event_type').agg(
        total_events_hosted=('event_id', 'count'),
        avg_attendance_pct=('attendance_ratio_pct', 'mean'),
        avg_rating=('average_rating', 'mean')
    ).round(1).to_dict(orient='index')
    
    # Step 2: Find the most common operational problem from past events
    all_complaints = df['top_complaint'].dropna().tolist()
    most_common_complaint = max(set(all_complaints), key=all_complaints.count) if all_complaints else "None"
    
    return {
        "baselines_by_type": summary,
        "recurring_operational_issue": most_common_complaint
    }

def get_recommendation_for_new_event(new_event_type, historical_memory):
    # Step 3: Fetch past lessons for a specific event type
    baselines = historical_memory.get("baselines_by_type", {})
    event_type = new_event_type.lower()
    
    if event_type in baselines:
        stats = baselines[event_type]
        expected_attendance = stats["avg_attendance_pct"]
        avg_rating = stats["avg_rating"]
        
        return {
            "event_type": event_type,
            "historical_attendance_rate": expected_attendance,
            "historical_satisfaction": avg_rating,
            "ai_recommendation": f"Historically, {event_type}s get {expected_attendance}% turnout with a {avg_rating}/5 rating. Budget room size accordingly."
        }
    else:
        return {
            "event_type": event_type,
            "message": "No historical data for this event type. Proceed with standard baseline predictions."
        }

# --- Mock Data: The 'Memory' of 4 Past Events ---
mock_past_events = [
    {"event_id": 1, "event_type": "workshop", "attendance_ratio_pct": 80.0, "average_rating": 4.5, "top_complaint": "Room too hot"},
    {"event_id": 2, "event_type": "workshop", "attendance_ratio_pct": 75.0, "average_rating": 4.2, "top_complaint": "Not enough power outlets"},
    {"event_id": 3, "event_type": "seminar", "attendance_ratio_pct": 50.0, "average_rating": 3.8, "top_complaint": "Audio was too quiet"},
    {"event_id": 4, "event_type": "seminar", "attendance_ratio_pct": 55.0, "average_rating": 3.9, "top_complaint": "Room too hot"}
]

# Run the analysis to build the memory
event_memory = analyze_historical_events(mock_past_events)

# Test it: The organizer wants to create a new "Workshop"
new_event_insight = get_recommendation_for_new_event("workshop", event_memory)

print("--- Overall Historical Memory ---")
print(json.dumps(event_memory, indent=4))

print("\n--- Recommendation for New Event ---")
print(json.dumps(new_event_insight, indent=4))
