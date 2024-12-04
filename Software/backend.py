from flask import Flask, render_template_string,render_template, request, redirect, flash
import sqlite3
from pyngrok import ngrok
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'babajoshyy'

def start_ngrok():
    ngrok.set_auth_token("2nt4sbxbYvteJM8mNiekzt27N7t_EsLGnKU4sLVHX5iSdUh7")
    public_url = ngrok.connect(5000).public_url
    print(f" * Web app available at: {public_url}")
    return public_url

# Database connection
def get_db_connection():
    connection = sqlite3.connect('Logins.db')
    connection.row_factory = sqlite3.Row
    return connection

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
#Function to login
def login():
    username = request.form['user']
    password = request.form['pass']
    
    connection = get_db_connection()
    user = connection.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    connection.close()
    
    if user and check_password_hash(user['hashpassword'], password):
        return f'Welcome {username}!'
    else:
        flash('Invalid credentials!')
        return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
#Function to login
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        hashed_password = generate_password_hash(password, method='sha256')
        
        connection = get_db_connection()
        try:
            connection.execute('INSERT INTO users (username, hashpassword) VALUES (?, ?)', 
                         (username, hashed_password))
            connection.commit()
            connection.close()
            flash('User registered successfully!')
            return redirect('/')
        except sqlite3.IntegrityError:
            flash('Username already exists!')
            connection.close()
            return redirect('/register')
    return render_template('register.html')

if __name__ == '__main__':
    start_ngrok()
    app.run(port=5000)
