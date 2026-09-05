import json
import random

# Load the registrations you already created
with open("dummy_registrations.json", "r") as f:
    registrations = json.load(f)

attendance = []
feedback = []

for student in registrations:
    # Simulate Attendance (roughly 70% show up)
    did_attend = random.random() < 0.70
    attendance.append({
        "participant": student["name"],
        "status": "Checked In" if did_attend else "No Show"
    })

    # Simulate Feedback (only for those who attended)
    if did_attend:
        if random.random() < 0.15: # Inject negative themes for your NLP to catch
            rating = random.choice([1, 2])
            comment = random.choice(["Room was too hot.", "The AC was broken.", "Audio was quiet."])
        else:
            rating = random.choice([4, 5])
            comment = random.choice(["Great speaker!", "I learned a lot.", "Amazing content."])
            
        feedback.append({
            "participant": student["name"],
            "rating": rating,
            "comment": comment
        })

# Save the new files
with open("dummy_attendance.json", "w") as f:
    json.dump(attendance, f, indent=4)

with open("dummy_feedback.json", "w") as f:
    json.dump(feedback, f, indent=4)

print(f"Successfully generated {len(attendance)} attendance records and {len(feedback)} feedback forms!")
