from flask import Flask, request, render_template
from bot_functions.cycle_tracking import handle_cycle_tracking
from bot_functions.sentiment_analysis import analyze_sentiment, get_response
from bot_functions.safety_features import handle_safety_features
from bot_functions.career_finance import handle_career_finance
from user_data import user_data

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def chatbot():
    response = None
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if not message:
            response = 'Please enter a message.'
        else:
            # Check for greetings.
            if message.lower() in ['hi', 'hello', 'hey']:
                response = 'Hello! How can I help you today, girlie?'
            elif message.lower() in ['bye', 'goodbye', 'see you']:
                response = 'Goodbye! Have a great day, girlie!'
            # Safety features.
            elif handle_safety_features(message) is not None:
                response = user_data.get('safety_response')
                print(f"Safety features response: {response}")
            # Career and finance advice.
            elif handle_career_finance(message) is not None:
                response = user_data.get('career_response')
                print(f"Career and finance response: {response}")
            # Cycle tracking branch.
            elif handle_cycle_tracking(message, user_data) is not None:
                cycle_info = user_data.get('cycle_information', {})
                response = (cycle_info.get('prompt') or
                            cycle_info.get('last_period_start_response') or
                            cycle_info.get('cycle_end_response') or
                            cycle_info.get('next_period_response') or
                            "Cycle tracking: no update.")
                print(f"Cycle tracking response: {response}")
            # Default to sentiment analysis.
            else:
                sentiment = analyze_sentiment(message)
                response = get_response(message, sentiment)
                print(f"Sentiment analysis response: {response}")
    print(f"Final response: {response}")
    return render_template('womenbot.html', response=response)

if __name__ == '__main__':
    app.run(debug=True)
