import psycopg2

db = psycopg2.connect(
    database='magazin',
    user='postgres',
    host='localhost',
    password='1'
)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS school (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    address TEXT,
    phone_number CHAR(15),
    davlat_maktabi BOOLEAN
);

CREATE TABLE IF NOT EXISTS teacher (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone_number CHAR(15),
    school_id INT REFERENCES school(id)
);

CREATE TABLE IF NOT EXISTS student (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender CHAR(1),
    school_id INT REFERENCES school(id)
);

CREATE TABLE IF NOT EXISTS class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    teacher_id INT REFERENCES teacher(id),
    school_id INT REFERENCES school(id)
);

CREATE TABLE IF NOT EXISTS subject (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    class_id INT REFERENCES class(id),
    teacher_id INT REFERENCES teacher(id)
);

CREATE TABLE IF NOT EXISTS enrollment (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(id),
    class_id INT REFERENCES class(id),
    enrollment_date DATE DEFAULT CURRENT_DATE
);

CREATE TABLE IF NOT EXISTS grade (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(id),
    subject_id INT REFERENCES subject(id),
    grade_value INT,
    date_given TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS attendance (
    id SERIAL PRIMARY KEY,
    student_id INT REFERENCES student(id),
    class_id INT REFERENCES class(id),
    date DATE DEFAULT CURRENT_DATE
);
""")
db.commit()

cursor.execute("INSERT INTO school (name, address, phone_number, davlat_maktabi) VALUES ('1-maktab', 'Toshkent', '123456789', TRUE);")
cursor.execute("INSERT INTO teacher (first_name, last_name, email, phone_number, school_id) VALUES ('Ali', 'Valiyev', 'ali@example.com', '123456789', 1);")
cursor.execute("INSERT INTO student (first_name, last_name, date_of_birth, gender, school_id) VALUES ('Ozod', 'Saidov', '2008-01-01', 'M', 1);")
db.commit()

cursor.execute("SELECT id, TO_CHAR(date_of_birth, 'DD-MM-YYYY') as birth_date FROM student;")
for row in cursor.fetchall():
    print(row)

cursor.execute("ALTER TABLE school RENAME TO maktab;")
cursor.execute("ALTER TABLE teacher RENAME TO oqituvchi;")
db.commit()

cursor.execute("ALTER TABLE student RENAME COLUMN first_name TO ism;")
cursor.execute("ALTER TABLE student RENAME COLUMN last_name TO familiya;")
cursor.execute("ALTER TABLE student RENAME COLUMN gender TO jins;")
db.commit()

cursor.execute("ALTER TABLE student ADD COLUMN grade_level INT;")
cursor.execute("ALTER TABLE teacher ADD COLUMN hire_date DATE;")
db.commit()

cursor.execute("ALTER TABLE attendance DROP COLUMN date;")
db.commit()

cursor.execute("UPDATE student SET first_name = 'Aziz' WHERE id = 1;")
cursor.execute("UPDATE teacher SET last_name = 'Qodirov' WHERE id = 1;")
cursor.execute("UPDATE school SET name = '2-maktab' WHERE id = 1;")
cursor.execute("UPDATE class SET name = '5-A' WHERE id = 1;")
db.commit()

cursor.execute("DELETE FROM student WHERE id = 1;")
cursor.execute("DELETE FROM teacher WHERE id = 1;")
cursor.execute("DELETE FROM school WHERE id = 1;")
cursor.execute("DELETE FROM class WHERE id = 1;")
db.commit()

cursor.close()
db.close()
