# FeedBack

The main feedback api

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
FeedBack Api/
├── feedback/
│   ├── __init__.py
    ├── asgi.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
├──feedback_data
    ├── __init__.py
    ├── admin.py
    ├── app.py
    ├── models.py
    ├── serializer.py
    ├── test.py
    ├── urls.py ## app url routing through main urls
    ├── views.py
├──manage.py
├── README.md

```
**Note the project structure is a blue print and any changes to it should be updated ,(Auto update is not curectly implemented)*

feedback_data is segrigated into ```view_functions``` that handels the the incomming routes, ```urls``` that has the actual url mapping to the view_functions using blueprints, ```models``` handels the database, ```admin``` handles the admin dashborad based of registered models, ```serializers``` contains form fields that can be serialized in json.

All the env setting for the feedback_data app can be done insise the ``settings.py``  
The main app and errors handelers are defined inside the ```__init__.py```   

method POST

### validate feedback data
**url**  
```/feedback/create```  
**request**  
```
method POST
body:
{
    "phone_contact":"+12873645289",
    "feedback":"text",
    "full_name" : "text name field"
}
```  

**response body**  
```

{
    "message":"successfully created",
}
-------------------------
error:
{
  "error": "invalid form data: form field contains invalid data ",  
  "message": "throws serialized data errors", 
  "status_code": 403
}
-------------------------
## ENV
supply the neccessary information for your Database to the env file.
This is to connect the api to your custom database