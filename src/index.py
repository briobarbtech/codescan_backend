from app import app
from config import config
from routes.students import page_not_found

if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404,page_not_found)
    app.run()