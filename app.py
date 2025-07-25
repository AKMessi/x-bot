from flask import Flask, request, jsonify
import asyncio
from twikit import Client

app = Flask(__name__)

# Login credentials (change if needed)
USERNAME = 'youdontknow1028'
EMAIL = 'sensiblegamingyt@gmail.com'
PASSWORD = 'Aaryan@2007'

# Initialize Twikit client
client = Client('en-US')

# Login async function
async def login():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

# --- Route: Get Top 10 Trends ---
@app.route('/trends', methods=['GET'])
def get_trends():
    async def fetch():
        await login()
        trends = await client.get_trends('trending')
        return [{"trend": t.name} for t in trends[:10]]  # ✅ Proper JSON structure

    try:
        results = asyncio.run(fetch())
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Route: Post a Tweet ---
@app.route('/tweet', methods=['POST'])
def post_tweet():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing tweet text"}), 400

    async def tweet():
        await login()
        await client.create_tweet(text=text)

    try:
        asyncio.run(tweet())
        return jsonify({"success": True, "tweet": text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Entry Point ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
