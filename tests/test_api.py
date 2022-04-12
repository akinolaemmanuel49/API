from fastapi.testclient import TestClient

from api.v1 import __version__
from api.v1.main import app


client = TestClient(app=app)
