-- ==============================================================================
-- Student Result Management System - Database Schema
-- Remote MySQL Database Definition
-- ==============================================================================

-- 1. Users Table (System administrators and faculty)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) DEFAULT 'admin',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Students Table
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id VARCHAR(30) NOT NULL UNIQUE,
    roll_number VARCHAR(30) NOT NULL UNIQUE,
    student_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone_number VARCHAR(20),
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    date_of_birth DATE,
    department VARCHAR(100) NOT NULL,
    course VARCHAR(50) NOT NULL,
    semester INT NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_roll (roll_number),
    INDEX idx_name (student_name),
    INDEX idx_dept (department),
    INDEX idx_sem (semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Subjects Table
CREATE TABLE IF NOT EXISTS subjects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_code VARCHAR(20) NOT NULL UNIQUE,
    subject_name VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    semester INT NOT NULL,
    max_marks INT DEFAULT 100,
    pass_marks INT DEFAULT 40,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_sub_sem (semester),
    INDEX idx_sub_dept (department)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Examinations Table
CREATE TABLE IF NOT EXISTS examinations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    exam_name VARCHAR(100) NOT NULL,
    semester INT NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    exam_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Results Table
CREATE TABLE IF NOT EXISTS results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    exam_id INT NOT NULL,
    marks_obtained DECIMAL(5,2) NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL DEFAULT 100.00,
    percentage DECIMAL(5,2) NOT NULL,
    grade VARCHAR(5) NOT NULL,
    status ENUM('Pass', 'Fail') NOT NULL,
    remarks VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE,
    FOREIGN KEY (exam_id) REFERENCES examinations(id) ON DELETE CASCADE,
    UNIQUE KEY unique_student_subject_exam (student_id, subject_id, exam_id),
    INDEX idx_res_status (status),
    INDEX idx_res_student (student_id),
    INDEX idx_res_exam (exam_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Initial default subjects for Computer Science (Semester 5 & 6)
INSERT IGNORE INTO subjects (subject_code, subject_name, department, semester, max_marks, pass_marks) VALUES
('CS501', 'Database Management Systems', 'Computer Science and Engineering', 5, 100, 40),
('CS502', 'Operating Systems', 'Computer Science and Engineering', 5, 100, 40),
('CS503', 'Computer Networks', 'Computer Science and Engineering', 5, 100, 40),
('CS504', 'Software Engineering', 'Computer Science and Engineering', 5, 100, 40),
('CS505', 'Web Technologies Lab', 'Computer Science and Engineering', 5, 100, 40),
('CS601', 'Artificial Intelligence', 'Computer Science and Engineering', 6, 100, 40),
('CS602', 'Compiler Design', 'Computer Science and Engineering', 6, 100, 40),
('CS603', 'Cloud Computing', 'Computer Science and Engineering', 6, 100, 40);

-- Initial default examination
INSERT IGNORE INTO examinations (id, exam_name, semester, academic_year, exam_date) VALUES
(1, 'End Semester Examination Nov-Dec 2025', 5, '2025-2026', '2025-11-20'),
(2, 'Mid Term Examination 2025', 5, '2025-2026', '2025-09-15');

