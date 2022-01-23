worker:
	FLASK_APP=manage.py flask runworker

serve:
	FLASK_APP=manage.py FLASK_ENV=development flask run