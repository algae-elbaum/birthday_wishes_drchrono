import os
import django
from django.core.management import call_command, get_commands

# Just call the management command. Need to do this in a script to keep Heroku
# happy.
os.environ['DJANGO_SETTINGS_MODULE'] = 'birthday_wishes.settings'
django.setup()
call_command('periodic_jobs')
