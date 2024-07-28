import mysql.connector
import bcrypt
from database.stock_database import connect_db


def create_user(username, email, password):
    conn, cursor = connect_db()

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute('INSERT INTO users (username, password, email) VALUES (%s, %s, %s)',
                       (username, hashed_password.decode('utf-8'), email))
        conn.commit()
        return True
    except mysql.connector.IntegrityError:
        # Handle the case when the username or email is not unique
        return False
    finally:
        conn.close()


def get_stored_password(username):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='Stock'
    )
    cursor = conn.cursor()

    # Execute the SQL query to retrieve the hashed password
    cursor.execute('SELECT password FROM users WHERE username = %s', (username,))

    # Fetch the result
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]  # The first column of the result is the password hash
    else:
        return None  # User not found


def authenticate_user(username, password):
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='Stock'
    )
    cursor = conn.cursor()

    stored_password = get_stored_password(username)

    if stored_password:
        if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
            return True  # Passwords match, user is authenticated
        else:
            return False  # Passwords do not match
    else:
        return False  # User not found
