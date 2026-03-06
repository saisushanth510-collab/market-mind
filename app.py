from flask import Flask, render_template, request, jsonify
import os
from datetime import datetime
from services.groq_client import GroqClient
from services.text_cleaner import TextCleaner
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

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

@app.route('/api/generate_campaign', methods=['POST'])
def generate_campaign():
    """Generate marketing campaign using AI"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['product_name', 'product_description', 'target_audience', 
                          'platform', 'budget', 'campaign_goal']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Generate prompt for AI
        prompt = f"""Generate a comprehensive marketing campaign for the following:

Product Name: {data['product_name']}
Product Description: {data['product_description']}
Target Audience: {data['target_audience']}
Marketing Platform: {data['platform']}
Budget: ${data['budget']}
Campaign Goal: {data['campaign_goal']}

Please provide a structured response with the following sections:
1. Campaign Objective
2. Content Ideas (5 specific ideas)
3. Ad Copy (3 variations)
4. Call to Action
5. Hashtags (relevant to platform)
6. Campaign Timeline (weekly breakdown)
7. Expected Engagement Metrics

Format the response in clear sections with headers."""

        # Get AI response
        ai_response = groq_client.generate(prompt)
        
        # Clean the response
        cleaned_response = text_cleaner.clean_campaign_response(ai_response)
        
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

@app.route('/api/generate_pitch', methods=['POST'])
def generate_pitch():
    """Generate sales pitch using AI"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['product_name', 'customer_persona', 'industry', 
                          'company_size', 'budget_range']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Generate prompt for AI
        prompt = f"""Create a compelling sales pitch for:

Product: {data['product_name']}
Customer Persona: {data['customer_persona']}
Industry: {data['industry']}
Company Size: {data['company_size']}
Budget Range: {data['budget_range']}

Please provide:
1. 30-Second Elevator Pitch
2. Value Proposition
3. Key Differentiators (3 main points)
4. Pain Points Solved
5. Call to Action
6. Email Pitch Template
7. LinkedIn Outreach Message

Make it professional and compelling."""

        # Get AI response
        ai_response = groq_client.generate(prompt)
        
        # Clean the response
        cleaned_response = text_cleaner.clean_pitch_response(ai_response)
        
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

@app.route('/api/score_lead', methods=['POST'])
def score_lead():
    """Score a lead using AI analysis"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['lead_name', 'company', 'budget', 'business_need', 
                          'urgency', 'decision_authority']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Generate prompt for AI
        prompt = f"""Analyze and score this lead:

Lead Name: {data['lead_name']}
Company: {data['company']}
Budget: {data['budget']}
Business Need: {data['business_need']}
Urgency: {data['urgency']}
Decision Authority: {data['decision_authority']}

Provide:
1. Lead Score (0-100)
2. Lead Category (Hot/Warm/Medium/Cold)
3. Conversion Probability Percentage
4. Brief Explanation (2-3 sentences)
5. Recommended Next Actions (3 specific actions)

Be analytical and precise in your scoring."""

        # Get AI response
        ai_response = groq_client.generate(prompt)
        
        # Parse and clean the response
        lead_score_data = text_cleaner.parse_lead_score(ai_response)
        
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

@app.route('/api/get_history/<content_type>')
def get_history(content_type):
    """Get historical generated content"""
    if content_type in generated_content:
        return jsonify(generated_content[content_type])
    return jsonify([])

if __name__ == '__main__':
    app.run(debug=True, port=5000)