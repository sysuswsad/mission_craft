import os
from app import create_app
app = create_app()
app.run(port=5000)

# To Run:
# python run.py
# or
# python -m flask run
