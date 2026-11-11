import io, csv
from functools import wraps
from bson.objectid import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash, session, Response, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config, get_grade
from database import get_db, check_connection

app = Flask(__name__)
app.config.from_object(Config)

@app.context_processor
def inject_user():
    admin_endpoints = {'dashboard', 'view_students', 'add_student', 'update_student',
                       'manage_subjects', 'manage_examinations', 'view_results', 'add_result',
                       'upload_results', 'reports', 'manage_faculty', 'register'}
    return {
        'logged_in': 'user_id' in session,
        'is_admin_page': request.endpoint in admin_endpoints if request.endpoint else False,
        'current_user': session.get('username'),
        'current_username': session.get('username'),
        'current_full_name': session.get('full_name'),
        'current_role': session.get('role', 'admin')
    }

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Access Restricted: Only College Administrators & Faculty can access backend management features. Students can only check results on the public portal.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return wrapper

@app.route('/')
def index():
    db = get_db()
    try: exams = list(db.examinations.find().sort('_id', -1))
    except Exception: exams = []
    return render_template('index.html', examinations=exams)

@app.route('/check-result', methods=['GET', 'POST'])
def check_result():
    db = get_db()
    if request.method == 'POST':
        roll = request.form.get('roll_number', '').strip()
        student = db.students.find_one({"roll_number": {"$regex": f"^{roll}$", "$options": "i"}})
        if not student:
            flash(f"No student record found with Roll Number '{roll}'. Please verify.", "danger")
            return redirect(url_for('index'))
        return redirect(url_for('view_marksheet', student_id=str(student['_id'])))
    try: exams = list(db.examinations.find().sort('_id', -1))
    except Exception: exams = []
    return render_template('index.html', examinations=exams)

@app.route('/health')
def health():
    ok, msg = check_connection()
    return {'status': 'healthy' if ok else 'db_offline', 'message': msg}

@app.route('/register', methods=['GET', 'POST'])
def register():
    db = get_db()
    user_count = db.users.count_documents({})
    is_initial_setup = (user_count == 0)

    # Restrict registration to logged-in admin (unless no users exist yet)
    if not is_initial_setup and 'user_id' not in session:
        flash('Registration is restricted. Only an administrator can register faculty accounts.', 'warning')
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        u, f, e = request.form['username'].strip(), request.form['full_name'].strip(), request.form['email'].strip().lower()
        p, cp = request.form['password'], request.form['confirm_password']
        role = 'admin' if is_initial_setup else request.form.get('role', 'faculty')

        if p != cp:
            flash('Passwords do not match.', 'danger')
        elif db.users.find_one({"$or": [{"username": u}, {"email": e}]}):
            flash('Username or email already exists.', 'warning')
        else:
            db.users.insert_one({"username": u, "full_name": f, "email": e, "password_hash": generate_password_hash(p), "role": role})
            if is_initial_setup:
                flash('Initial Admin account created! Please login.', 'success')
                return redirect(url_for('admin_login'))
            flash(f"Faculty account '{u}' registered successfully!", 'success')
            return redirect(url_for('manage_faculty'))

    return render_template('register.html', is_initial_setup=is_initial_setup)

@app.route('/faculty')
@login_required
def manage_faculty():
    db = get_db()
    faculty_list = list(db.users.find({}, {'password_hash': 0}).sort('_id', -1))
    return render_template('faculty.html', faculty_list=faculty_list)

@app.route('/faculty/delete/<id>', methods=['POST'])
@login_required
def delete_faculty(id):
    db = get_db()
    if id == session.get('user_id'):
        flash("You cannot delete your own logged-in account.", "warning")
    else:
        db.users.delete_one({"_id": ObjectId(id)})
        flash("Faculty account removed.", "info")
    return redirect(url_for('manage_faculty'))

@app.route('/admin/login', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def admin_login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        db = get_db()
        ident = request.form.get('identity', '').strip()
        pwd = request.form.get('password', '')
        user = db.users.find_one({"$or": [{"username": ident}, {"email": ident.lower()}]})
        if user and check_password_hash(user['password_hash'], pwd):
            session['user_id'] = str(user['_id'])
            session['username'] = user['username']
            session['full_name'] = user.get('full_name', user['username'])
            session['role'] = user.get('role', 'admin')
            flash(f"Welcome back, {session['full_name']}! Signed into Admin Panel.", "success")
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

def login():
    return admin_login()

@app.route('/admin/logout')
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/dashboard')
@login_required
def dashboard():
    db = get_db()
    try:
        stats = {
            'total_students': db.students.count_documents({}),
            'total_results': db.results.count_documents({}),
            'total_subjects': db.subjects.count_documents({}),
            'total_exams': db.examinations.count_documents({}),
            'passed_count': len(db.results.distinct('student_id', {'status': 'Pass'})),
            'failed_count': len(db.results.distinct('student_id', {'status': 'Fail'}))
        }
        recents = list(db.students.find().sort('_id', -1).limit(5))
        recent_res = list(db.results.find().sort('_id', -1).limit(5))
    except Exception:
        stats, recents, recent_res = {'total_students': 0, 'total_results': 0, 'total_subjects': 0, 'total_exams': 0, 'passed_count': 0, 'failed_count': 0}, [], []
    return render_template('dashboard.html', stats=stats, recent_students=recents, recent_results=recent_res)

@app.route('/students')
@login_required
def view_students():
    db = get_db()
    q, sem, dept = request.args.get('search', '').strip(), request.args.get('semester', ''), request.args.get('department', '')
    query = {}
    if q:
        query['$or'] = [{'student_name': {'$regex': q, '$options': 'i'}},
                        {'roll_number': {'$regex': q, '$options': 'i'}},
                        {'student_id': {'$regex': q, '$options': 'i'}}]
    if sem: query['semester'] = int(sem) if sem.isdigit() else sem
    if dept: query['department'] = dept
    try: students = list(db.students.find(query).sort('_id', -1))
    except Exception: students = []
    return render_template('view_students.html', students=students, search=q, sem=sem, dept=dept)

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def add_student():
    if request.method == 'POST':
        db = get_db()
        d = request.form.to_dict()
        if db.students.find_one({"$or": [{"student_id": d['student_id']}, {"roll_number": d['roll_number']}]}):
            flash('Student ID or Roll Number already exists.', 'warning')
        else:
            db.students.insert_one(d)
            flash('Student added successfully!', 'success')
            return redirect(url_for('view_students'))
    return render_template('add_student.html')

@app.route('/students/edit/<id>', methods=['GET', 'POST'])
@login_required
def update_student(id):
    db = get_db()
    student = db.students.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        db.students.update_one({"_id": ObjectId(id)}, {"$set": request.form.to_dict()})
        flash('Student updated successfully!', 'success')
        return redirect(url_for('view_students'))
    return render_template('update_student.html', student=student)

@app.route('/students/delete/<id>', methods=['POST'])
@login_required
def delete_student(id):
    db = get_db()
    db.students.delete_one({"_id": ObjectId(id)})
    db.results.delete_many({"student_id": id})
    flash('Student deleted.', 'info')
    return redirect(url_for('view_students'))

@app.route('/subjects', methods=['GET', 'POST'])
@login_required
def manage_subjects():
    db = get_db()
    if request.method == 'POST':
        d = request.form.to_dict()
        d['subject_code'] = d['subject_code'].upper()
        db.subjects.update_one({"subject_code": d['subject_code']}, {"$set": d}, upsert=True)
        flash('Subject saved.', 'success')
    try: subs = list(db.subjects.find().sort('subject_code', 1))
    except Exception: subs = []
    return render_template('subjects.html', subjects=subs)

@app.route('/subjects/delete/<id>', methods=['POST'])
@login_required
def delete_subject(id):
    get_db().subjects.delete_one({"_id": ObjectId(id)})
    flash('Subject deleted.', 'info')
    return redirect(url_for('manage_subjects'))

@app.route('/examinations', methods=['GET', 'POST'])
@login_required
def manage_examinations():
    db = get_db()
    if request.method == 'POST':
        db.examinations.insert_one(request.form.to_dict())
        flash('Exam session added.', 'success')
    try: exams = list(db.examinations.find().sort('_id', -1))
    except Exception: exams = []
    return render_template('examinations.html', examinations=exams)

@app.route('/examinations/delete/<id>', methods=['POST'])
@login_required
def delete_examination(id):
    get_db().examinations.delete_one({"_id": ObjectId(id)})
    flash('Exam session deleted.', 'info')
    return redirect(url_for('manage_examinations'))

@app.route('/results')
@login_required
def view_results():
    db = get_db()
    q, status = request.args.get('search', '').strip(), request.args.get('status', '')
    query = {}
    if q:
        query['$or'] = [{'student_name': {'$regex': q, '$options': 'i'}},
                        {'roll_number': {'$regex': q, '$options': 'i'}},
                        {'subject_name': {'$regex': q, '$options': 'i'}}]
    if status in ('Pass', 'Fail'): query['status'] = status
    try: results = list(db.results.find(query).sort('_id', -1))
    except Exception: results = []
    return render_template('view_results.html', results=results, search=q, status=status)

@app.route('/results/add', methods=['GET', 'POST'])
@login_required
def add_result():
    db = get_db()
    try:
        students = list(db.students.find().sort('roll_number', 1))
        subjects = list(db.subjects.find().sort('subject_code', 1))
        exams = list(db.examinations.find().sort('_id', -1))
    except Exception:
        students, subjects, exams = [], [], []

    if request.method == 'POST':
        sid, eid, sub_id = request.form['student_id'], request.form['exam_id'], request.form['subject_id']
        marks = float(request.form['marks_obtained'])
        student = db.students.find_one({"_id": ObjectId(sid)})
        subject = db.subjects.find_one({"_id": ObjectId(sub_id)})
        exam = db.examinations.find_one({"_id": ObjectId(eid)})

        max_m = float(subject.get('max_marks', 100))
        pct = round((marks / max_m) * 100, 2)
        grade = get_grade(pct)
        status = 'Pass' if marks >= float(subject.get('pass_marks', 40)) else 'Fail'

        doc = {
            'student_id': sid, 'student_name': student['student_name'], 'roll_number': student['roll_number'],
            'subject_id': sub_id, 'subject_code': subject['subject_code'], 'subject_name': subject['subject_name'],
            'exam_id': eid, 'exam_name': exam['exam_name'],
            'marks_obtained': marks, 'max_marks': max_m, 'pass_marks': subject.get('pass_marks', 40),
            'percentage': pct, 'grade': grade, 'status': status
        }
        db.results.update_one({'student_id': sid, 'subject_id': sub_id, 'exam_id': eid}, {'$set': doc}, upsert=True)
        flash(f'Result saved! {marks}/{max_m} ({pct}%) - {status} [{grade}]', 'success')
        return redirect(url_for('view_results'))

    return render_template('add_result.html', students=students, subjects=subjects, examinations=exams)

@app.route('/upload-results', methods=['GET', 'POST'])
@login_required
def upload_results():
    db = get_db()
    if request.method == 'POST':
        # CSV File Bulk Upload
        if 'csv_file' in request.files and request.files['csv_file'].filename:
            stream = io.StringIO(request.files['csv_file'].stream.read().decode("utf-8"), newline=None)
            count = 0
            for row in csv.DictReader(stream):
                roll, sub_code = row.get('roll_number', '').strip(), row.get('subject_code', '').strip().upper()
                exam_name = row.get('exam_name', '').strip()
                marks = float(row.get('marks_obtained', 0))

                student = db.students.find_one({"roll_number": roll})
                subject = db.subjects.find_one({"subject_code": sub_code})
                exam = db.examinations.find_one({"exam_name": exam_name}) or db.examinations.find_one()
                if student and subject:
                    max_m = float(subject.get('max_marks', 100))
                    pct = round((marks / max_m) * 100, 2)
                    doc = {
                        'student_id': str(student['_id']), 'student_name': student['student_name'], 'roll_number': student['roll_number'],
                        'subject_id': str(subject['_id']), 'subject_code': subject['subject_code'], 'subject_name': subject['subject_name'],
                        'exam_id': str(exam['_id']) if exam else '1', 'exam_name': exam['exam_name'] if exam else 'Exam',
                        'marks_obtained': marks, 'max_marks': max_m, 'pass_marks': subject.get('pass_marks', 40),
                        'percentage': pct, 'grade': get_grade(pct), 'status': 'Pass' if marks >= float(subject.get('pass_marks', 40)) else 'Fail'
                    }
                    db.results.update_one({'student_id': doc['student_id'], 'subject_code': sub_code}, {'$set': doc}, upsert=True)
                    count += 1
            flash(f"Successfully uploaded {count} results from CSV!", "success")
            return redirect(url_for('view_results'))

        # Quick Semester Results Form
        sid, eid = request.form.get('student_id'), request.form.get('exam_id')
        if sid and eid:
            student = db.students.find_one({"_id": ObjectId(sid)})
            exam = db.examinations.find_one({"_id": ObjectId(eid)})
            subjects = list(db.subjects.find())
            for sub in subjects:
                key = f"marks_{sub['subject_code']}"
                if key in request.form and request.form[key].strip():
                    marks = float(request.form[key])
                    max_m = float(sub.get('max_marks', 100))
                    pct = round((marks / max_m) * 100, 2)
                    doc = {
                        'student_id': sid, 'student_name': student['student_name'], 'roll_number': student['roll_number'],
                        'subject_id': str(sub['_id']), 'subject_code': sub['subject_code'], 'subject_name': sub['subject_name'],
                        'exam_id': eid, 'exam_name': exam['exam_name'],
                        'marks_obtained': marks, 'max_marks': max_m, 'pass_marks': sub.get('pass_marks', 40),
                        'percentage': pct, 'grade': get_grade(pct), 'status': 'Pass' if marks >= float(sub.get('pass_marks', 40)) else 'Fail'
                    }
                    db.results.update_one({'student_id': sid, 'subject_id': str(sub['_id']), 'exam_id': eid}, {'$set': doc}, upsert=True)
            flash("All semester marks saved successfully!", "success")
            return redirect(url_for('view_results'))

    students = list(db.students.find().sort('roll_number', 1))
    subjects = list(db.subjects.find().sort('subject_code', 1))
    exams = list(db.examinations.find().sort('_id', -1))
    return render_template('upload_results.html', students=students, subjects=subjects, examinations=exams)

@app.route('/download-sample-csv')
def download_sample_csv():
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(['roll_number', 'subject_code', 'exam_name', 'marks_obtained'])
    writer.writerow(['23CS101', 'CS501', 'End Semester Examination Nov-Dec 2025', '85'])
    writer.writerow(['23CS101', 'CS502', 'End Semester Examination Nov-Dec 2025', '78'])
    writer.writerow(['23CS102', 'CS501', 'End Semester Examination Nov-Dec 2025', '65'])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=sample_results.csv"})

@app.route('/results/delete/<id>', methods=['POST'])
@login_required
def delete_result(id):
    get_db().results.delete_one({"_id": ObjectId(id)})
    flash('Result deleted.', 'info')
    return redirect(url_for('view_results'))

@app.route('/marksheet/<student_id>')
def view_marksheet(student_id):
    db = get_db()
    student = db.students.find_one({"_id": ObjectId(student_id)})
    results = list(db.results.find({"student_id": student_id}))
    total_max = sum(float(r['max_marks']) for r in results)
    total_obt = sum(float(r['marks_obtained']) for r in results)
    pct = round((total_obt / total_max * 100), 2) if total_max else 0
    status = 'Fail' if any(r.get('status') == 'Fail' for r in results) or pct < 40 else 'Pass'
    grade = get_grade(pct)
    summary = {
        'total_max': total_max,
        'total_obtained': total_obt,
        'percentage': pct,
        'grade': grade,
        'status': status,
        'overall_percentage': pct,
        'overall_grade': grade,
        'overall_status': status,
        'exam_name': results[0].get('exam_name', 'Semester Examination') if results else '',
        'academic_year': student.get('academic_year', '') if student else ''
    }
    return render_template('marksheet.html', student=student, results=results, summary=summary)

@app.route('/reports')
@login_required
def reports():
    db = get_db()
    try:
        exams = list(db.examinations.find())
        students = list(db.students.find())
    except Exception: exams, students = [], []
    return render_template('reports.html', examinations=exams, students=students)

@app.route('/reports/export/csv')
@login_required
def export_csv():
    results = list(get_db().results.find())
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(['Roll No', 'Name', 'Subject Code', 'Subject', 'Exam', 'Marks', 'Max', '%', 'Grade', 'Status'])
    for r in results:
        writer.writerow([r.get('roll_number'), r.get('student_name'), r.get('subject_code'), r.get('subject_name'), r.get('exam_name'), r.get('marks_obtained'), r.get('max_marks'), r.get('percentage'), r.get('grade'), r.get('status')])
    return Response(out.getvalue(), mimetype="text/csv", headers={"Content-Disposition": "attachment;filename=results.csv"})

@app.route('/reports/export/pdf/<student_id>')
def export_pdf(student_id):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib import colors

    db = get_db()
    student = db.students.find_one({"_id": ObjectId(student_id)})
    results = list(db.results.find({"student_id": student_id}))
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()
    elems = [Paragraph("<b>STUDENT RESULT MANAGEMENT SYSTEM</b>", styles['Title']),
             Paragraph(f"Marksheet for {student['student_name']} (Roll: {student['roll_number']}) - Sem {student.get('semester')}", styles['Normal']),
             Spacer(1, 15)]

    data = [["Code", "Subject", "Max", "Pass", "Obtained", "Grade", "Status"]]
    for r in results:
        data.append([r.get('subject_code',''), r.get('subject_name',''), str(r.get('max_marks','')), str(r.get('pass_marks','')), str(r.get('marks_obtained','')), r.get('grade',''), r.get('status','')])
    t = Table(data, colWidths=[60, 200, 50, 50, 60, 50, 60])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a56db')),
                           ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                           ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                           ('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    elems.append(t)
    doc.build(elems)
    buf.seek(0)
    return send_file(buf, as_attachment=True, download_name=f"Marksheet_{student['roll_number']}.pdf", mimetype='application/pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
