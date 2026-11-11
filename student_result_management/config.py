import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'student_secret_key_2026')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb+srv://<username>:<password>@cluster0.mongodb.net/student_result_db?retryWrites=true&w=majority')
    DB_NAME = os.getenv('DB_NAME', 'student_result_db')

    @staticmethod
    def calculate_percentage(obtained, total):
        if not total or total <= 0: return 0.0
        return round((float(obtained) / float(total)) * 100, 2)

    @staticmethod
    def calculate_grade(pct):
        if pct >= 90: return 'A+'
        if pct >= 80: return 'A'
        if pct >= 70: return 'B+'
        if pct >= 60: return 'B'
        if pct >= 50: return 'C'
        if pct >= 40: return 'P'
        return 'F'

get_grade = Config.calculate_grade
