mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

msg:
	python3 manage.py makemessages -l uz -l ru -l en
