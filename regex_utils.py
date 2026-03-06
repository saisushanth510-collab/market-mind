import re
from utils.regex_utils import RegexUtils

class TextCleaner:
    def __init__(self):
        self.regex_utils = RegexUtils()
    
    def clean_campaign_response(self, text):
        """Clean and structure campaign AI response"""
        # Remove markdown formatting
        text = self.regex_utils.remove_markdown(text)
        
        # Structure the response into sections
        sections = {
            'objective': self._extract_section(text, 'Campaign Objective'),
            'content_ideas': self._extract_list_section(text, 'Content Ideas'),
            'ad_copy': self._extract_list_section(text, 'Ad Copy'),
            'call_to_action': self._extract_section(text, 'Call to Action'),
            'hashtags': self._extract_hashtags(text),
            'timeline': self._extract_section(text, 'Campaign Timeline'),
            'metrics': self._extract_section(text, 'Expected Engagement Metrics')
        }
        
        return sections
    
    def clean_pitch_response(self, text):
        """Clean and structure pitch AI response"""
        # Remove markdown formatting
        text = self.regex_utils.remove_markdown(text)
        
        # Structure the response into sections
        sections = {
            'elevator_pitch': self._extract_section(text, '30-Second Elevator Pitch'),
            'value_proposition': self._extract_section(text, 'Value Proposition'),
            'differentiators': self._extract_list_section(text, 'Key Differentiators'),
            'pain_points': self._extract_section(text, 'Pain Points Solved'),
            'call_to_action': self._extract_section(text, 'Call to Action'),
            'email_template': self._extract_section(text, 'Email Pitch Template'),
            'linkedin_message': self._extract_section(text, 'LinkedIn Outreach Message')
        }
        
        return sections
    
    def parse_lead_score(self, text):
        """Parse lead scoring AI response"""
        # Remove markdown formatting
        text = self.regex_utils.remove_markdown(text)
        
        # Extract lead score number
        score_match = re.search(r'Lead Score[:\s]+(\d+)', text, re.IGNORECASE)
        score = int(score_match.group(1)) if score_match else 75
        
        # Determine category based on score
        if score >= 90:
            category = 'Hot Lead'
            category_color = '#ff4444'
        elif score >= 75:
            category = 'Warm Lead'
            category_color = '#ff9944'
        elif score >= 60:
            category = 'Medium Lead'
            category_color = '#ffdd44'
        else:
            category = 'Cold Lead'
            category_color = '#4488ff'
        
        # Extract conversion probability
        prob_match = re.search(r'Conversion Probability[:\s]+(\d+)%?', text, re.IGNORECASE)
        probability = int(prob_match.group(1)) if prob_match else score - 10
        
        # Extract explanation
        explanation = self._extract_section(text, 'Explanation')
        if not explanation:
            explanation = f"This lead shows {category.lower()} potential based on the provided criteria."
        
        # Extract next actions
        actions = self._extract_list_section(text, 'Recommended Next Actions')
        if not actions:
            actions = [
                "Follow up within 24 hours",
                "Schedule a discovery call",
                "Send personalized demo"
            ]
        
        return {
            'score': score,
            'category': category,
            'category_color': category_color,
            'probability': probability,
            'explanation': explanation,
            'next_actions': actions
        }
    
    def _extract_section(self, text, section_name):
        """Extract a specific section from text"""
        pattern = rf'{section_name}[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        
        if match:
            content = match.group(1).strip()
            # Clean up the content
            content = re.sub(r'\s+', ' ', content)
            return content
        return ""
    
    def _extract_list_section(self, text, section_name):
        """Extract a list section from text"""
        pattern = rf'{section_name}[:\s]*((?:[•\-*\d\.]+[^\n]+\n?)+)'
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        
        if match:
            content = match.group(1)
            # Extract individual items
            items = re.findall(r'[•\-*\d\.]+\s*([^\n]+)', content)
            return [item.strip() for item in items if item.strip()]
        return []
    
    def _extract_hashtags(self, text):
        """Extract hashtags from text"""
        hashtags = re.findall(r'#\w+', text)
        if not hashtags:
            # Look for a hashtags section
            pattern = r'Hashtags[:\s]*((?:[#\w]+\s*)+)'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                hashtags = re.findall(r'#\w+', match.group(1))
        return list(set(hashtags))[:10]  # Limit to 10 unique hashtags