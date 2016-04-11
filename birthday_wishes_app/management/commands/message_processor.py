from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from birthday_wishes_app.models import Patient
import schedule, time, datetime

# If there were even a little bit more scheduling that needed to be done in this app,
# or any dreams of extensibility, I would switch to something like celery/redis to
# do the scheduled and asynchronous jobs. However, since those conditions aren't
# satisfied, this is a really simple way of getting the messages sent.

def send_messages():
    print 'Sending messages'
    today = datetime.datetime.now()
    messages = Patient.objects.filter(msg_active=True,
                                      birthday__day=today.day,
                                      birthday__month=today.month).all()
    for m in messages:
        # It would be really bad to require doctors to give their email
        # authentication to this site, so instead the messages will be
        # sent from the unfortunately less personal email of the server
        # (NOTE: This won't actually work unless the appropriate smtp server
        # is set up with the given email and auth
        try:
#               send_mail(m.subject, m.message, 'email@gaster', [m.email], fail_silently=False)
#               send_mail('Birthday message sent to ' + message.name, 
#                          'message was:\n' + m.birthday_message, 
#                         'email@gaster', 
#                         ['doctor@other'], 
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

    # TODO base when a message is sent on the patient's timezone (if one is available)
    # ie let's try to send it around 13:00 instead of 3:00 
    def handle(self, *args, **options):
        schedule.every().day.at('13:00').do(send_messages)
        while 1:
            schedule.run_pending()
            time.sleep(60*60)


