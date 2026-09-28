# Smart Attendance Management System

A simple, college-ready web application for managing student attendance, built with **Python, Flask, HTML, CSS and SQLite**.

## Features

- Add and delete students
- Mark students Present/Absent for a selected date
- Update attendance for an existing date
- Automatically calculate overall attendance
- Student-wise attendance report
- Responsive interface for desktop and mobile
- SQLite database created automatically
- Health-check endpoint for deployment
- Production server configuration with Gunicorn

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| Frontend | HTML + CSS |
| Database | SQLite |
| Production server | Gunicorn |

## Project Structure

```text
Smart-Attendance-Management-System/
├── app.py
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
├── templates/
│   ├── index.html
│   └── report.html
└── static/
    └── style.css
```

## Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/Smart-Attendance-Management-System.git
cd Smart-Attendance-Management-System
```

### 2. Create a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open `http://127.0.0.1:5000` in your browser.

The `attendance.db` SQLite file is generated automatically and is intentionally ignored by Git.

## Deployment

The included `Procfile` is compatible with platforms that support Gunicorn. Set a secure `SECRET_KEY` environment variable before deploying. For persistent production data, use a managed database instead of local SQLite storage.

## Main Routes

- `/` — dashboard and attendance marking
- `/report` — attendance report
- `/health` — health check

## Project Description

**Smart Attendance Management System** is a web-based application designed to reduce manual attendance work. Teachers can maintain a student list, record attendance by date, and view calculated attendance percentages through a simple interface.

## Future Scope

- Teacher/student authentication
- QR-code attendance
- CSV/PDF report export
- Low-attendance notifications
- PostgreSQL/MySQL support
- Role-based access control

## Author

**Prasun Bagde**

> Update this section with your GitHub profile URL after creating the repository.
