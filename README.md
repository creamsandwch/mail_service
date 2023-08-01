## Mail service

Small service that provides mass mailing functionality. You can create or choose an already created template, choose one or many subcribers and plan mailing it to them at future date and time. Frontend done with jquery and ajax with Django MVC project. Containerized in docker, uses PostgreSQL there, so that in ought to launch project locally you must change ```DEBUG_LOCAL``` to ```False``` in ```DJANGO_SETTINGS_MODULE``` (default: ```mail_service/settings.py```).
### Tech stack:
-```Python 2.7```
-```jquery```
-```AJAX```
-```Django 1.11.29```
-```celery 3.1.25```
-```Django REST framework```
-```RabbitMQ```
-```PostgreSQL```

### Launching the project:
To launch project using docker, inside a project folder go to ```infra/``` and prepare a ```.env``` file as in following example:
```
SECRET_KEY=your django secret key

EMAIL_HOST=<your email host>
EMAIL_PORT=<your email port>
EMAIL_USE_TLS="True"
EMAIL_USE_SSL="False"
EMAIL_HOST_USER=<your email address>
EMAIL_HOST_PASSWORD=<check out app passwords in the mail service of choice>

CELERY_BROKER_URL='amqp://host.docker.internal'
CELERY_RESULT_BACKEND='django_celery_fulldbresult.result_backends:DatabaseResultBackend'

# local launch
RABBITMQ_HOST="localhost"
RABBITMQ_PORT="5672"
RABBITMQ_USER="guest"
RABBITMQ_PASSWORD="guest"

C_FORCE_ROOT="True"

DB_ENGINE="django.db.backends.postgresql"
DB_NAME=<your db name>
POSTGRES_USER=<db_username>
POSTGRES_PASSWORD=<db_password>
DB_HOST=<db_host>
DB_PORT=<db_port>

```
Note that the project was tested with @mail.ru account and app password.

Then execute the following:
```
docker compose up --build -d
docker compose exec mail_service bash # to access app container
```
inside app container execute the following:
```
python manage.py makemigrations
python manage.py migrate
```
to create all tables needed. You should also
```
python manage.py createsuperuser
```
in order to access admin panel, where you can check out celery mailing task states and other info.
Access a launched project on ```localhost:8000``` in any browser.
