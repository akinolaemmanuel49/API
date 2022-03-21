db_init: python db/manage.py version_control
db_version: python db/manage.py db_version
migrate: python db/manage.py upgrade
web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}
