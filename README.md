# Room Rate Management - Using Django REST Framework (DRF), MySql & Swagger

## Prerequisites
`Python`
`pip`
`MySql`
`MySqlClient`

Follow the below mentioned steps to run the code.


Go to the project directory

```bash
  cd room_rate_management
```

Create and activate a virtual environment

```bash
  python -m venv <path to venv>
  source /<path to venv>/bin/activate
```

Set MYSQLCLIENT environment variables

```bash
export MYSQLCLIENT_CFLAGS=$(mysql_config --cflags)
export MYSQLCLIENT_LDFLAGS=$(mysql_config --libs)
```

Install dependencies

```bash
pip install -r requirements.txt
```

Set MySql DB address, name and password in room_rate_management/settings.py

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '<DB_NAME>',
        'USER': '<DB_USER>',
        'PASSWORD': '<DB_PASSWORD>',
        'HOST': '<DB_ADDRESS>',
        'PORT': '3306',
    }
}
```

Run the DB Migrations.
```bash
python manage.py makemigrations api
python manage.py migrate
```

Start the app.
```bash
python manage.py runserver
```

API URL - [http://127.0.0.1:8000/api/](http://127.0.0.1:8000/api/)

Swagger URL - [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)

API docs - [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)



