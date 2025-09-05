from flask import Flask, request, render_template, redirect, url_for, session, flash
import numpy as np
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from feature import FeatureExtraction
import pickle
import warnings

warnings.filterwarnings('ignore')

# Load the pre-trained model
gbc = pickle.load(open("pickle/model.pkl", "rb"))

app = Flask(__name__)
app.secret_key = 'b8d7f2e7c438417faef98485b7c3c4f9'  # Set your secret key

# Initialize user database if not exists
def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

init_db()

# Make 'session' available in all templates
@app.context_processor
def inject_session():
    return dict(session=session)

@app.route('/', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        flash('Please login to continue.', 'warning')
        return redirect(url_for('login'))

    prediction = -1
    url = None
    if request.method == "POST":
        url = request.form.get("url", "")
        obj = FeatureExtraction(url)
        x = np.array(obj.getFeaturesList()).reshape(1, 30)

        y_pred = gbc.predict(x)[0]
        y_pro_non_phishing = gbc.predict_proba(x)[0, 1]
        prediction = round(y_pro_non_phishing, 2)

    return render_template("index.html", xx=prediction, url=url)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Please enter both username and password.', 'warning')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)

        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
            flash('Registration successful. Please login.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        with sqlite3.connect('users.db') as conn:
            cursor = conn.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()

            if user and check_password_hash(user[2], password):
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash('Login successful!', 'success')
                return redirect(url_for('predict'))
            else:
                flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
