# Scotty-Maps
18-500 Capstone project code



### Starting up the server
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

venv\Scripts\Activate.ps1

python manage.py runserver



### Setting up Docker Container for redis

docker run --rm -p 6379:6379 redis:7
