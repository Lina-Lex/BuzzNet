from flask import Flask
from .routes.ivr_url import IVRFlow  
from .routes.auth import Auth

app = Flask(__name__)

app.register_blueprint(IVRFlow)
app.register_blueprint(Auth,url_prefix='/authenticate')




#############################
###### ERROR HANDLER ########

@app.errorhandler(404)
def not_found(error):
    print(error)
    return (("""
                <h1>ARE YOU LOST</h1>
                
                """),404)

@app.errorhandler(405)
def method_notallowed(error):
    return (("""<h1>ARE YOU LOST</h1>
                    """),405)

@app.errorhandler(403)
def forbidden_page(error):
    return ({"status_code":403,'exit_code':1,"error":f"permission denied/ {str(error)}","message":"failed"},403)

@app.errorhandler(500)
def server_error(error):
    return ({"status_code":500,'exit_code':1,"error":f"Internal server error {str(error)}","message":"failed"},500)

@app.errorhandler(400)
def token_expired(error):
    return ({"status_code":400,'exit_code':2,"error":f"Bad Request/ Data format incorrect / Invalid Token {str(error)}","message":"failed"},400)

@app.errorhandler(401)
def unauthorized(error):
    return ({"status_code":401,'exit_code':1,"error":f"Authorization failed,password incorrect {str(error)}","message":"failed"},401)
