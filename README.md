# Email Availability Checker

A FastAPI service to check if a Gmail username is already taken.

## Installation

1. Clone this repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Running the API

Start the service with:

```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

## API Endpoints

### Check Email Availability

```
POST /check-email
```

Request body:

```json
{
  "domain": "username" // The username part before @gmail.com
}
```

Response:

```json
{
  "email": "username@gmail.com",
  "is_available": true, // true if the email is available, false if taken
  "is_registered": false // true if the email is registered, false if not
}
```

### Health Check

```
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

## API Documentation

Swagger documentation is available at `/docs` when the server is running.
