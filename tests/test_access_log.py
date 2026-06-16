import json
import pytest
import requests
from requests.auth import HTTPBasicAuth


BASE = 'http://localhost:9200'
AUTH = HTTPBasicAuth('admin', 'admin')

@pytest.mark.dependency()
def test_write_log():
    response = requests.post(
        f'{BASE}/app-logs/_doc',
        json={'level': 'INFO', 'message': 'Hello from test_write_log'},
        auth=AUTH
    )

    assert response.status_code == 200

@pytest.mark.dependency(depends=['test_write_log'])
def test_read_log():
    resp = requests.get(
        f'{BASE}/app-logs/_search',
        json={'query': {'match': {'message': 'hello'}}},
        auth=AUTH
    )
    hits = resp.json()['hits']['hits']

    assert len(hits) == 1
