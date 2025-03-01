from user_data import user_data

def handle_career_finance(message):
    message = message.lower()
    if message == 'career advice':
        user_data['career_response'] = (
            "Here are some career tips:\n"
            "1. Set clear career goals.\n"
            "2. Network with professionals in your field.\n"
            "3. Continuously upgrade your skills.\n"
            "4. Seek mentorship and guidance."
        )
        return True
    elif message == 'finance tips':
        user_data['career_response'] = (
            "Here are some finance tips:\n"
            "1. Create a monthly budget.\n"
            "2. Save at least 20% of your income.\n"
            "3. Invest in low-risk options like mutual funds.\n"
            "4. Avoid unnecessary debt."
        )
        return True
    else:
        return None