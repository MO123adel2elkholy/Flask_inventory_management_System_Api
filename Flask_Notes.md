# Flask 
## Flask is mimimal WEB for Developing WEb apps 
* Running Command  flask --app app run
* Congigure Ruff (liniting and formating tool ) for your code 
'''
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
''''
* Our Flask Prject Structure Ecommerce/apps/app1/app2
* we created our like that for modularity and Scalabilty 
* In __init__.py file create_app  works ass Factory Function (design pattern) for creating Flask app 
* this Enaples us from single Cooncern of responsabilty (Diffrent configuration for Diffrent APPs , Production and Development Stages  )
* enaples us For isolation of code Base From Businnes Logic 
# What is Alembic 
* alembic is Database migration too that Enaples us to migration on Flask Ddatabase models through Flask-Migrate 

# what is Flask blue Print 

 * blueprint makes our app more modular and easy to manitains and sacaling 


# What is Marshmallow 
* Marshmallow is Python  Packe for Data serealization bulit on flask


# what is apifairy 
* apifairy is minimal framework buit on flask to Enaples Rest opertions in easy way unlike marshmallow  which we do this in complicated way
# what is flask admin 
* deisgn nice interface for working with databasse 


# flask-Admin 
* flask-admin is python package thats enaples us to create nice interface thats eanables to make CRUD ops on models and doing filers and other operations 


# Celery
* celery is asyncronous task processing queue for background tasks this is used for heavy  tasks like sending Email - Image Processing 
``` celery -A make_celery worker --pool=solo --loglevel 
INFO ```


# celery_beat 
* running  Tasks on  Schedule we beat to runs task in specfic  peroid of time  tasks such sending Email to cutomer eaach 2 day 
``` celery -A make_celery beat  --loglevel INFO ```




# clery RedBeat
* celery red beast is used for controlling Schedule (Dynamic schedule )
in tasks requiring dynamic scheduling like taking scdule from user this is good for producttion level rather than celery beat 
```    celery -A make_celery beat -S redbeat.RedBeatScheduler --loglevel= INFO ```


# ariadne 
* integratig ariadne  for for Graphql api with flask 

