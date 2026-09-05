
import json
def calculate_event_health(current_registrations, room_capacity, duplicate_count):
    # Step 1: Start with a perfect score of 100
    health_score = 100
    status = "HEALTHY"

    # Step 2: Check if registrations exceed room capacity
    if current_registrations > room_capacity:
        over_capacity = current_registrations - room_capacity
        # Deduct 10 points for every person over capacity
        health_score -= (over_capacity * 1) 
        
    # Step 3: Deduct points for sloppy data (duplicates)
    if duplicate_count > 0:
        health_score -= (duplicate_count * .5)

    # Step 4: Ensure the score doesn't drop below 0
    if health_score < 0:
        health_score = 0

    # Step 5: Determine the text status
    if health_score < 50:
        status = "CRITICAL"
    elif health_score < 80 :
        status = "WARNING"
    elif health_score >=80 and health_score<90:
        status="Good" 

    # Step 6: Return the final assessment
    return {
        "score": health_score,
        "status": status
    }

# Let's test it: 110 people registered for a 100-person room, with 2 duplicate signups.
test_result = calculate_event_health(current_registrations=110, room_capacity=100, duplicate_count=2)
print("Event Health:", json.dumps(test_result, indent=4))
