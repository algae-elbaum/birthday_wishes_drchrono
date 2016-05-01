from django.core.management.base import BaseCommand
from django.core import mail
from birthday_wishes_app.models import Patient, Doctor
import time, datetime, schedule
import sys

# If there were even a little bit more scheduling that needed to be done in this app,
# or any dreams of extensibility, I would switch to something like celery/redis to
# do the scheduled and asynchronous jobs. However, since those conditions aren't
# satisfied, this is a really simple way of getting the messages sent.

# Now that two jobs are happening here, I feel a little uncomfortable keeping the
# scheduling like this rather than using celery. However, this is still fairly
# clean and I don't yet feel like it's even worth it to add all the extra weight 
# of celery and redis to something as small as this

def send_messages():
    print 'Sending messages'
    today = datetime.datetime.now()
    messages = Patient.objects.filter(msg_active=True,
                                      birthday__day=today.day,
                                      birthday__month=today.month,
                                      message_time=today.hour).all()
   
    # NOTE: It would be really bad to require doctors to give their email
    # authentication to this site, so instead the messages will be sent
    # from the unfortunately less personal email of the server. Something
    # that could be done instead is to set up an account for each user on
    # our own smtp server made for this service, eg bob@yaybirth.com
    for m in messages:
        try:
            # If text messages are added, the sending should go here
            with mail.get_connection() as connection:
                mail.EmailMessage(m.subject,           # subject
                                  m.message,           # body
                                  connection.username, # from
                                  [m.email],           # to
                                  connection=connection).send()
                mail.EmailMessage('Birthday message sent to ' + m.name,  # subject
                                  'message was:\n'                       # body
                                        + 'subject:' + m.subject + '\n\n' 
                                        + 'message: ' + m.message, 
                                  connection.username,                   # from
                                  [m.doctor.user.email],                 # to
                                  connection=connection).send()
        except:
            print 'Failed to send message to', m.name
            print 'Error:', sys.exc_info()[0]

def reauthorize():
    for d in Doctor.objects.all():
        try:
            d.refresh_authorization()
        # Ignore errors, the user will be asked to fix it when they next refresh 
        # their patients
        except:
            pass


class Command(BaseCommand):
    help = "Daily sends all active birthday messages for the day"

    def handle(self, *args, **options):
        # Start on the hour
        time.sleep(60 * (60 - datetime.datetime.now().minute))
        schedule.every().hour.do(send_messages)
        schedule.every().day.do(reauthorize)
        while True:
            schedule.run_pending()
            time.sleep(60) 


