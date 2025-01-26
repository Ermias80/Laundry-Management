from flask import Flask, render_template, request, redirect, url_for, flash, session
from dotenv import load_dotenv
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder='template', static_folder='static')
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# SQLTools Connection Configuration
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'Laundery_managemen7'),
            port=int(os.getenv('DB_PORT', 3306))
        )
        return conn
    except mysql.connector.Error as e:
        print("Error connecting to MySQL: {}".format(e))
        return None
# Routes
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
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        # Input validation
        if not all([first_name, last_name, email, password]):
            flash('All fields are required.', 'error')
            return render_template('sign_up.html')

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', 'error')
            return render_template('sign_up.html')

        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'[0-9]', password):
            flash('Password must be at least 8 characters long and include at least one uppercase letter and one number.', 'error')
            return render_template('sign_up.html')

        hashed_password = generate_password_hash(password)

        # Database interaction
        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed.', 'error')
                return render_template('sign_up.html')

            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)",
                (first_name, last_name, email, hashed_password)
            )
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email is already registered. Please log in.', 'error')
        except mysql.connector.Error as e:
            flash("An error occurred: {}".format(str(e)), 'error')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template('sign_up.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            conn = get_db_connection()
            if not conn:
                flash('Database connection failed.', 'error')
                return render_template('sign_in.html')

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and check_password_hash(user['password'], password):
                # Set session
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                flash('Login successful!', 'success')
                return redirect(url_for('order_page'))
            else:
                flash('Invalid email or password.', 'error')
        except mysql.connector.Error as e:
                flash("An error occurred: {}".format(str(e)), 'error')
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()

    return render_template('sign_in.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('login'))

@app.route('/order_page')
def order_page():
    if 'user_email' not in session:
        flash('Please log in to access the order page.', 'error')
        return redirect(url_for('login'))
    return render_template('order_page.html', user_email=session['user_email'])

if __name__ == '__main__':
    app.run(debug=True)
