# flaskapp

The main flask app

```
pip install -r requirements.txt

```
If fails to install ```psycopg2``` on linux try below steps  
**Python 3**
```
sudo apt install libpq-dev python3-dev
sudo apt-get install build-essential
pip install psycopg2
```
## Project structure
```
flaskapp/
├── core/
│   ├── ivr_core.py
├── __init__.py
├── README.md
├── models/
│   ├── ivr_model.py
├── routes/
│   ├── auth.py
│   ├── ivr_url.py
├── settings.py
├── tools/
│   ├── authtools/
│   │   ├── authgen.py
│   │   ├── env.py
│   │   ├── __init__.py
│   │   ├── otpstore.py
│   │   └── README.md
│   ├── data/
│   ├── templates/
│   └── util.py
└── view_functions/
    ├── authenticate.py
    ├── ivrflow.py

```
**Note the project structure is a blue print and any changes to it should be updated ,(Auto update is not curectly implemented)**

flaskapp is segrigated into ```view_functions``` that handels the the incomming routes, ```routes``` that has the actual url mapping to the view_functions using blueprints, ```models``` handels the database, ```core``` have the core business logic implemented, ```tools``` contains helper libraries.

All the env setting for the flask app can be done insise the ``settings.py``  
The main app and errors handelers are defined inside the ```__init__.py```   

## REST API

### get otp
**url**  
```/authenticate/get_otp```  
**request**  
```
method POST
body:
{
    "phone":"+912873645289"

}
```  

**response body**  
```

{
    "message":"success",
    'exit_code':0
}
-------------------------
error:
{
    "error": "Internal server error 500 Internal Server Error: unable to connect to message server :- Credentials are required to create a TwilioClient",
    "exit_code": 5,
    "message": "failed",
    "status_code": 500
}
-------------------------
``` 


### validate otp
**url**  
```/authenticate/validate_otp```  
**request**  
```
method POST
body:
{
    "phone":"+912873645289",
    "otp":"012313"

}
```  

**response body**  
```

{
    "message":"success",
    'exit_code':0
}
-------------------------
error:
{
  "error": "permission denied/ 403 Forbidden: Invalid OTP or Validation failed ", 
  "exit_code": 1, 
  "message": "failed", 
  "status_code": 403
}
-------------------------
``` 
