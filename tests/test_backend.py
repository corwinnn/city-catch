import json
from types import SimpleNamespace
from unittest.mock import patch
import threading
import urllib.request
import pytest

from backend import server


class MockResponse(SimpleNamespace):
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        pass
    def read(self):
        return json.dumps(self.data).encode()


def test_fetch_city_info_success():
    sample = {"title": "Sample", "extract": "Sample city"}
    mock = MockResponse(status=200, data=sample)
    with patch("backend.server.urlopen", return_value=mock):
        assert server.fetch_city_info("Sample") == sample


def test_fetch_city_info_regression():
    with open("tests/data/london.json", "r") as f:
        london = json.load(f)
    mock = MockResponse(status=200, data=london)
    with patch("backend.server.urlopen", return_value=mock):
        assert server.fetch_city_info("London") == london


def test_city_endpoint():
    output = {"title": "Paris", "extract": "Capital of France"}

    def run_server():
        with patch("backend.server.fetch_city_info", return_value=output):
            srv = server.HTTPServer(("", 0), server.CityHandler)
            port = srv.server_port
            threading.current_thread().port = port
            srv.serve_forever()

    t = threading.Thread(target=run_server)
    t.daemon = True
    t.start()
    while not hasattr(t, "port"):
        pass
    port = t.port
    with urllib.request.urlopen(f"http://localhost:{port}/api/city?name=Paris") as resp:
        data = json.loads(resp.read().decode())
    assert data == output
