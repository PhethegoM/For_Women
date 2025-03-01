from user_data import user_data

def handle_safety_features(message):
    message = message.lower()
    if message == 'safety tips':
        user_data['safety_response'] = (
            "Here are some safety tips:\n"
            "1. Always share your location with a trusted friend.\n"
            "2. Avoid walking alone at night.\n"
            "3. Keep emergency contacts saved on your phone.\n"
            "4. Trust your instincts and avoid risky situations."
        )
        return True
    elif message == 'emergency contacts':
        user_data['safety_response'] = (
            "Here are some emergency contacts:\n"
            "1. Local Police: 911\n"
            "2. Trusted Friend: [Name] - [Phone]\n"
            "3. Family Member: [Name] - [Phone]"
        )
        return True
    else:
        return None