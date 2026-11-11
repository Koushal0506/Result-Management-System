import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from database import get_db
from config import get_grade
from werkzeug.security import generate_password_hash

def seed_rich_dataset():
    db = get_db()
    print("=" * 60)
    print("POPULATING EXPANDED ACADEMIC DATASET IN MONGODB ATLAS...")
    print("=" * 60)

    # 1. Subjects across departments
    subjects = [
        # CSE Subjects
        {'subject_code': 'CS501', 'subject_name': 'Database Management Systems', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS502', 'subject_name': 'Operating Systems', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS503', 'subject_name': 'Computer Networks', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS504', 'subject_name': 'Software Engineering', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS505', 'subject_name': 'Design and Analysis of Algorithms', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        
        # IT Subjects
        {'subject_code': 'IT501', 'subject_name': 'Web Application Development', 'department': 'Information Technology', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'IT502', 'subject_name': 'Cloud Computing & Virtualization', 'department': 'Information Technology', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'IT503', 'subject_name': 'Cryptography & Network Security', 'department': 'Information Technology', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},

        # ECE Subjects
        {'subject_code': 'EC501', 'subject_name': 'Microprocessors & Microcontrollers', 'department': 'Electronics and Communication', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'EC502', 'subject_name': 'Digital Signal Processing', 'department': 'Electronics and Communication', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'EC503', 'subject_name': 'VLSI Design', 'department': 'Electronics and Communication', 'semester': 5, 'max_marks': 100, 'pass_marks': 40}
    ]

    for s in subjects:
        db.subjects.update_one({'subject_code': s['subject_code']}, {'$set': s}, upsert=True)
    print(f"✔ 1. Inserted/Updated {len(subjects)} Subjects")

    # 2. Examinations
    exams = [
        {'exam_name': 'End Semester Examination Nov-Dec 2025', 'semester': 5, 'academic_year': '2025-2026', 'exam_date': '2025-11-20'},
        {'exam_name': 'Mid Semester Assessment Oct 2025', 'semester': 5, 'academic_year': '2025-2026', 'exam_date': '2025-10-15'}
    ]
    for ex in exams:
        db.examinations.update_one({'exam_name': ex['exam_name']}, {'$set': ex}, upsert=True)
    
    exam_end_sem = db.examinations.find_one({'exam_name': 'End Semester Examination Nov-Dec 2025'})
    exam_mid_sem = db.examinations.find_one({'exam_name': 'Mid Semester Assessment Oct 2025'})
    print(f"✔ 2. Inserted/Updated {len(exams)} Examinations")

    # 3. Students
    students = [
        # CSE Students
        {'student_id': 'CS2023-01', 'roll_number': '23CS101', 'student_name': 'Aarav Sharma', 'email': 'aarav.sharma@college.edu', 'phone_number': '9876543210', 'gender': 'Male', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-02', 'roll_number': '23CS102', 'student_name': 'Diya Patel', 'email': 'diya.patel@college.edu', 'phone_number': '9876543211', 'gender': 'Female', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-03', 'roll_number': '23CS103', 'student_name': 'Rohan Verma', 'email': 'rohan.verma@college.edu', 'phone_number': '9876543212', 'gender': 'Male', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-04', 'roll_number': '23CS104', 'student_name': 'Ananya Iyer', 'email': 'ananya.iyer@college.edu', 'phone_number': '9876543213', 'gender': 'Female', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-05', 'roll_number': '23CS105', 'student_name': 'Kabir Mehta', 'email': 'kabir.mehta@college.edu', 'phone_number': '9876543214', 'gender': 'Male', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-06', 'roll_number': '23CS106', 'student_name': 'Pooja Reddy', 'email': 'pooja.reddy@college.edu', 'phone_number': '9876543215', 'gender': 'Female', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-07', 'roll_number': '23CS107', 'student_name': 'Vikram Singh', 'email': 'vikram.singh@college.edu', 'phone_number': '9876543216', 'gender': 'Male', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-08', 'roll_number': '23CS108', 'student_name': 'Sneha Nair', 'email': 'sneha.nair@college.edu', 'phone_number': '9876543217', 'gender': 'Female', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},

        # IT Students
        {'student_id': 'IT2023-01', 'roll_number': '23IT201', 'student_name': 'Aditya Joshi', 'email': 'aditya.joshi@college.edu', 'phone_number': '9876543218', 'gender': 'Male', 'department': 'Information Technology', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'IT2023-02', 'roll_number': '23IT202', 'student_name': 'Meera Kulkarni', 'email': 'meera.k@college.edu', 'phone_number': '9876543219', 'gender': 'Female', 'department': 'Information Technology', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'IT2023-03', 'roll_number': '23IT203', 'student_name': 'Kunal Deshmukh', 'email': 'kunal.d@college.edu', 'phone_number': '9876543220', 'gender': 'Male', 'department': 'Information Technology', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'IT2023-04', 'roll_number': '23IT204', 'student_name': 'Riya Sen', 'email': 'riya.sen@college.edu', 'phone_number': '9876543221', 'gender': 'Female', 'department': 'Information Technology', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},

        # ECE Students
        {'student_id': 'EC2023-01', 'roll_number': '23EC301', 'student_name': 'Arjun Rao', 'email': 'arjun.rao@college.edu', 'phone_number': '9876543222', 'gender': 'Male', 'department': 'Electronics and Communication', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'EC2023-02', 'roll_number': '23EC302', 'student_name': 'Tanvi Bhat', 'email': 'tanvi.bhat@college.edu', 'phone_number': '9876543223', 'gender': 'Female', 'department': 'Electronics and Communication', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'EC2023-03', 'roll_number': '23EC303', 'student_name': 'Nikhil Gupta', 'email': 'nikhil.g@college.edu', 'phone_number': '9876543224', 'gender': 'Male', 'department': 'Electronics and Communication', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'}
    ]

    for st in students:
        db.students.update_one({'roll_number': st['roll_number']}, {'$set': st}, upsert=True)
    print(f"✔ 3. Inserted/Updated {len(students)} Students")

    # 4. Results Generation (Real curriculum distribution)
    # CSE Curriculum: CS501, CS502, CS503, CS504, CS505
    cse_subs = list(db.subjects.find({'department': 'Computer Science and Engineering'}))
    it_subs = list(db.subjects.find({'department': 'Information Technology'}))
    ece_subs = list(db.subjects.find({'department': 'Electronics and Communication'}))

    # Pre-defined realistic marks mapping for variety
    student_scores = {
        '23CS101': [85, 78, 92, 88, 90],  # Aarav Sharma: Outstanding (A)
        '23CS102': [68, 72, 65, 70, 75],  # Diya Patel: Good (B+)
        '23CS103': [35, 42, 48, 38, 45],  # Rohan Verma: Fail (Backlog in CS501 & CS504)
        '23CS104': [95, 92, 94, 96, 91],  # Ananya Iyer: Rank 1 Outstanding (A+)
        '23CS105': [55, 60, 58, 62, 54],  # Kabir Mehta: Average (C / B)
        '23CS106': [82, 85, 80, 79, 84],  # Pooja Reddy: Distinction (A)
        '23CS107': [28, 34, 41, 35, 40],  # Vikram Singh: Needs Re-evaluation (Fail)
        '23CS108': [74, 76, 78, 72, 75],  # Sneha Nair: Very Good (B+)
        
        '23IT201': [88, 84, 82],           # Aditya Joshi: Excellent (A)
        '23IT202': [76, 79, 81],           # Meera Kulkarni: Very Good (B+)
        '23IT203': [38, 45, 52],           # Kunal Deshmukh: Fail (Backlog in IT501)
        '23IT204': [92, 90, 94],           # Riya Sen: Outstanding (A+)

        '23EC301': [85, 80, 87],           # Arjun Rao: Distinction (A)
        '23EC302': [65, 70, 68],           # Tanvi Bhat: Good (B)
        '23EC303': [32, 36, 45]            # Nikhil Gupta: Fail
    }

    results_count = 0
    all_students_db = {s['roll_number']: s for s in db.students.find()}

    for roll, scores in student_scores.items():
        st = all_students_db.get(roll)
        if not st:
            continue
        
        # Pick department subjects
        dept = st['department']
        if 'Computer' in dept:
            subs = cse_subs
        elif 'Information' in dept:
            subs = it_subs
        else:
            subs = ece_subs

        for idx, sub in enumerate(subs[:len(scores)]):
            score = scores[idx]
            max_m = float(sub.get('max_marks', 100))
            pass_m = float(sub.get('pass_marks', 40))
            pct = round((score / max_m) * 100, 2)
            grade = get_grade(pct)
            status = 'Pass' if score >= pass_m else 'Fail'

            doc = {
                'student_id': str(st['_id']),
                'student_name': st['student_name'],
                'roll_number': st['roll_number'],
                'subject_id': str(sub['_id']),
                'subject_code': sub['subject_code'],
                'subject_name': sub['subject_name'],
                'exam_id': str(exam_end_sem['_id']),
                'exam_name': exam_end_sem['exam_name'],
                'marks_obtained': score,
                'max_marks': max_m,
                'pass_marks': pass_m,
                'percentage': pct,
                'grade': grade,
                'status': status
            }

            db.results.update_one(
                {'student_id': doc['student_id'], 'subject_id': doc['subject_id'], 'exam_id': doc['exam_id']},
                {'$set': doc},
                upsert=True
            )
            results_count += 1

    print(f"✔ 4. Inserted/Updated {results_count} Examination Result Records")

    # 5. More Faculty / Evaluators for the Directory
    faculty_members = [
        {'username': 'dr_sharma', 'full_name': 'Dr. Alok Sharma', 'email': 'alok.sharma@college.edu', 'role': 'faculty'},
        {'username': 'prof_priya', 'full_name': 'Prof. Priya Menon', 'email': 'priya.menon@college.edu', 'role': 'faculty'},
        {'username': 'dr_venkat', 'full_name': 'Dr. Venkat Raman', 'email': 'venkat.raman@college.edu', 'role': 'faculty'}
    ]
    for fac in faculty_members:
        if not db.users.find_one({'username': fac['username']}):
            fac['password_hash'] = generate_password_hash('faculty123')
            db.users.insert_one(fac)
    print("✔ 5. Verified Faculty Directory Records")

    print("-" * 60)
    print(f"DATABASE SUMMARY:")
    print(f" - Total Students     : {db.students.count_documents({})}")
    print(f" - Total Subjects     : {db.subjects.count_documents({})}")
    print(f" - Total Examinations : {db.examinations.count_documents({})}")
    print(f" - Total Results      : {db.results.count_documents({})}")
    print(f" - Total Users/Faculty: {db.users.count_documents({})}")
    print("=" * 60)
    print("ALL DATA UPLOADED SUCCESSFULLY TO MONGODB ATLAS!")

if __name__ == '__main__':
    seed_rich_dataset()
