How Tracktivity Pets Works
===========================

Dependencies
-----------------------------

* Ubuntu 14.04 LTS (May work on other operating systems however)
* Python3
* pip3
* Nginx (We used version 1.9)
* mySQL or mariaDB server 
* Python libraries
* django
* fitbit
* django-fitbit
* django-celery
* mysqlclient
* gunicorn
* Virtualenv
* RabbitMQ
* Celery

Installation
-----------------------------

1. Install Ubuntu server and install any updates available.
2. Install python3 - apt-get install python3
3. Install pip3 - apt-get install python3-pip
4. Install virtualenv - pip3 install virtualenv
5. Install the mysql client libraries - apt-get install libmysqlient-dev python3-dev
6. Install mySQL - apt-get install mysql
7. Log into mysql and create a database called “tracktivitypets”
8. Create a mySQL user called “tracktivitypets” with the password “tracktivitypets”
9. The username can be changes in the settings.py of Tracktivity Pets
10. Give the tracktivitypets user all privileges on the tracktivitypets database
11. Create a user called “django” with a default home directory - useradd django
12. Gives the user django a password - passwd django 
13. Create a directory for logs - mkdir /var/log/TracktivityPets
14. Give django ownership of /var/log/TracktivityPets - chown django:django /var/log/TracktivityPets
15. Login as the user - su django
16. cd to the home directory - cd ~
17. Create a Python virtual environment - virtualenv init
18. Copy TracktivityPets folder into the home directory of the user django
19. In the settings.py file, change the hostname or IP address of the database to the location of your database instance (localhost if mysql is installed on the same server)
20. Make sure the django user owns the files and directories within the TracktivityPets directory - chown -R django:django TracktivityPets
21. Activate the Python virtual environment - source ./init/bin/activate
22. Install the following python libraries using pip3:
	
	- django
	- fitbit
	- django-fitbit
	- django-celery
	- mysqlclient
	- gunicorn
	
23. Get django to create the tables in the database - python3 manage makemigrations, python3 manage migrate
24. Load the initial data into the database - python3 manage loaddata initdata.json
25. Install RabbitMQ server - apt-get install rabbitmq-server
26. Install nginx - apt-get install nginx
27. Create a file /etc/nginx/sites-enabled/tracktivitypets.conf
28. Define a server block to communicate to the gunicorn UNIX socket. (Below is an example server block config)
29. Set up gunicorn to run on the servers start-up using Upstart. (Below is an example configuration script)
30. In the settings.py file, you will need to configure the SMTP settings so that they work with your server. This is for the feedback functionality of the application.
	below is an example:
	
	- EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	- EMAIL_USE_TLS = True (Should be True)
	- EMAIL_HOST = 'SMTP HOSTNAME HERE'
	- EMAIL_HOST_USER = 'SMTP USERNAME'
	- EMAIL_HOST_PASSWORD = 'SMTP PASSWORD'
	- EMAIL_PORT = 587

31. In the settings.py, you will also need to change the hostname and Fitbit fields so that they correspond with your details

	- HOST_NAME = "YOUR HOSTNAME HERE"
	
	- FITAPP_CONSUMER_KEY = 'FITBIT CONSUMER KEY HERE'
	- FITAPP_CONSUMER_SECRET = 'FITBIT CONSUMER PRIVATE KEY HERE'
	- FITAPP_SUBSCRIBE = SET TO True FOR SUBSCRIPTION (ASYNC) FITBIT RESULTS 
	- FITAPP_SUBSCRIBER_ID = "FITBIT SUBSCRIBER ID HERE"

Nginx configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: nginx.txt


Gunicorn configuration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. literalinclude:: upstart.txt

