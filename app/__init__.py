from os import path
from flask import Flask
from flask_cors import CORS
from .config import configs
cors=CORS()
def create_app(config):
    app=Flask(__name__)
    app.config.from_object(configs[config])
    from .uploader import uploader
    app.register_blueprint(uploader)
    cors.init_app(app)
    return app
    

def getuploadpath():
    return path.join(path.abspath(path.dirname(__file__)),'uploads')

    
    