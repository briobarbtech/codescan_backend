from flask import Flask
from routes.students import students

app = Flask(__name__)

app.register_blueprint(students)
