web: gunicorn birthday_wishes.wsgi --log-file -
worker: python birthday_wishes_app/management/commands/periodic_jobs.py
