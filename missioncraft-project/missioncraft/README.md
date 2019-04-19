
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

    pip install -e .
```

## tree of app
```bash
missioncraft-project
├── missioncraft/
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
│   └── static/
│       └── style.css
├── venv/
├── setup.py
└── MANIFEST.in
```
