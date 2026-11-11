"""
Database seeder for MongoDB Atlas.
Populates sample subjects, examinations, students, and results.
"""
from database import get_db
from config import get_grade

def seed():
    db = get_db()
    print("Seeding MongoDB Atlas with sample academic data...")

    # 1. Subjects
    subjects = [
        {'subject_code': 'CS501', 'subject_name': 'Database Management Systems', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS502', 'subject_name': 'Operating Systems', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS503', 'subject_name': 'Computer Networks', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40},
        {'subject_code': 'CS504', 'subject_name': 'Software Engineering', 'department': 'Computer Science and Engineering', 'semester': 5, 'max_marks': 100, 'pass_marks': 40}
    ]
    for s in subjects:
        db.subjects.update_one({'subject_code': s['subject_code']}, {'$set': s}, upsert=True)

    # 2. Examination
    exam = {'exam_name': 'End Semester Examination Nov-Dec 2025', 'semester': 5, 'academic_year': '2025-2026', 'exam_date': '2025-11-20'}
    db.examinations.update_one({'exam_name': exam['exam_name']}, {'$set': exam}, upsert=True)
    exam_doc = db.examinations.find_one({'exam_name': exam['exam_name']})

    # 3. Students
    students = [
        {'student_id': 'CS2023-01', 'roll_number': '23CS101', 'student_name': 'Aarav Sharma', 'email': 'aarav@college.edu', 'phone_number': '9876543210', 'gender': 'Male', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-02', 'roll_number': '23CS102', 'student_name': 'Diya Patel', 'email': 'diya@college.edu', 'phone_number': '9876543211', 'gender': 'Female', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'},
        {'student_id': 'CS2023-03', 'roll_number': '23CS103', 'student_name': 'Rohan Verma', 'email': 'rohan@college.edu', 'phone_number': '9876543212', 'gender': 'Male', 'department': 'Computer Science and Engineering', 'course': 'B.Tech', 'semester': 5, 'academic_year': '2025-2026'}
    ]
    for st in students:
        db.students.update_one({'roll_number': st['roll_number']}, {'$set': st}, upsert=True)

    # 4. Results
    stud_docs = list(db.students.find().limit(3))
    sub_docs = list(db.subjects.find().limit(4))
    sample_scores = [[85, 78, 92, 88], [65, 70, 58, 62], [35, 42, 48, 38]]

    for i, stud in enumerate(stud_docs):
        scores = sample_scores[i % len(sample_scores)]
        for j, sub in enumerate(sub_docs):
            score = scores[j % len(scores)]
            max_m = float(sub.get('max_marks', 100))
            pct = round((score / max_m) * 100, 2)
            grade = get_grade(pct)
            status = 'Pass' if score >= float(sub.get('pass_marks', 40)) else 'Fail'

            doc = {
                'student_id': str(stud['_id']), 'student_name': stud['student_name'], 'roll_number': stud['roll_number'],
                'subject_id': str(sub['_id']), 'subject_code': sub['subject_code'], 'subject_name': sub['subject_name'],
                'exam_id': str(exam_doc['_id']), 'exam_name': exam_doc['exam_name'],
                'marks_obtained': score, 'max_marks': max_m, 'pass_marks': sub.get('pass_marks', 40),
                'percentage': pct, 'grade': grade, 'status': status
            }
            db.results.update_one({'student_id': doc['student_id'], 'subject_id': doc['subject_id'], 'exam_id': doc['exam_id']}, {'$set': doc}, upsert=True)

    print("[SUCCESS] MongoDB Atlas seeded with sample students and results!")

if __name__ == '__main__':
    seed()
