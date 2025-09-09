# City Catch

City Catch is a minimal web application that shows Wikipedia information about any city. The frontend is a static page hosted on GitHub Pages with an oval input over a generated city skyline background. The backend is a small Python service that queries Wikipedia and returns a short summary for a requested city.

## Setup and Installation

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd city-catch
   ```
2. **Run the backend**
   ```bash
   python backend/server.py
   ```
   The service listens on port `8000` and exposes `/api/city?name=City`.
3. **Open the frontend**
   Serve the `frontend/` folder or open `frontend/index.html` directly in a browser. By default the page falls back to calling Wikipedia directly. To use the Python backend, set `API_BASE` in the browser console:
   ```javascript
   window.API_BASE = 'http://localhost:8000';
   ```

## Running Tests

Unit and regression tests cover the backend logic and endpoint. Run them with:
```bash
pytest
```

## CI/CD Pipeline

The GitHub Actions workflow `.github/workflows/ci.yml` runs on every push and pull request:

1. Set up Python.
2. Install dependencies and run all tests.
3. If tests pass, the `frontend/` directory is deployed to GitHub Pages.

## GitHub Pages Hosting

The deployed site is available via GitHub Pages once the workflow completes. The static page can call the backend if it is hosted separately and `API_BASE` is configured accordingly.
