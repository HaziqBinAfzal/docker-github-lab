"""Verify both routes through an actual running server's HTTP interface."""
import json
import sys
from urllib.request import urlopen


def check(base_url):
    expected = {
        '/': {'service': 'docker-github-lab', 'message': 'Hello from Docker & GitHub Lab!'},
        '/health': {'status': 'ok'},
    }
    for path, payload in expected.items():
        with urlopen(base_url.rstrip('/') + path, timeout=5) as response:
            if response.status != 200 or json.load(response) != payload:
                raise RuntimeError(f'Unexpected response for {path}')
        print(f'PASS {path}')


if __name__ == '__main__':
    check(sys.argv[1] if len(sys.argv) > 1 else 'http://127.0.0.1:8080')
