import mysql.connector


def connect_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='Stock'
    )
    cursor = conn.cursor()
    return conn, cursor


def create_signup_table(conn, cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL UNIQUE,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL
        )
    ''')
    conn.commit()


def register_user(conn, cursor, username, password, email):
    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        conn.commit()
        return True  # Registration successful
    except mysql.IntegrityError:
        return False  # User with the same username or email already exists


def login_user(conn, cursor, username, password):
    cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    if user:
        return True  # Login successful
    else:
        return False  # Invalid username or password
