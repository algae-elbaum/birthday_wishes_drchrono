from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from birthday_wishes_app.models import Patient, Doctor
import time, datetime, schedule

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
    for m in messages:
        # It would be really bad to require doctors to give their email
        # authentication to this site, so instead the messages will be
        # sent from the unfortunately less personal email of the server
        # NOTE: This won't actually work until the server gets an smtp
        # server
        try:
#               send_mail(m.subject, 
#                         m.message, 
#                         SERVER_EMAIL, 
#                         [m.email], 
#                         fail_silently=False)
#               send_mail('Birthday message sent to ' + m.name, 
#                         'message was:\n' + m.message, 
#                         SERVER_EMAIL, 
#                         [m.doctor.user.email], 
#                         fail_silently=False)
#               If there's to be a text message as well, that would also go here
            print 'Pretending to send message to', m.name
            print 'Subject:', m.subject
            print 'Message:', m.message
            print '\n'
        except:
            print 'Failed to send message to', m.name 

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


