web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
db_init: python app/db/manage.py version_control
db_version: python app/db/manage.py db_version
migrate: python app/db/manage.py upgrade
