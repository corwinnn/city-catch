import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, quote
from urllib.request import urlopen


def fetch_city_info(city: str):
    """Fetch summary information about a city from Wikipedia."""
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(city)}"
    try:
        with urlopen(url, timeout=5) as response:
            if response.status != 200:
                return None
            data = json.loads(response.read().decode())
            return {
                "title": data.get("title"),
                "extract": data.get("extract"),
            }
    except Exception:
        return None


class CityHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/city":
            self.send_response(404)
            self.end_headers()
            return

        params = parse_qs(parsed.query)
        city = params.get("name", [""])[0]
        info = fetch_city_info(city) if city else None

        self.send_response(200 if info else 404)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        if info:
            self.wfile.write(json.dumps(info).encode())
        else:
            self.wfile.write(json.dumps({"error": "City not found"}).encode())


def run(port: int = 8000):
    server = HTTPServer(("", port), CityHandler)
    print(f"Server running on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    run()
