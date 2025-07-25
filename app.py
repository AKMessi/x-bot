from flask import Flask, request, jsonify
import asyncio
import nest_asyncio
from twikit import Client

# Patch existing event loop to allow nested use
nest_asyncio.apply()

app = Flask(__name__)

# Twitter (X) credentials
USERNAME = 'youdontknow1028'
EMAIL = 'sensiblegamingyt@gmail.com'
PASSWORD = 'Aaryan@2007'

client = Client('en-US')

async def login():
    await client.login(
        auth_info_1=USERNAME,
        auth_info_2=EMAIL,
        password=PASSWORD,
        cookies_file='cookies.json'
    )

@app.route('/trends', methods=['GET'])
def get_trends():
    async def fetch_trends():
        await login()
        trends = await client.get_trends('trending')
        return [{"trend": t.name} for t in trends[:10]]

    try:
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(fetch_trends())
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        loop = asyncio.get_event_loop()
        loop.run_until_complete(send_tweet())
        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
