import json
import pytest
import requests
from requests.auth import HTTPBasicAuth


BASE = 'https://localhost:9200'
AUTH = HTTPBasicAuth('admin', 'admin')

@pytest.mark.dependency()
def test_write_log():
    response = requests.post(
        f'{BASE}/app-logs/_doc',
        json={'level': 'INFO', 'message': 'Hello from test_write_log'},
        auth=AUTH,
        verify=False
    )

    assert response.status_code == 201

@pytest.mark.dependency(depends=['test_write_log'])
def test_read_log():
    resp = requests.get(
        f'{BASE}/app-logs/_search',
        json={'query': {'match': {'message': 'test_write_log'}}},
        auth=AUTH,
        verify=False
    )
    hits = resp.json()['hits']['hits']

    assert len(hits) == 1
