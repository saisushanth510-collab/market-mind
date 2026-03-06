import re

class TextCleaner:
    
    def remove_extra_spaces(self, text):
        """Remove extra spaces from text"""
        return re.sub(r'\s+', ' ', text).strip()

    def remove_special_characters(self, text):
        """Remove unnecessary special characters"""
        return re.sub(r'[^a-zA-Z0-9\s.,!?-]', '', text)

    def clean_text(self, text):
        """Complete text cleaning pipeline"""
        text = self.remove_extra_spaces(text)
        text = self.remove_special_characters(text)
        return text