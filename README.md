# ThinklandBlog

FOR LINUX

$ git clone https://github.com/Amirshox/ThinklandBlog.git
$ cd ThinklandBlog
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py loaddata data.json
$ python manage.py runserver
