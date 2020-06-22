Feeds Reader Assignment
--
## Setup environment

Preferably, first create a virtualenv and activate it (i'm using python 3.8), perhaps with the following command:

```
virtualenv -p python3 .venv
source .venv/bin/activate
```

Next, run to get the dependencies.

```
pip install -r requirements.txt
```

Copy the `.env_sample` and rename it into `.env`.
**Remember** changing all environment's variables for security purpose.

Next, we will setup db in one run - put a new name for this  var `SQL_DATABASE` in `.env` file if you want. 
After that you can initialize the database by this command:

```
python manage.py migrate
```

Before going to the Feeds Reader Management, you may need an account to access to Django Admin, create super user 
by this command:
```
python manage.py createsuperuser
```

Finally run the app by the command below

```
python manage.py runserver 127.0.0.1:8001

```
- You can change the ```default service port (8001)``` into another one.

Navigate to the posted URL `http://127.0.0.1:8001/admin/` to be greeted with Django Admin page, please use the account which
you setup above to access.

- In order to grab items from feed urls, just open another terminal and navigate to this project dir, then activate 
virtualenv and run the command below:
```
python manage.py retrieve_feeds 'https://www.feedforall.com/sample-feed.xml' 'http://www.feedforall.com/sample.xml' --verbose
```
**NOTES**: 
- `--verbose` flag will log the progress into your log file which you set in `.env` file - var `LOG_FILE`.
Please change it into your file path which you want.
- After retrieving feeds urls by command above, please navigate to `http://127.0.0.1:8001/admin/feeds_reader/` - here, 
you can add/update/remove feeds/entries and filter items by name in dropdown list search.
- `tests` dir will contain the Unit tests implementation. 


Happy Coding.
