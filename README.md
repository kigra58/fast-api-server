# User Management API

A FastAPI-based REST API for user management with PostgreSQL integration, following industry standards and best practices.

## Features

- User authentication with JWT tokens
- User management (CRUD operations)
- Role-based access control
- PostgreSQL database integration
- Input validation with Pydantic
- Comprehensive error handling
- Logging system
- API documentation with Swagger/OpenAPI
- Database migrations with Alembic

## Project Structure

```
fast-api-server/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── api.py
│   │       └── endpoints/
│   │           ├── auth.py
│   │           └── users.py
│   ├── core/
│   │   ├── config.py
│   │   ├── deps.py
│   │   ├── logging.py
│   │   ├── middleware.py
│   │   └── security.py
│   ├── db/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   └── user.py
│   ├── schemas/
│   │   └── user.py
│   ├── services/
│   │   └── user.py
│   ├── tests/
│   │   └── test_users.py
│   ├── utils/
│   │   └── errors.py
│   └── main.py
├── alembic/
│   ├── env.py
│   └── versions/
├── alembic.ini
├── .env
└── requirements.txt
```

## Setup Instructions

### Prerequisites

- Python 3.8+
- PostgreSQL Server

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd fast-api-server
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory with the following variables:
   ```
   POSTGRES_SERVER=localhost
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_password
   POSTGRES_DB=user_management
   SECRET_KEY=your_secret_key
   BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
   ```

5. Create the PostgreSQL database:
   ```
   sudo -u postgres psql
   CREATE DATABASE user_management;
   \q
   ```

6. Run database migrations:
   ```
   alembic upgrade head
   ```

7. Start the application:
   ```
   uvicorn app.main:app --reload
   ```

8. Access the API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/login` - Get access token

### Users
- `GET /api/v1/users/` - Get all users (superuser only)
- `POST /api/v1/users/` - Create new user (superuser only)
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users/{user_id}` - Get user by ID
- `PUT /api/v1/users/{user_id}` - Update user (superuser only)
- `DELETE /api/v1/users/{user_id}` - Delete user (superuser only)

## Running Tests

```
pytest app/tests/
```

## License

MIT
