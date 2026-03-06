import json

class TextCleaner:
    """Parse and clean AI responses into structured JSON"""

    def clean_campaign_response(self, text):
        """Parse campaign response JSON from AI"""
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {}

        # Ensure all required fields exist
        return {
            "campaign_objective": data.get("campaign_objective", "No objective provided"),
            "content_ideas": data.get("content_ideas", []),
            "ad_copy": data.get("ad_copy", []),
            "call_to_action": data.get("call_to_action", "No CTA provided"),
            "hashtags": data.get("hashtags", []),
            "campaign_timeline": data.get("campaign_timeline", "No timeline provided"),
            "expected_metrics": data.get("expected_metrics", "No metrics provided")
        }

    def clean_pitch_response(self, text):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {}

        return {
            "elevator_pitch": data.get("elevator_pitch", "No pitch provided"),
            "value_proposition": data.get("value_proposition", "No value proposition provided"),
            "key_differentiators": data.get("key_differentiators", []),
            "pain_points_solved": data.get("pain_points_solved", "No info"),
            "call_to_action": data.get("call_to_action", "No CTA provided"),
            "email_pitch_template": data.get("email_pitch_template", "No template provided"),
            "linkedin_outreach_message": data.get("linkedin_outreach_message", "No message provided")
        }

    def parse_lead_score(self, text):
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            data = {}

        return {
            "lead_score": data.get("lead_score", 0),
            "lead_category": data.get("lead_category", "Unknown"),
            "conversion_probability": data.get("conversion_probability", "0%"),
            "explanation": data.get("explanation", "No explanation provided"),
            "recommended_actions": data.get("recommended_actions", [])
        }
