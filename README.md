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

To conclude, make the necessary migrations and the database will be created:

```
python .\manage.py makemigrations
python .\manage.py migrate
```