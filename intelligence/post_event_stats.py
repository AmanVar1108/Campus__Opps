import pandas as pd
from textblob import TextBlob
import json

def generate_post_event_report(attendance_data, feedback_data):
    # --- Part 1: Attendance Metrics ---
    att_df = pd.DataFrame(attendance_data)
    total_registered = len(att_df)
    attended = len(att_df[att_df['status'] == 'Checked In'])
    attendance_ratio = (attended / total_registered) * 100 if total_registered > 0 else 0

    # --- Part 2: Feedback & NLP Text Analysis ---
    fb_df = pd.DataFrame(feedback_data)
    average_rating = fb_df['rating'].mean() if not fb_df.empty else 0

    highlights = []
    complaints = []
    themes_detected = []

    # Loop through every single feedback comment
    for index, row in fb_df.iterrows():
        comment = str(row.get('comment', ''))
        if not comment:
            continue
            
        # Use TextBlob to score the emotion of the sentence (-1.0 to 1.0)
        blob = TextBlob(comment)
        polarity = blob.sentiment.polarity
        
        # Categorize the comment based on the rating and the text polarity
        if row['rating'] >= 4 or polarity > 0.2:
            highlights.append(comment)
        elif row['rating'] <= 2 or polarity < -0.1:
            complaints.append(comment)

        # Basic theme extraction: check for specific keywords
        text_dump = comment.lower()
        if "hot" in text_dump or "ac" in text_dump or "room" in text_dump:
            themes_detected.append("Facility/Room Issue")
        if "speaker" in text_dump or "content" in text_dump or "learned" in text_dump:
            themes_detected.append("Content/Speaker Quality")

    # Clean up themes to remove duplicates
    unique_themes = list(set(themes_detected))

    # --- Part 3: Overall Success Math ---
    # NEW: Wrap the Pandas math in float() to convert them to standard Python numbers
    average_rating = float(fb_df['rating'].mean()) if not fb_df.empty else 0.0
    rating_score = (average_rating / 5.0) * 100 
    success_score = float((attendance_ratio * 0.6) + (rating_score * 0.4))

    return {
        "metrics": {
            "total_attended": int(attended),
            "attendance_ratio_pct": round(attendance_ratio, 1),
            "average_rating": round(average_rating, 2),
            "overall_success_score": round(success_score, 1)
        },
        "feedback_intelligence": {
            "positive_highlights": highlights,
            "complaints": complaints,
            "detected_themes": unique_themes,
            "total_reviews_analyzed": len(fb_df)
        }
    }

mock_attendance = [
    {"participant": "Alice", "status": "Checked In"},
    {"participant": "Bob", "status": "No Show"},
    {"participant": "Charlie", "status": "Checked In"}
]

mock_feedback = [
    {"participant": "Alice", "rating": 5, "comment": "The content was amazing, I learned a lot!"},
    {"participant": "Charlie", "rating": 2, "comment": "Room was too hot and the AC was broken."}
]

final_report = generate_post_event_report(mock_attendance, mock_feedback)

# NEW: Print using json.dumps with a 4-space indent
print(json.dumps(final_report, indent=4))
