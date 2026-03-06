from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from groq import Groq

app = Flask(__name__)
CORS(app)

# Groq API key
client = Groq(api_key="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")

@app.route("/")
def home():
    return render_template("index.html")


# Campaign Generator
@app.route("/generate_campaign", methods=["POST"])
def generate_campaign():
    try:
        data = request.json

        product = data.get("product")
        audience = data.get("audience")
        platform = data.get("platform")

        prompt = f"""
Create a marketing campaign.

Product: {product}
Audience: {audience}
Platform: {platform}

Include:
- Headline
- Marketing message
- Call to action
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        campaign = completion.choices[0].message.content

        return jsonify({"campaign": campaign})

    except Exception as e:
        return jsonify({"error": str(e)})


# Sales Pitch
@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    try:
        data = request.json

        product = data.get("product")
        customer = data.get("customer")

        prompt = f"""
Create a persuasive sales pitch.

Product: {product}
Customer: {customer}
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        pitch = completion.choices[0].message.content

        return jsonify({"pitch": pitch})

    except Exception as e:
        return jsonify({"error": str(e)})


# Lead Score
@app.route("/lead_score", methods=["POST"])
def lead_score():
    try:
        data = request.json

        name = data.get("name")
        budget = data.get("budget")
        need = data.get("need")
        urgency = data.get("urgency")

        prompt = f"""
Analyze the following lead.

Name: {name}
Budget: {budget}
Need: {need}
Urgency: {urgency}

Give a lead score out of 10 and explain briefly.
"""

        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )

        score = completion.choices[0].message.content

        return jsonify({"score": score})

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
