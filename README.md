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
