web: gunicorn quiz.wsgi
web: python manage.py migrate
web: python manage.py collectstatic --noinput
heroku ps:scale web=1
