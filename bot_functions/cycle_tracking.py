from datetime import datetime, timedelta
from user_data import user_data  # Assuming user_data is a shared dict

def process_next_period(message_lower, user_data):
    if 'next period' in message_lower:
        cycle_info = user_data.get('cycle_information', {})
        if ('cycle_length' in cycle_info and 'last_period_end' in cycle_info):
            cycle_length = cycle_info['cycle_length']
            last_period_end = cycle_info['last_period_end']
            predicted_next = last_period_end + timedelta(days=cycle_length)
            cycle_info['next_period_prediction'] = predicted_next
            cycle_info['next_period_response'] = (
                f"Your next period is predicted around {predicted_next.strftime('%Y-%m-%d')}."
            )
        else:
            user_data.setdefault('cycle_information', {})
            user_data['cycle_information']['next_period_response'] = (
                "I don't have enough information to predict your next period. Please provide both your period start and end dates."
            )
        return True
    return False

def process_generic_cycle(message_lower, user_data, cycle_keywords):
    """
    If the message contains generic cycle tracking keywords (e.g., "track my period")
    and does not include explicit date instructions, check if cycle data exists.
    If yes, display the last recorded period and next prediction; otherwise, prompt for dates.
    """
    # Debug print: Show the message and keywords.
    print("[DEBUG] In process_generic_cycle, message_lower:", message_lower)
    print("[DEBUG] Cycle keywords:", cycle_keywords)
    
    if any(keyword in message_lower for keyword in cycle_keywords):
        user_data.setdefault('cycle_information', {})
        cycle_info = user_data['cycle_information']
        
        # If both start and end dates exist, then build a detailed response.
        if 'last_period_start' in cycle_info and 'last_period_end' in cycle_info:
            start_date = cycle_info['last_period_start']
            end_date = cycle_info['last_period_end']
            period_duration = (end_date - start_date).days
            
            # Use cycle_length if available; if not assume it equals period_duration.
            cycle_length = cycle_info.get('cycle_length', period_duration)
            predicted_next = end_date + timedelta(days=cycle_length)
            current_date = datetime.now()
            if current_date > predicted_next:
                next_status = (f"Your next period was predicted on {predicted_next.strftime('%Y-%m-%d')}, "
                               "it might be overdue.")
            else:
                next_status = f"Your next period is predicted to start on {predicted_next.strftime('%Y-%m-%d')}."
                
            cycle_info['prompt'] = (
                f"Your last period ended on {end_date.strftime('%Y-%m-%d')}. It lasted {period_duration} days. {next_status}"
            )
        else:
            # No cycle data yet – so prompt the user.
            cycle_info['prompt'] = (
                "Welcome to cycle tracking! Please provide your last period's start date using "
                "'cycle start YYYY-MM-DD' and your last period's end date using 'cycle end YYYY-MM-DD'."
            )
        print("[DEBUG] Generic cycle prompt set to:", cycle_info.get('prompt'))
        return True
    return False

def process_cycle_start(message_lower, user_data):
    if 'cycle start' in message_lower:
        date_str = message_lower.replace('cycle start', '').strip()
        try:
            start_date = datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            user_data.setdefault('cycle_information', {})['last_period_start_response'] = (
                "Invalid date format for cycle start. Please use YYYY-MM-DD."
            )
            return True
        
        user_data.setdefault('cycle_information', {})['last_period_start'] = start_date
        user_data['cycle_information']['last_period_start_response'] = (
            f"Your period start date is set to {start_date.strftime('%Y-%m-%d')}."
        )
        return True
    return False

def process_cycle_end(message_lower, user_data):
    if 'cycle end' in message_lower:
        date_str = message_lower.replace('cycle end', '').strip()
        try:
            end_date = datetime.strptime(date_str, '%Y-%m-%d')
        except Exception as e:
            user_data.setdefault('cycle_information', {})['cycle_end_response'] = (
                "Invalid date format for cycle end. Please use YYYY-MM-DD."
            )
            return True
        
        user_data.setdefault('cycle_information', {})['last_period_end'] = end_date
        
        if 'last_period_start' in user_data['cycle_information']:
            start_date = user_data['cycle_information']['last_period_start']
            period_duration = (end_date - start_date).days
            # Here we assume the cycle length equals the period duration.
            user_data['cycle_information']['cycle_length'] = period_duration
            predicted_next = end_date + timedelta(days=period_duration)
            user_data['cycle_information']['cycle_end_response'] = (
                f"Your period ended on {end_date.strftime('%Y-%m-%d')}. It lasted {period_duration} days. "
                f"Your next period is predicted around {predicted_next.strftime('%Y-%m-%d')}."
            )
        else:
            user_data['cycle_information']['cycle_end_response'] = (
                f"Your period end is set to {end_date.strftime('%Y-%m-%d')}. Please provide your period start date."
            )
        return True
    return False

def handle_cycle_tracking(message, user_data):
    """
    Routes the message to the proper cycle tracking function.
    Checks for "next period" requests, then generic cycle tracking keywords,
    and finally specific commands ('cycle start' and 'cycle end').
    """
    try:
        message_lower = message.lower().strip()
        cycle_keywords = [
            'track my cycle', 
            'track my period', 
            'menstruation', 
            'menstrual cycle', 
            'period tracking'
        ]
        
        if process_next_period(message_lower, user_data):
            return True
        if process_generic_cycle(message_lower, user_data, cycle_keywords):
            return True
        if process_cycle_start(message_lower, user_data):
            return True
        if process_cycle_end(message_lower, user_data):
            return True
        return False
    except Exception as e:
        print("Error in handle_cycle_tracking:", e)
        return None
