# analytics_service.py

from registration_stats import analyze_registrations
from pre_event_health import calculate_event_health
from post_event_stats import generate_post_event_report
from predictions import predict_final_registrations, predict_advanced_attendance
from historical_insights import analyze_historical_events, get_recommendation_for_new_event

class IntelligenceService:
    @staticmethod
    def get_pre_event_insights(mock_registration_data, room_capacity, is_weekend, event_type, days_open, days_left):
        reg_stats = analyze_registrations(mock_registration_data)
        current_total = reg_stats["total"]
        
        health_stats = calculate_event_health(
            current_registrations=current_total, 
            room_capacity=room_capacity, 
            duplicate_count=reg_stats["duplicate_count"]
        )
        
        volume_prediction = predict_final_registrations(
            current_registrations=current_total,
            days_form_open=days_open,
            days_remaining=days_left,
            capacity=room_capacity
        )

        turnout_prediction = predict_advanced_attendance(
            current_registrations=current_total, 
            is_weekend=is_weekend,
            event_type=event_type
        )
        
        return {
            "registration_data": reg_stats,
            "event_health": health_stats,
            "predictions": {
                "volume": volume_prediction,
                "turnout": turnout_prediction
            }
        }

    @staticmethod
    def get_post_event_insights(attendance_data, feedback_data):
        return generate_post_event_report(attendance_data, feedback_data)

    @staticmethod
    def get_historical_recommendation(past_events_data, new_event_type):
        memory = analyze_historical_events(past_events_data)
        return get_recommendation_for_new_event(new_event_type, memory)
