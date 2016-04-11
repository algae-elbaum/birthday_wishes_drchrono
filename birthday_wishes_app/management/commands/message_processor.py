from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from birthday_wishes_app.models import Patient
import time, datetime

# If there were even a little bit more scheduling that needed to be done in this app,
# or any dreams of extensibility, I would switch to something like celery/redis to
# do the scheduled and asynchronous jobs. However, since those conditions aren't
# satisfied, this is a really simple way of getting the messages sent.

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
        # NOTE: This won't actually work until the server gets a smtp
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


class Command(BaseCommand):
    help = "Daily sends all active birthday messages for the day"

    def handle(self, *args, **options):
        while 1:
            # Sleep until the next 31 minute mark. This will not be very accurate,
            # however it will never drift significantly from sending at the 31
            # minute mark of every hour
            minutes_to_sleep = 30 - datetime.datetime.now().minute
            if minutes_to_sleep < 0:
                minutes_to_sleep = 90 - datetime.datetime.now().minute
            # Add one to make sure we always pass the half hour mark (else could
            # accidentally repeat sending a message)
            sleep(60 * (minutes_to_sleep + 1))

            send_messages()
            


