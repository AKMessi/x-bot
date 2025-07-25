from flask import Flask, request, jsonify
import asyncio
import nest_asyncio
from twikit import Client

# Fix event loop issue in hosted environments
nest_asyncio.apply()

app = Flask(__name__)

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
    async def fetch():
        await login()
        trends = await client.get_trends('trending')
        return [t.name for t in trends[:10]]
    
    try:
        results = asyncio.run(fetch())
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        return jsonify({"success": True, "text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
