# Birthday Wishes
A mini project for my application to drchrono

Provides a UI to doctors which will allow them to set up automatic birthday 
messages for their patients

Currently being hosted (intermittently) on [birthday-wishes.herokuapp.com/](https://birthday-wishes.herokuapp.com/)


To set up your own instance of this, you will need to run your own database and 
configure the app to use it. It is currently configured to use postgresql. 

Additionally, you'll want to modify the settings to use your own email settings.
In case it happens to be useful for drchrono devs reviewing this, the account 
currently in settings.py is a real account.

(I know I've kept my dev username and password for the database and the email in
 settings.py. In practice I wouldn't put the actual dev username and password of 
 anything in a public git repo, but here the account is just a one off local 
 thing so it's not a problem to ignore it and avoid making committing changes to
 settings.py more complex.)


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
