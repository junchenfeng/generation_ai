from flask import Flask, request, jsonify
from openai import OpenAI
import os

app = Flask(__name__)

# Initialize OpenAI client with DeepSeek configuration
client = OpenAI(
    base_url="https://api.deepseek.com",
    api_key=os.getenv("DEEPSEEK_API_KEY", "your-api-key-here"),  # Replace with your API key
)

@app.route('/chat', methods=['GET'])
def generate_review():
    try:
        # Get the item parameter from the request
        item = request.args.get('item')
        
        if not item:
            return jsonify({
                'review': 'No item provided',
                'status': 400
            }), 400

        # Construct the prompt
        prompt = f'please make a scathing review for {item}'
        
        # Generate response using DeepSeek
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Extract the review from the response
        review = response.choices[0].message.content
        
        return jsonify({
            'review': review,
            'status': 200
        }), 200
        
    except Exception as e:
        return jsonify({
            'review': str(e),
            'status': 500
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001) 