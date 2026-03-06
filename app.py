from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from services.groq_client import GroqClient
from services.text_cleaner import TextCleaner
import json
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Initialize services
groq_client = GroqClient()
text_cleaner = TextCleaner()

# In-memory storage for demo (use database in production)
generated_content = {
    'campaigns': [],
    'pitches': [],
    'leads': []
}

@app.route('/')
def dashboard():
    """Render main dashboard"""
    return render_template('dashboard.html', 
                         campaigns_count=len(generated_content['campaigns']),
                         pitches_count=len(generated_content['pitches']),
                         leads_count=len(generated_content['leads']))

@app.route('/campaign')
def campaign():
    """Render campaign generator page"""
    return render_template('campaign.html')

@app.route('/pitch')
def pitch():
    """Render sales pitch generator page"""
    return render_template('pitch.html')

@app.route('/lead')
def lead():
    """Render lead scoring page"""
    return render_template('lead.html')

# -# ------------------- Campaign Route -------------------
@app.route('/api/generate_campaign', methods=['POST'])
def generate_campaign():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['product_name', 'product_description', 'target_audience', 
                          'platform', 'budget', 'campaign_goal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # ----- MOCK AI RESPONSE FOR TESTING -----
        ai_response = """
        {
          "campaign_objective": "Increase brand awareness",
          "content_ideas": ["Social media challenge","Influencer reels","Daily tips","Product showcase","Giveaways"],
          "ad_copy": ["Stay hydrated with EcoSmart","Smart bottle for healthy living","Drink smarter, live healthier"],
          "call_to_action": "Shop Now",
          "hashtags": ["#StayHydrated","#SmartBottle","#HealthyLifestyle"],
          "campaign_timeline": "Week1: Awareness, Week2: Influencers, Week3: Challenge, Week4: Promotion",
          "expected_metrics": "Reach: 50k, Engagement: 7%"
        }
        """
        
        # Parse and clean the AI response
        cleaned_response = text_cleaner.clean_campaign_response(ai_response)

        # ---- DEBUG PRINT ----
        print("Cleaned campaign response:", cleaned_response)
        
        # Store generated campaign
        campaign_data = {
            'id': len(generated_content['campaigns']) + 1,
            'timestamp': datetime.now().isoformat(),
            'input': data,
            'output': cleaned_response
        }
        generated_content['campaigns'].append(campaign_data)
        
        return jsonify({'success': True, 'campaign': cleaned_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- Pitch Route -------------------
@app.route('/api/generate_pitch', methods=['POST'])
def generate_pitch():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['product_name', 'customer_persona', 'industry', 
                          'company_size', 'budget_range']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # ----- MOCK AI RESPONSE FOR TESTING -----
        ai_response = """
        {
          "elevator_pitch": "Our EcoSmart bottle keeps you hydrated smarter!",
          "value_proposition": "Eco-friendly, smart hydration tracking, convenient design",
          "key_differentiators": ["Smart sensor","Sleek design","Eco-friendly materials"],
          "pain_points_solved": "Forgets to drink, uses disposable bottles, lacks smart tracking",
          "call_to_action": "Buy Now",
          "email_pitch_template": "Introducing EcoSmart Bottle...",
          "linkedin_outreach_message": "Hey [Name], check out our EcoSmart bottle..."
        }
        """
        cleaned_response = text_cleaner.clean_pitch_response(ai_response)

        # ---- DEBUG PRINT ----
        print("Cleaned pitch response:", cleaned_response)
        
        # Store generated pitch
        pitch_data = {
            'id': len(generated_content['pitches']) + 1,
            'timestamp': datetime.now().isoformat(),
            'input': data,
            'output': cleaned_response
        }
        generated_content['pitches'].append(pitch_data)
        
        return jsonify({'success': True, 'pitch': cleaned_response})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- Lead Scoring Route -------------------
@app.route('/api/score_lead', methods=['POST'])
def score_lead():
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['lead_name', 'company', 'budget', 'business_need', 
                          'urgency', 'decision_authority']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400

        # ----- MOCK AI RESPONSE FOR TESTING -----
        ai_response = """
        {
          "lead_score": 85,
          "lead_category": "Hot",
          "conversion_probability": "75%",
          "explanation": "Lead has high budget, urgent need, and decision authority",
          "recommended_actions": ["Schedule call","Send demo","Follow up next week"]
        }
        """
        lead_score_data = text_cleaner.parse_lead_score(ai_response)

        # ---- DEBUG PRINT ----
        print("Cleaned lead score response:", lead_score_data)
        
        # Store scored lead
        lead_data = {
            'id': len(generated_content['leads']) + 1,
            'timestamp': datetime.now().isoformat(),
            'input': data,
            'output': lead_score_data
        }
        generated_content['leads'].append(lead_data)
        
        return jsonify({'success': True, 'lead_score': lead_score_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ------------------- History Route -------------------
@app.route('/api/get_history/<content_type>')
def get_history(content_type):
    if content_type in generated_content:
        return jsonify(generated_content[content_type])
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
