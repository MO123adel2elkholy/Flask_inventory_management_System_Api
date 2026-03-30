# Database Migration Command 
flask db init
# to Do Actual Migrations You Should use such makemigration in django 
flask db migrate -m"initial migrations"
# To applay the migrations use 
flask db upgrade
