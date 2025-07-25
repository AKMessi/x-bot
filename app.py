from flask import Flask, request, jsonify
import asyncio
from twikit import Client

app = Flask(__name__)

# --- Twitter (X) credentials ---
USERNAME = 'youdontknow1028'
EMAIL = 'sensiblegamingyt@gmail.com'
PASSWORD = 'Aaryan@2007'

# --- Initialize twikit client ---
client = Client('en-US')

# --- Safe event loop runner ---
def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        result = loop.run_until_complete(coro)
        return result
    finally:
        loop.close()

# --- Login function ---
async def login():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

# --- Route: GET /trends ---
@app.route('/trends', methods=['GET'])
def get_trends():
    async def fetch_trends():
        await login()
        trends = await client.get_trends('trending')
        # Return each trend as an object for n8n compatibility
        return [{"trend": t.name} for t in trends[:10]]

    try:
        results = run_async(fetch_trends())
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Route: POST /tweet ---
@app.route('/tweet', methods=['POST'])
def post_tweet():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return jsonify({"error": "Missing tweet text"}), 400

    async def send_tweet():
        await login()
        await client.create_tweet(text=text)

    try:
        run_async(send_tweet())
        return jsonify({"success": True, "text": text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Start server locally if needed ---
if __name__ == '__main__':
    app.run(debug=True)
