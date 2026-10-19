import random
import json

def generate_participant_data(total_records):
    first_names = ["Rahul", "Priya", "Amit", "Neha", "Vikram", "Sneha", "Rohan", "Anjali", "Karan", "Pooja"]
    last_names = ["Sharma", "Verma", "Patel", "Singh", "Gupta", "Kumar", "Rao", "Desai"]
    branches = ["Computer Science", "Information Technology", "Electrical", "Mechanical", "Data Science"]
    interests_pool = ["AI", "Web Dev", "Robotics", "IoT", "Cybersecurity", "Blockchain"]
    
    participants = []
    
    for i in range(total_records):
        # Pick random traits for the student
        f_name = random.choice(first_names)
        l_name = random.choice(last_names)
        domain = random.choice(branches)
        
        # Randomly assign a gender based on the name (simplified for dummy data)
        gender = "F" if f_name in ["Priya", "Neha", "Sneha", "Anjali", "Pooja"] else "M"
        
        # Pick 2 random interests
        student_interests = random.sample(interests_pool, 2)
        
        # Create the email
        email = f"{f_name.lower()}.{l_name.lower()}{random.randint(1,99)}@college.edu"
        
        student = {
            "name": f"{f_name} {l_name}",
            "email": email,
            "branch": domain,
            "year": random.choice([1, 2, 3, 4]),
            "gender": gender,
            "interests": student_interests
        }
        participants.append(student)

    # Intentionally inject 15 exact duplicates to test your duplicate_count logic
    for _ in range(15):
        random_existing_student = random.choice(participants)
        participants.append(random_existing_student)
        
    return participants

# Generate 285 unique + 15 duplicates = 300 records
synthetic_data = generate_participant_data(285)

# Save it to a JSON file so your analytics engine can read it later
with open("dummy_registrations.json", "w") as file:
    json.dump(synthetic_data, file, indent=4)

print("Successfully generated dummy_registrations.json with", len(synthetic_data), "records!")
