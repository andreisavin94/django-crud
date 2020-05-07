# django-crud
A simple CRUD application using Django

# Description
You must login with a GitHub account to access this app.
Once logged in, you can see your profile information if it exists or you can create a new profile.
Furthermore, you can update or delete your profile.

# How to build
* Please make sure you've created and activated a virtual environment before attempting to build or run this app. 
You can find information regarding virtual environments [HERE.](https://docs.python.org/3/tutorial/venv.html)
* Once you have activated the virtual env, you can build the app using:
```
pip install -r requirements.txt
```

And then run migrations:
```
python manage.py migrate
```

Alternatively, you can use the `make` command:

```
make build
```

# How to run
* With a virtual env activated, run:
```
python3 manage.py runserver
```

Alternatively, you can use the `make` command:
```
make run
```

* Once the server is running open http://localhost:8000/ to see the app.

# How to run tests
* To run tests, run the following command:
```
python3 manage.py test
```

Alternatively you can use the `make` command:
```
make test
```