import json
from analytics_service import IntelligenceService

# Step 1: Load the synthetic data from your local JSON files
with open("dummy_registrations.json", "r") as f:
    registrations = json.load(f)

with open("dummy_attendance.json", "r") as f:
    attendance = json.load(f)

with open("dummy_feedback.json", "r") as f:
    feedback = json.load(f)

print(f"Loaded {len(registrations)} registrations, {len(attendance)} attendance records, and {len(feedback)} feedback forms.\n")

# Step 2: Run the Pre-Event Intelligence Engine
pre_event_results = IntelligenceService.get_pre_event_insights(
    mock_registration_data=registrations,
    room_capacity=200,       
    is_weekend=True,         
    event_type="Workshop",   
    days_open=5,             
    days_left=10             
)

# Step 3: Run the Post-Event Intelligence Engine
post_event_results = IntelligenceService.get_post_event_insights(
    attendance_data=attendance,
    feedback_data=feedback
)

# Step 4: Display the dashboard-ready outputs
print("=== PRE-EVENT INTELLIGENCE (WHAT THE AI READS BEFORE THE EVENT) ===")
print(json.dumps(pre_event_results, indent=4))

print("\n=== POST-EVENT INTELLIGENCE (THE FINAL REPORT) ===")
print(json.dumps(post_event_results, indent=4))
