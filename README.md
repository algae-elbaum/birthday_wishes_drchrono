# Birthday Wishes
A mini project for my application to drchrono

Provides a UI to doctors which will allow them to set up automatic birthday 
messages for their patients

Currently being hosted (intermittently) on [birthday-wishes.herokuapp.com/](https://birthday-wishes.herokuapp.com/)

(Note: The Heroku app will not actually send the birthday messages. Scaling the
 number of worker processes to be greater than 0 made Heroku ask for my credit
 card number, which I was not willing to give for this project. A dev instance,
 on the other hand, will send the emails)


To set up your own instance of this, you will need to run your own database and 
configure the app to use it. It is currently configured to use postgresql. 

Additionally, you'll want to modify the settings to use your own email settings.
In case it happens to be useful for anyone reviewing this, the account currently
in settings.py is a real account.

(I know I've kept the dev username and password for the database and the email
 in settings.py. In practice I of course wouldn't put the actual dev username
 and password of anything in a public git repo, but here the accounts are just
 one off things, so it's not a problem to ignore it and avoid making committing
 changes to settings.py more complex.)


To run this in a local dev environment, you should add the appropriate entry to
ALLOWED_HOSTS and set the values in birthday_wishes_app/globs.py to the values
you want. (Currently that file holds the client secret of this app. Again, this
would be a BAD_THING<sup>tm</sup> if this weren't a one off project, in which case
I would be more cautious. So too for the SECRET_KEY in settings.py). You should
set DEBUG to True if you want the css to work.

To start the dev server:  
`python manage.py runserver`  
To start the periodic jobs (mail sending and authorization refreshing):  
`python manage.py periodic_jobs`


Currently birthday texts are not supported, as I don't think that would be a good
feature. I would be uncomfortable with my doctor sending me automated birthday
texts. However, if it's desired I can certainly add support for it. Anyone
interested in this probably already has access to my email, so just shoot me a
message if you want me to do so. If implemented, just as with email, you'd have
to set up the text sending mechanics yourself.
