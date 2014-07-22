smirik
======

test task for https://gist.github.com/smirik/09a2469ff2d443a0d9c2

## Installing

run this commands:
+ virtualenv -p python3 smirik
+ source smirik/bin/activate
+ cd smirik
+ `git clone git@github.com:dicos/smirik.git`
+ cd smirik
+ pip install -r requirements.pip
+ cd smirik
+ python manage.py syncdb
+ python manage.py get\_data
+ python manage.py runserver


##How to create new user
+ go to http://localhost:8000/admin/auth/negotiablepaper/ and add some tickers from https://www.google.com/finance#stockscreener (for example 'IBM', 'MSF')
+ go to http://localhost:8000/admin/auth/client/ and click to your user
+ in profile page select "negotiable papers" and write first\_name and last\_name
+ go to http://localhost:8000/ where you can see plot "portfolio vs time" and table "portfolio by month"


##Testing
run command python manage.py test


## Time control:
- 0.5 hour for find library, design and initialization project
- 1 hour for create command "python manage.py get\_data". It's command for load data from yahoo finance service intto local database;
- 0.25 hour write test  python manage.py test plot.tests.Cases.test\_load\_data
- 0.25 hour for create structure project
- 1 hours test plot image with JavaScript libraries. Decline becouse need more time if many data render
- 3 hours learning libraries pandas, matplotlib, numpy
- 2 hours plotting imager "portfolio vs time"
- 1 hours create report "portfolio by months"
*total time:* 9 hours
