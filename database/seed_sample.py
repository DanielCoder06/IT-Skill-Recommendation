import sqlite3


connection = sqlite3.connect("data/it_jobs.db")

cursor = connection.cursor()

cursor.execute("""
    INSERT INTO companies (name, address)
    VALUES (?, ?)
""", ("FPT Software", "Cần Thơ"))


company_id = cursor.lastrowid


cursor.execute("""
    INSERT INTO locations (city, district, address)
    VALUES (?, ?, ?)
""", ("Cần Thơ", "Ninh Kiều", "Cần Thơ"))


location_id = cursor.lastrowid


cursor.execute("""
    INSERT INTO jobs
    (title, company_id, location_id, jd_raw, job_url, experience)
    VALUES (?, ?, ?, ?, ?, ?)
""", (
    "Python Intern",
    company_id,
    location_id,
    """
    Tuyển Intern Python Developer.

    Yêu cầu:
    - Biết Python và SQL
    - Sử dụng Git và GitHub
    - Có kiến thức Machine Learning
    - Có khả năng giao tiếp tiếng Anh
    - Làm việc nhóm tốt
    """,
    "https://example.com/python-intern-001",
    "Dưới 1 năm"
))


job_id = cursor.lastrowid

connection.commit()
connection.close()

print("Đã tạo job mẫu:", job_id)