python3 -m pip install pipenv
cd Proj/
pipenv install django
pipenv shell
django-admin startproject trader .
//Using custom port no
python3 manage.py runserver PORT_NO
//Using default portno:8000
python3 manage.py runserver 
python3 manage.py makemigration
python3 manage.py migrate
python3 manage.py createsuperuser
pipenv install websockets