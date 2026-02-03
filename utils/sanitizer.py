import re
class DataSanitizer:
    @staticmethod
    def clean_alphanumeric(text):
        if not text:
            return ""
        return re.sub(r'[^a-zA-Z0-9_\-\s]', '', str(text))
