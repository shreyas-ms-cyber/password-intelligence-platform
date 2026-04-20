import math
import re
import string
import os

class PasswordIntelligenceEngine:
    def __init__(self, dictionary_path=None):
        self.common_passwords = set()
        if dictionary_path and os.path.exists(dictionary_path):
            with open(dictionary_path, 'r') as f:
                self.common_passwords = {line.strip().lower() for line in f}

    def calculate_entropy(self, password):
        """Calculates Shannon entropy of the password."""
        if not password:
            return 0
        
        charset_size = 0
        if any(c in string.ascii_lowercase for c in password): charset_size += 26
        if any(c in string.ascii_uppercase for c in password): charset_size += 26
        if any(c in string.digits for c in password): charset_size += 10
        if any(c in string.punctuation for c in password): charset_size += 32
        
        # If we have characters not in standard sets, assume a larger charset
        other_chars = set(password) - set(string.ascii_letters + string.digits + string.punctuation)
        if other_chars:
            charset_size += len(other_chars) * 2 # Conservative estimate for unicode etc.

        if charset_size == 0:
            return 0
            
        entropy = len(password) * math.log2(charset_size)
        return round(entropy, 2)

    def detect_patterns(self, password):
        """Detects sequential, repeated, and mirrored patterns."""
        findings = []
        
        # Sequential characters (abc, 123)
        sequences = ["abcdefghijklmnopqrstuvwxyz", "01234567890", "qwertyuiop", "asdfghjkl", "zxcvbnm"]
        for seq in sequences:
            for i in range(len(password) - 2):
                sub = password[i:i+3].lower()
                if sub in seq or sub[::-1] in seq:
                    findings.append(f"Sequential pattern detected: '{sub}'")
                    break

        # Repeated characters (aaa, 111)
        if re.search(r'(.)\1\1', password):
            findings.append("Repeated character patterns detected.")

        # Dictionary check
        if password.lower() in self.common_passwords:
            findings.append("Commonly leaked/dictionary password.")

        return findings

    def estimate_crack_time(self, entropy):
        """Estimates crack time based on entropy and hash rates."""
        # Rates (hashes per second)
        # Low: 1e6 (Desktop CPU)
        # Mid: 1e10 (High-end GPU Cluster)
        # High: 1e14 (Supercomputer / Botnet)
        
        combinations = 2**entropy
        
        def format_time(seconds):
            if seconds < 1: return "Instantly"
            if seconds < 60: return f"{round(seconds)} seconds"
            if seconds < 3600: return f"{round(seconds/60)} minutes"
            if seconds < 86400: return f"{round(seconds/3600)} hours"
            if seconds < 31536000: return f"{round(seconds/86400)} days"
            if seconds < 3153600000: return f"{round(seconds/31536000)} years"
            return "Centuries"

        return {
            "offline_fast": format_time(combinations / 1e10), # GPU
            "online_throttled": format_time(combinations / 100), # Web login
            "brute_force_guess": combinations
        }

    def get_score_and_label(self, entropy, findings):
        """Calculates a normalized score 0-100 and labels it."""
        # Penalty for patterns
        penalty = len(findings) * 15
        base_score = min(100, (entropy / 80) * 100) # 80 bits is considered strong
        
        final_score = max(0, base_score - penalty)
        
        label = "Critical"
        color = "#ff4d4d"
        if final_score > 80:
            label = "Enterprise-Grade"
            color = "#00ffcc"
        elif final_score > 60:
            label = "Strong"
            color = "#33cc33"
        elif final_score > 40:
            label = "Moderate"
            color = "#ffcc00"
        elif final_score > 20:
            label = "Weak"
            color = "#ff6600"
            
        return {
            "score": round(final_score),
            "label": label,
            "color": color
        }

    def generate_secure_password(self, length=16, use_symbols=True):
        """Generates a cryptographically secure random password."""
        chars = string.ascii_letters + string.digits
        if use_symbols:
            chars += string.punctuation
        
        import secrets
        return ''.join(secrets.choice(chars) for _ in range(length))

    def get_ai_advice(self, password, findings, entropy):
        """Generates AI-style feedback."""
        advice = []
        if len(password) < 12:
            advice.append("Increase length to at least 12 characters.")
        if not any(c in string.punctuation for c in password):
            advice.append("Include special characters like !, @, # to increase complexity.")
        if findings:
            advice.append("Avoid predictable sequences or common words.")
        
        if entropy < 40:
            alternative = self.generate_secure_password(14)
            advice.append(f"Consider using a passphrase or a generated one like: {alternative}")
            
        return advice if advice else ["This password meets high-security standards."]
