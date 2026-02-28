# Student Interactive System

A production-ready Django web application with quizzes, authentication, leaderboard, and a study-help chatbot.

## Features
- Quiz module with question explanations, difficulty filter, and timed progression.
- Authentication (register/login/logout) with protected quiz access.
- Personal quiz attempt history.
- Leaderboard of top 10 users by best score percentage.
- AJAX-based rule chatbot for core study topics.
- Bootstrap 5 responsive UI with reusable base template.
- Django admin support for Question and Score management.

## Project Structure
- `student_system/` – Django project settings and root URLs.
- `quiz_app/` – quiz feature app (`models.py`, `views.py`, `forms.py`, `urls.py`, templates, static assets).
- `templates/registration/` – auth templates.

## Setup & Run
1. Create a virtual environment and activate it.
2. Install dependencies:
   ```bash
   pip install django
   ```
3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Create an admin account (optional):
   ```bash
   python manage.py createsuperuser
   ```
5. Start server:
   ```bash
   python manage.py runserver
   ```
6. Visit: `http://127.0.0.1:8000/`

## Admin Usage
- Login to `/admin/`
- Add/edit/delete `Question` entries.
- Review `Score` records.
