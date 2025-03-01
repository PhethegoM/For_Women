from textblob import TextBlob

def analyze_sentiment(message):
    blob = TextBlob(message)
    return blob.sentiment.polarity

def get_response(message, sentiment):
    message = message.lower()
    if message in ['hello', 'hi', 'hey']:
        return 'Hello! How can I help you today, girlie?'
    elif message in ['bye', 'goodbye', 'see you']:
        return 'Goodbye! Have a great day, girlie!'
    elif sentiment > 0.5:
        return 'That sounds amazing! Tell me more.'
    elif sentiment > 0:
        return 'That sounds positive! How can I assist you?'
    elif sentiment < -0.5:
        return 'I\'m really sorry to hear that. Is there anything I can do to help?'
    elif sentiment < 0:
        return 'That doesn\'t sound great. Let me know if you need support.'
    else:
        return 'I didn\'t quite understand that. Can you rephrase or provide more details?'