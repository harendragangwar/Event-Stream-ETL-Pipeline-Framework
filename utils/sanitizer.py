import re

class DataSanitizer:
    @staticmethod
    def clean_alphanumeric(text):
        if not text:
            return ""
        safe_text = str(text).encode('ascii', 'ignore').decode('ascii')
        cleaned = re.sub(r'[^a-zA-Z0-9_\-\s]', '', safe_text)
        return " ".join(cleaned.split())

    @staticmethod
    def is_valid_uuid(token):
        if not token:
            return False
        return bool(re.match(r'^evt_[a-zA-Z0-9_\-]+$', str(token)))

    @staticmethod
    def enforce_string_limits(text, max_len=64):
        cleaned = DataSanitizer.clean_alphanumeric(text)
        return cleaned[:max_len]

    @staticmethod
    def strip_sql_injection_chars(text):
        if not text:
            return ""
        return re.sub(r"['\";\-]", "", str(text))
