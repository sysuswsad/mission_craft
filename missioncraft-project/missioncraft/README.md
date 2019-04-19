
## run app
```bash

bash:

for mac/linux:
    export FLASK_APP=missioncraft
    export FLASK_ENV=development
    flask run

    visit:  
        http://127.0.0.1:5000/hello 

    export FLASK_APP=missioncraft
    export FLASK_ENV=development
    flask init-db

    visit:  
        http://127.0.0.1:5000/auth/register
        http://127.0.0.1:5000/auth/login

    flask run
    flaskr

    pip install -e .
```

## tree of app
```bash
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py
└── MANIFEST.in
```