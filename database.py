
import sqlite3

DB_NAME = "studysphere.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # SUBJECTS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS subjects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            teacher TEXT
        )
    """)

    # TASKS TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject_id INTEGER,
            deadline TEXT,
            priority TEXT,
            status TEXT DEFAULT 'Pending',
            FOREIGN KEY (subject_id) REFERENCES subjects(id)
        )
    """)

    # CHECK OLD TIMETABLE TABLE
    cursor.execute("PRAGMA table_info(timetable)")
    existing_columns = [row[1] for row in cursor.fetchall()]

    required_columns = {
        "id", "day", "subject", "start_time", "end_time"
    }

    if existing_columns and not required_columns.issubset(set(existing_columns)):
        cursor.execute("DROP TABLE IF EXISTS timetable_old")
        cursor.execute("ALTER TABLE timetable RENAME TO timetable_old")

    # TIMETABLE TABLE
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS timetable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            day TEXT NOT NULL,
            subject TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- SUBJECT FUNCTIONS ----------------

def add_subject(name, teacher):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO subjects (name, teacher) VALUES (?, ?)",
        (name, teacher)
    )

    conn.commit()
    conn.close()


def get_subjects():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects ORDER BY name")

    subjects = cursor.fetchall()
    conn.close()

    return subjects


def delete_subject(subject_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE subject_id = ?",
        (subject_id,)
    )

    cursor.execute(
        "DELETE FROM subjects WHERE id = ?",
        (subject_id,)
    )

    conn.commit()
    conn.close()


# ---------------- TASK FUNCTIONS ----------------

def add_task(title, subject_id, deadline, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tasks
        (title, subject_id, deadline, priority)
        VALUES (?, ?, ?, ?)
    """, (title, subject_id, deadline, priority))

    conn.commit()
    conn.close()


def get_tasks():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tasks.id,
            tasks.title,
            subjects.name,
            tasks.deadline,
            tasks.priority,
            tasks.status
        FROM tasks
        LEFT JOIN subjects
        ON tasks.subject_id = subjects.id
        ORDER BY tasks.deadline
    """)

    tasks = cursor.fetchall()
    conn.close()

    return tasks


def update_task_status(task_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )

    conn.commit()
    conn.close()


def delete_task(task_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,)
    )

    conn.commit()
    conn.close()


# ---------------- TIMETABLE FUNCTIONS ----------------

def add_timetable(day, subject, start_time, end_time):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO timetable
        (day, subject, start_time, end_time)
        VALUES (?, ?, ?, ?)
    """, (day, subject, start_time, end_time))

    conn.commit()
    conn.close()


def get_timetable():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, day, subject, start_time, end_time
        FROM timetable
        ORDER BY
            CASE day
                WHEN 'Monday' THEN 1
                WHEN 'Tuesday' THEN 2
                WHEN 'Wednesday' THEN 3
                WHEN 'Thursday' THEN 4
                WHEN 'Friday' THEN 5
                WHEN 'Saturday' THEN 6
                WHEN 'Sunday' THEN 7
                ELSE 8
            END,
            start_time
    """)

    timetable = cursor.fetchall()
    conn.close()

    return timetable


def delete_timetable(entry_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM timetable WHERE id = ?",
        (entry_id,)
    )

    conn.commit()
    conn.close()


# ---------------- NOTES TABLE ----------------

def create_notes_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_note(title, subject, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO notes (title, subject, content, created_at)
        VALUES (?, ?, ?, datetime('now'))
    """, (title, subject, content))

    conn.commit()
    conn.close()


def get_notes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, subject, content, created_at
        FROM notes
        ORDER BY id DESC
    """)

    notes = cursor.fetchall()
    conn.close()

    return notes


def update_note(note_id, title, subject, content):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE notes
        SET title = ?, subject = ?, content = ?
        WHERE id = ?
    """, (title, subject, content, note_id))

    conn.commit()
    conn.close()


def delete_note(note_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )

    conn.commit()
    conn.close()


create_notes_table()

# CREATE DATABASE TABLES
init_db()
