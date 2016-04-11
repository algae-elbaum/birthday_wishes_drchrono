# Birthday Wishes
A mini project for my application to drchrono

This project will provide a UI to doctors which will allow them to set up
automatic birthday messages for their patients

Currently being hosted (intermittently) on [gaster.caltech.edu](http://gaster.caltech.edu)

Dependencies:
django
pytz
requests
sqlite
schedule

To start the dev server:
`python manage.py runserver`
To start the mail sending service:
`python manage.py message_processor`
