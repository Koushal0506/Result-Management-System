# Student Result Management System

A clean, practical, and authentic web-based academic record management system developed as a **Third-Year Computer Science Internship Project**.

Built with **Python Flask**, **Jinja2**, **HTML5**, **CSS3**, **JavaScript**, and a **Remote MySQL Database**.

---

## 📌 Project Overview

This project provides an automated, centralized platform for colleges and academic institutions to:
- Enroll and manage student profiles.
- Define curriculum subjects, course credits, maximum marks, and passing thresholds.
- Schedule and manage examination sessions.
- Record student marks with automated calculation of percentages, letter grades (A+, A, B+, B, C, P, F), and pass/fail evaluation.
- View real-time SQL-calculated analytics on a faculty dashboard.
- Generate and print university-style grade cards (Marksheets).
- Export evaluation reports in CSV and PDF formats.

---

## 🛠️ Technology Stack

- **Frontend:**
  - HTML5 & Jinja2 Templates
  - CSS3 (Custom styling with a light background and blue & white academic palette)
  - JavaScript (Form validation and live grade preview calculations)
  - Bootstrap 5 (Responsive grid, basic buttons, and form layouts)
- **Backend:**
  - Python 3
  - Flask (Routing, session management, template rendering)
  - Werkzeug (Secure password hashing using PBKDF2/Scrypt)
  - ReportLab (Server-side PDF marksheet generation)
- **Database:**
  - MySQL hosted on a remote/cloud database server (e.g. Aiven, TiDB Cloud, Clever Cloud, AlwaysData, AWS RDS)
  - PyMySQL connector with parameterized queries to prevent SQL injection

---

## 📁 Project Folder Structure

```
student_result_management/
│
├── app.py                  # Main Flask application with routes and controllers
├── config.py               # Environment configuration and grading logic
├── database.py             # Remote MySQL connection handler and schema initializer
├── requirements.txt        # Python package dependencies
├── .env                    # Environment variables (DB credentials, secret key)
├── .env.example            # Sample configuration template
├── schema.sql              # Remote MySQL schema with tables and initial seed data
├── test_db.py              # Remote MySQL connectivity testing script
├── test_app.py             # Automated unit and integration test suite
│
├── templates/              # Jinja2 HTML templates
│   ├── base.html           # Common layout, navigation bar, alerts, and footer
│   ├── index.html          # Public home and project overview page
│   ├── register.html       # Faculty registration form
│   ├── login.html          # Portal authentication form
│   ├── dashboard.html      # Analytics dashboard with SQL metrics and recent records
│   ├── add_student.html    # Student enrollment form
│   ├── view_students.html  # Student directory with search and multi-filter
│   ├── update_student.html # Edit student profile form
│   ├── subjects.html       # Subject and syllabus master management
│   ├── examinations.html   # Examination session management
│   ├── add_result.html     # Mark entry form with live preview calculations
│   ├── view_results.html   # Results directory with search and status filters
│   ├── marksheet.html      # Printable official college grade card
│   └── reports.html        # Export hub (CSV spreadsheets & PDF marksheets)
│
└── static/
    ├── css/
    │   └── style.css       # Custom student project CSS (Blue & White aesthetic)
    ├── js/
    │   └── script.js       # Client validation and UI helpers
    └── images/             # Static assets and icons
```

---

## 🗄️ Database Architecture (`schema.sql`)

The database consists of 5 relational tables linked with foreign keys and cascade deletions:

1. **`users`**: System faculty and administrators.
   - `id`, `username`, `email`, `password_hash`, `full_name`, `role`, `created_at`
2. **`students`**: Student records.
   - `id`, `student_id`, `roll_number`, `student_name`, `email`, `phone_number`, `gender`, `date_of_birth`, `department`, `course`, `semester`, `academic_year`, `address`, `created_at`
3. **`subjects`**: Academic courses.
   - `id`, `subject_code`, `subject_name`, `department`, `semester`, `max_marks`, `pass_marks`, `created_at`
4. **`examinations`**: Examination terms.
   - `id`, `exam_name`, `semester`, `academic_year`, `exam_date`, `created_at`
5. **`results`**: Subject evaluation records.
   - `id`, `student_id` (FK), `subject_id` (FK), `exam_id` (FK), `marks_obtained`, `max_marks`, `percentage`, `grade`, `status` ('Pass'/'Fail'), `remarks`, `created_at`

---

## 🌐 Setting Up Remote MySQL Database

You can connect this application to any remote cloud MySQL server. Examples of free cloud MySQL hosts:
- **TiDB Cloud Serverless** (Free, MySQL compatible): [tidbcloud.com](https://tidbcloud.com)
- **Aiven for MySQL** (Free tier): [aiven.io](https://aiven.io)
- **Clever Cloud** (Free MySQL add-on): [clever-cloud.com](https://clever-cloud.com)
- **AlwaysData** (Free 100MB remote MySQL): [alwaysdata.com](https://alwaysdata.com)

### Configuring `.env`:
Copy `.env.example` to `.env` and fill in your remote database details:

```ini
DB_HOST=your-remote-mysql-host.com
DB_PORT=3306
DB_USER=your_remote_db_user
DB_PASSWORD=your_remote_password
DB_NAME=student_result_db
DB_SSL=False   # Set to True if your cloud provider requires SSL (e.g. TiDB Cloud)

SECRET_KEY=college_student_result_mgmt_secret_key_2026
FLASK_PORT=5000
```

---

## 🚀 How to Run the Application

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Test remote database connection:**
   ```bash
   python test_db.py
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```

4. **Access the portal:**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

5. **Run the test suite:**
   ```bash
   python test_app.py
   ```

---

## 🎓 Grading Criteria

| Percentage Range | Grade | Performance Description | Result Status |
| :--- | :--- | :--- | :--- |
| **90% - 100%** | **A+** | Outstanding | PASS |
| **80% - 89.9%** | **A** | Excellent | PASS |
| **70% - 79.9%** | **B+** | Very Good | PASS |
| **60% - 69.9%** | **B** | Good | PASS |
| **50% - 59.9%** | **C** | Average | PASS |
| **40% - 49.9%** | **P** | Pass (Threshold) | PASS |
| **< 40%** | **F** | Fail | FAIL |

