from flask import Flask, render_template, request, redirect, url_for, session
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)
app.secret_key = "cookiesnkream"

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('/Users/darryl/Documents/minderwebsite/js/minder-394816-f462324e6b0b.json', scope)
client = gspread.authorize(credentials)
spreadsheet = client.open('patients')
worksheet = spreadsheet.get_worksheet(0) 

@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_error = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if username and password match a row in the Google Sheet
        user_data = worksheet.get_all_records()
        for user in user_data:
            if user['Username'] == username and user['Password'] == password:
                session['username'] = username
                return redirect(url_for('main_page'))
        
        login_error = "The Username or Password you've entered doesn't match any account."

    return render_template('login_signup.html', login_error=login_error)

@app.route('/signup', methods=['POST'])
def signup():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    new_username = request.form['new_username']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']

    signup_error = None

    if new_password != confirm_password:
        signup_error = "Passwords do not match. Please try again"
        return render_template('login_signup.html', signup_error=signup_error)


    # Append new user data to the Google Sheet
    new_user_data = [first_name, last_name, email, new_username, new_password]
    worksheet.append_row(new_user_data)

    session['username'] = new_username
    return redirect(url_for('main_page'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/main_page')
def main_page():
    if 'username' in session:
        return render_template('main_page.html')
    return redirect(url_for('login'))

@app.route('/add_device')
def add_device():
    if 'username' in session:
        return render_template('add_device.html')
    return redirect(url_for('login'))

@app.route('/download')
def download():
    if 'username' in session:
        return render_template('download.html')
    return redirect(url_for('login'))

@app.route('/update_info')
def update_info():
    if 'username' in session:
        return render_template('update_info.html')
    return redirect(url_for('login'))

@app.route('/contact_us')
def contact_us():
    if 'username' in session:
        return render_template('contact_us.html')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
