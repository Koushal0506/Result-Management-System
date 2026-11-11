import unittest, io, sys, os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from app import app
from config import Config

class StudentResultSystemTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_grade_calculation(self):
        self.assertEqual(Config.calculate_grade(95.0), 'A+')
        self.assertEqual(Config.calculate_grade(85.0), 'A')
        self.assertEqual(Config.calculate_grade(75.0), 'B+')
        self.assertEqual(Config.calculate_grade(65.0), 'B')
        self.assertEqual(Config.calculate_grade(55.0), 'C')
        self.assertEqual(Config.calculate_grade(45.0), 'P')
        self.assertEqual(Config.calculate_grade(35.0), 'F')

    def test_routes_accessible(self):
        self.assertEqual(self.client.get('/').status_code, 200)
        self.assertEqual(self.client.get('/login').status_code, 200)
        self.assertEqual(self.client.get('/register').status_code, 200)
        self.assertEqual(self.client.get('/check-result').status_code, 200)
        self.assertEqual(self.client.get('/health').status_code, 200)

    def test_login_required(self):
        for url in ['/dashboard', '/students', '/students/add', '/results', '/results/add', '/upload-results', '/reports']:
            res = self.client.get(url)
            self.assertEqual(res.status_code, 302, f"{url} should redirect when not logged in")

    def test_authenticated_dashboard(self):
        with self.client.session_transaction() as sess:
            sess['user_id'] = 1
            sess['username'] = 'admin'
            sess['full_name'] = 'Administrator'
        res = self.client.get('/dashboard')
        self.assertEqual(res.status_code, 200)

    def test_pdf_generation(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph
        from reportlab.lib.styles import getSampleStyleSheet
        buf = io.BytesIO()
        SimpleDocTemplate(buf, pagesize=letter).build([Paragraph("Test", getSampleStyleSheet()['Normal'])])
        self.assertTrue(buf.getvalue().startswith(b'%PDF-'))

if __name__ == '__main__':
    unittest.main()
