# Birthday Wishes
A mini project for my application to drchrono

Provides a UI to doctors which will allow them to set up automatic birthday 
messages for their patients

Currently being hosted (intermittently) on [gaster.caltech.edu](http://gaster.caltech.edu)

To set up, you will need to run your own database and configure the app to use
it. It is currently configured to use sqlite

Additionally, you'll want to modify the settings to use your own email settings.
For ease of drchrono devs reviewing this, the account currently in the settings
is a real account. In practice I certainly wouldn't put the username and password
of the account used for dev in a public repo.

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
