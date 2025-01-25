from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import os


app = Flask(__name__, template_folder='template')
app.secret_key = ''
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')


# MySQL Configuration
db_config = {
    'host': 'localhost',       # Change if your MySQL server is on another host
    'user': 'root',   # Your MySQL username
    'password': 'S12345s?',  # Your MySQL password
    'database': 'E5'        # Database name
}

# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
     return render_template("index.html")

@app.route('/about')
def about():
    return render_template('about.html')
 
@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/admin')
def admin():
    return render_template('Admin.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Retrieve form data
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate input
        if not all([first_name, last_name, email, password]):
            flash('All fields are required.', 'error')
            return render_template('sign_up.html')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', 'error')
            return render_template('sign_up.html')

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            flash('Password must be at least 8 characters long and include at least one uppercase letter and one number.', 'error')
            return render_template('sign_up.html')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Save to database
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, hashed_password)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            
            # Redirect to login form after registration
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email is already registered. Please log in.', 'error')
        except mysql.connector.Error as e:
            flash(f"An error occurred: {str(e)}", 'error')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()
    # Render the registration page
    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'error')

    return render_template('sign_in.html')

@app.route('/order_page')
def dashboard():
    return render_template('order_page.html')

if __name__ == '__main__':
    app.run(debug=True)