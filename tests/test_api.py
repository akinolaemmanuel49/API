from fastapi.testclient import TestClient
from fastapi import status

from api.v1 import __version__
from api.v1.main import app


client = TestClient(app=app)
