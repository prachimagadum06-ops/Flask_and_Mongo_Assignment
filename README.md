# Flask + MongoDB Atlas App

A simple Flask REST API backed by MongoDB Atlas, with secure config handling and input validation.

## Features
- Flask REST API with MongoDB Atlas as the database
- Connection string loaded securely from environment variables (never hardcoded)
- Input validation on incoming requests
- Graceful error handling for bad data and database errors

## Prerequisites
- Python 3.9+
- A MongoDB Atlas account and cluster (or local MongoDB instance)
- pip

## Setup

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate       # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**

   Copy the example file and fill in your own values:
   ```bash
   cp .env.example .env
   ```

   Edit `.env`:
   ```
   MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
   FLASK_ENV=development
   ```

   > **Never commit your `.env` file.** It's already included in `.gitignore`.

5. **Run the app**
   ```bash
   flask run
   ```
   The app will be available at `http://127.0.0.1:5000`.

## Environment Variables

| Variable    | Required | Description                                  |
|-------------|----------|-----------------------------------------------|
| `MONGO_URI` | Yes      | MongoDB Atlas connection string               |
| `FLASK_ENV` | No       | `development` or `production` (default: production) |

## API Endpoints

| Method | Endpoint          | Description              |
|--------|-------------------|---------------------------|
| GET    | `/items`          | List all items            |
| GET    | `/items/<id>`     | Get a single item by ID   |
| POST   | `/items`          | Create a new item         |
| PUT    | `/items/<id>`     | Update an existing item   |
| DELETE | `/items/<id>`     | Delete an item             |

### Example: Create an item
```bash
curl -X POST http://127.0.0.1:5000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Sample Item", "price": 9.99}'
```

**Validation rules:**
- `name` — required, non-empty string
- `price` — required, non-negative number

Invalid or missing fields return a `400` response with an error message. Requests for a non-existent ID return `404`. Malformed IDs return `400`. Database-level failures return `500` with an error message rather than crashing the app.

## Project Structure
```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── .env.example         # Template for required environment variables
├── .gitignore
└── README.md
```

## Tech Stack
- **Flask** — web framework
- **MongoDB Atlas** — cloud database
- **PyMongo** — MongoDB driver for Python
- **python-dotenv** — environment variable management

## Notes
This project follows basic DevOps best practices:
- No secrets committed to version control
- Config via environment variables (12-factor app style)
- Input validation and error handling at the API layer

## License
MIT