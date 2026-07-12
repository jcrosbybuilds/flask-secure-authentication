"""

Name: Jacob Crosby
Date: 7/6/2025
Purpose: Week 8 Lab Assignment

"""


# Import Libraries

import csv
import logging
from datetime import datetime
import re
from flask import Flask, render_template, request, redirect, url_for, session, flash
from passlib.hash import sha256_crypt

PASSWORD_FILE = 'password_file.txt'

app = Flask(__name__)

app.secret_key = 'your-secret-key'

users = {}  # Storing users


logging.basicConfig(filename='failed_logins.log', level=logging.WARNING,
                    format='%(asctime)s - %(message)s')


def password_valid(password):
    """ Function to validate password based on defined parameters """
    if (len(password) >= 12 and
        re.search(r'[A-Z]', password) and
        re.search(r'[a-z]', password) and
        re.search(r'\d', password) and
        re.search(r'[!@#$%^&*(),.?":{}|<>]', password)):
        return True
    return False


def is_common_password(password):
    """ Function to check if the updated password contains any elements of commonly known
    passwords"""

    try:
        with open('common_password.txt', 'r') as file:
            common_passwords = set(p.strip().lower() for p in file if p.strip())

        password_lower = password.lower()

        if password_lower in common_passwords:
            return "Password is on the list of common passwords."

        for common in common_passwords:
            if common in password_lower:
                return f"Your password contains a common word: '{common}'."

        return None  # No common password issues found

    except FileNotFoundError:
        print("CommonPassword.txt not found.")
        return None


@app.route("/")
def home():
    """ Renders the Home page for website """
    if 'user' not in session:
        return redirect(url_for('login'))
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template("home.html", time=current_time)


@app.route("/about")
def about():
    """ Renders the About page for website """
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("about.html")


@app.route("/contact")
def contact():
    """ Renders the Contact page for the website"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template("contact.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Function calls the register.html template and processes registration requests by
     validating that input meets required standards. """
    if request.method == 'GET':  # get / render the registration page for the user
        return render_template('register.html', style='home', pagename='Registration')

    username = request.form['username']
    password = request.form['password']


    if len(username) < 4:
        flash("Username must be at least 4 characters.")
        return render_template('register.html', style='home', pagename='Registration')

    if get_password_if_registered(username) is not None:
        flash("Username already exists.")
        return render_template('register.html', style='home', pagename='Registration')

    if not password_valid(request.form['password']):  # Enforce password complexity
        flash("Password must be at least 12 characters and include uppercase, lowercase, number, "
              "and special character.")
        return render_template('register.html', style='home', pagename='Registration')

    write_user_to_file(username, password)
    flash("Registration successful! Please log in.")
    return redirect(url_for('login'))


def get_password_if_registered(username_input):
    """ Check if the given username does not already exist in our password file
    return none of the username does not exist; otherwise return the password for that user """
    try:
        with open(PASSWORD_FILE, 'r') as users_file:
            reader = csv.reader(users_file)
            for row in reader:
                if len(row) != 2:
                    continue
                username, pass_hash = row
                if username == username_input:
                    return pass_hash

    except FileNotFoundError as e:
        print("File not found:", e)
        return None

    except Exception as e:
        print("No permissions to open this file or data in it not in correct format:", e)
        return None
    return None


def write_user_to_file(username, password):
    """ Write given username and password to the password file """
    pass_hash = sha256_crypt.hash(password) #encrypt password before storing to file
    try: # Add account info to account database
        with open(PASSWORD_FILE, 'a', newline='') as pass_file:
            writer = csv.writer(pass_file)
            writer.writerow([username, pass_hash])
        return redirect(url_for('register'))
    except FileNotFoundError as e:
        print("Could not find file called " + PASSWORD_FILE)
        print(e.args) #all info about the error printed to the server for support to see/debug
        flash("Account database error. Try again later or contact support.")
        return redirect(url_for('register'))
    except Exception as e:
        print("Could not append to file " + PASSWORD_FILE)
        print(e.args) #all info about the error printed to the server for support to see/debug
        flash("Account database error. Try again later or contact support.")
        return redirect(url_for('register'))


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login Function """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        stored_hash = get_password_if_registered(username)
        if stored_hash and sha256_crypt.verify(password, stored_hash):
            session['user'] = username
            return redirect(url_for('home'))

        ip_address = request.remote_addr
        logging.warning(f"Failed login attempt for user '{username}' from IP {ip_address}")
        flash("Invalid credentials.")

    return render_template("login.html")

@app.route("/logout")
def logout():
    """ Logout Function """
    session.pop('user', None)
    flash("You have been logged out.")
    return redirect(url_for("login"))


@app.route("/update_password", methods=["GET", "POST"])
def update_password():
    """ Allows registered users to change their passwords """
    if 'user' not in session:
        flash("You must be logged in to update your password.")
        return redirect(url_for("login"))

    if request.method == "POST":
        current_user = session['user']
        old_password = request.form["old_password"]
        new_password = request.form["new_password"]

        stored_hash = get_password_if_registered(current_user)
        if not sha256_crypt.verify(old_password, stored_hash):
            flash("Old password is incorrect.")
            return render_template("update_password.html")

        if not password_valid(new_password):
            flash("New password does not meet complexity requirements.")
            return render_template("update_password.html")

        common_issue = is_common_password(new_password)
        if common_issue:
            flash(common_issue)
            return render_template("update_password.html")

        update_user_password(current_user, new_password)
        flash("Password updated successfully.")
        return redirect(url_for("home"))

    return render_template("update_password.html")


def update_user_password(username, new_password):
    """Replace user's old password with a new one"""
    pass_hash = sha256_crypt.hash(new_password)
    updated = False
    rows = []

    try:
        with open(PASSWORD_FILE, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == username:
                    rows.append([username, pass_hash])
                    updated = True
                else:
                    rows.append(row)

        with open(PASSWORD_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)
        return updated
    except Exception as e:
        print("Error updating password:", e)
        flash("Could not update password. Please try again.")
        return False


if __name__ == "__main__":
    app.run()
