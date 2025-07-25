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

async def try_fetch_trends():
    return await client.get_trends('trending')

async def full_login():
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
            # Test login by attempting to fetch trends
            asyncio.run(try_fetch_trends())
        else:
            raise Exception("No cookies found")
    except Exception as e:
        print(f"Cookie login failed, trying full login: {str(e)}")
        asyncio.run(full_login())

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
