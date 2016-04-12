# Birthday Wishes
A mini project for my application to drchrono

Provides a UI to doctors which will allow them to set up automatic birthday messages for their patients

Currently being hosted (intermittently) on [gaster.caltech.edu](http://gaster.caltech.edu)

Dependencies [(p) indicates a python package]:
* django  
* sqlite  
* pytz (p)  
* requests (p)  
* schedule (p)  


To start the dev server:  
`python manage.py runserver`  
To start the periodic jobs (mail sending and authorization refreshing):  
`python manage.py periodic_jobs`  

Additionally, you'll need to set up an email service and hook it into django by telling django the username and password of the email that the birthday messages should come from. After that, uncomment a couple lines in birthday_wishes_app/management/commands/periodic_jobs.py and you should be ready to go.

Currently birthday texts are not supported, as I don't think that would be a good feature. I would be uncomfortable with my doctor sending me automated birthday texts. However, if it's desired I can certainly add support for it. Anyone interested in this probably already has access to my email, so just shoot me a message if you want me to do so. If implemented, just as with email, you'd have to set up the text sending mechanics yourself.
