💻Ceocaching App💻
================================================================

Steps to run it in local.

First, create the virtual environment with `virtualenv`. If you have not installed it, you can do it using `pip`, with the next command: `pip install virtualenv`.

```
virtualenv env
.\env\Scripts\activate
```

Once you are inside the virtual environment, install the required packages:

```
pip install -r .\requirements.txt
```

Then, we need to specify the credentials for the environmental variables. For that we need to copy the `.env.sample` file and complete the data there:

```
cp .env.sample .env
nano .env
```

The fields that have to be completed are the next ones:

```
DJANGO_DEBUG=changeme(1/0)            //  1 for Debug=True & 0 for Debug=False
DB_NAME=changeme                      //  Database name
DB_CLIENT=changeme                    //  Database client url for MongoDB
SECRET_KEY=changeme                   //  Secret key for the Django project
```

Anyway, to work locally, we can specify Django to use local settings. For that, we need to change the next line of the files *manage.py* and *wsgi.py*:

```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings.local')
```

To conclude, make the necessary migrations and the database will be created:

```
python .\manage.py makemigrations
python .\manage.py migrate
```