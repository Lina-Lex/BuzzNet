from flask import Flask
from .routes.ivr_url import IVRFlow  
from .routes.auth import Auth

app = Flask(__name__)

app.register_blueprint(IVRFlow)
app.register_blueprint(Auth,url_prefix='/authenticate')


