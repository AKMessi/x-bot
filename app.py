from flask import Flask, request, jsonify
import asyncio
from twikit import Client
import nest_asyncio
import os

nest_asyncio.apply()
app = Flask(__name__)

USERNAME = 'youdontknow1028'
EMAIL = 'sensiblegamingyt@gmail.com'
PASSWORD = 'Aaryan@2007'

client = Client('en-US')
COOKIES_PATH = 'cookies.json'

async def login_with_credentials():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file=COOKIES_PATH
    )

def ensure_logged_in():
    try:
        if os.path.exists(COOKIES_PATH):
            client.load_cookies(COOKIES_PATH)
        if not client.is_logged_in:
            asyncio.run(login_with_credentials())
    except Exception as e:
        raise Exception(f"Login failed: {str(e)}")

@app.route('/trends', methods=['GET'])
def get_trends():
    try:
        ensure_logged_in()
        trends = asyncio.run(client.get_trends('trending'))
        result = [{"name": t.name} for t in trends[:10]]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/tweet', methods=['POST'])
def post_tweet():
    try:
        data = request.get_json()
        text = data.get("text")
        if not text:
            return jsonify({"error": "Missing tweet text"}), 400

        ensure_logged_in()
        asyncio.run(client.create_tweet(text=text))
        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
