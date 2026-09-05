import pandas as pd
import json

def analyze_registrations(mock_data):
    df = pd.DataFrame(mock_data)

    total_registered = len(df)
    duplicate_count = len(df[df.duplicated(subset=['email'], keep=False)])
    
    branch_counts = df['branch'].value_counts().to_dict()
    year_counts = df['year'].value_counts().to_dict()
    
    # NEW: Calculate gender ratio
    gender_counts = df['gender'].value_counts(normalize=True).to_dict()
    # Convert decimal (0.5) to percentage (50%)
    gender_percentages = {gender: round(val * 100, 1) for gender, val in gender_counts.items()}

    # NEW: Analyze interests (since interests is a list of words)
    # We explode the lists into individual rows so Pandas can count them
    if 'interests' in df.columns:
        exploded_interests = df.explode('interests')
        top_interests = exploded_interests['interests'].value_counts().head(3).to_dict()
    else:
        top_interests = {}

    return {
        "total": total_registered,
        "duplicate_count": duplicate_count,
        "branches": branch_counts,
        "years": year_counts,
        "gender_ratio_pct": gender_percentages,
        "top_interests": top_interests
    }

# Upgraded mock data
sample_data = [
    {"name": "Alice", "email": "alice@college.edu", "branch": "CS", "year": 2, "gender": "F", "interests": ["AI", "Robotics"]},
    {"name": "Bob", "email": "bob@college.edu", "branch": "IT", "year": 3, "gender": "F", "interests": ["Web Dev", "AI"]},
    {"name": "Charlie", "email": "charlie@college.edu", "branch": "CS", "year": 2, "gender": "M", "interests": ["Robotics", "IoT"]}
]
result=analyze_registrations(sample_data)

print(json.dumps(result, indent=4))
