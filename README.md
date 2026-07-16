# Flask Secure Authentication

---

A Flask web application that demonstrates secure user authentication, password management, 
session handling, and access control using Passlib for password hashing. The project was designed 
around a private music studio to illustrate how authentication features can be integrated into a small business website.

![Python](https://img.shields.io/badge/Python-3-blue)
![Flask](https://img.shields.io/badge/Flask-Web_Framework-lightgrey)
![Security](https://img.shields.io/badge/Security-Authentication-green)
![Git](https://img.shields.io/badge/Git-Version_Control-orange)

## Overview

---
This project demonstrates the implementation of secure authentication features within a Flask web application. Users can register new accounts, securely log in, update passwords, and access protected pages while following common authentication and password security practices.

The application is presented as a private music studio website, illustrating how authentication can be incorporated into a real-world small business scenario.

## Features

---
- User registration
- Secure login and logout
- Password hashing
- Password complexity enforcement
- Common password detection
- Password update functionality
- Session-based authentication
- Protected routes
- Flash messaging
- Failed login logging

## Security Features

- Passwords are securely hashed before storage.
- Password complexity requirements help enforce stronger credentials.
- Common passwords are rejected to improve account security.
- Failed login attempts are recorded for auditing purposes.
- User sessions protect authenticated resources.

## Technologies

This project was developed using the following technologies:
- Python
- Flask
- Passlib
- Jinja2
- HTML5
- CSS3
- Git

## Screenshots

### Login

![Login](screenshots/login.png)

### Register

![Register](screenshots/register.png)

### Home

![Home](screenshots/homepage.png)

### Update Password

![Update Password](screenshots/update_password.png)

## Testing

---
The application was manually tested to verify functionality, HTML structure, navigation, and project organization. All required features were successfully validated.

### Test Scenarios

- Dynamic date and time display updates without restarting the application
- Navigation between Home, About, and Contact pages using Flask routing
- Proper rendering of templates using `render_template()`
- HTML semantic elements including headings, paragraphs, comments, ordered lists, and unordered lists
- External resource links open correctly in a new browser tab
- Flask project structure follows recommended organization (`templates/` and `static/` directories)
- Static assets and page styling load correctly across all pages

### Code Quality

The project was analyzed using **Pylint**. After improving documentation, import organization, and formatting, the application achieved a perfect score of:

**10.00 / 10.00**

### Result

All functional and structural tests passed successfully.

## Installation

---
### Clone the repository

```bash
git clone https://github.com/jcrosbybuilds/flask-secure-authentication.git
```

### Navigate to the project

```bash
cd flask-secure-authentication
```

### Create a virtual environment (recommended)

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

## Project Structure

---
```text
flask-secure-authentication/
├── app.py
├── common_password.txt
├── requirements.txt
├── README.md
├── .gitignore
├── screenshots/
├── static/
└── templates/
```

## What I Learned

---
This project strengthened my understanding of:

- Building secure web applications with Flask
- Implementing session-based authentication
- Applying password hashing and validation techniques
- Protecting application routes from unauthorized access
- Logging authentication events for auditing
- Organizing a Flask project for maintainability
- Using Git and GitHub to manage project development

## Future Improvements

---
Potential enhancements include:

- Store users in a relational database instead of a text file
- Implement email-based password reset
- Add multi-factor authentication
- Strengthen password policy with configurable rules
- Add automated unit tests
- Deploy the application to a cloud platform