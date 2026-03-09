# To-Do List API

https://roadmap.sh/projects/todo-list-api

A comprehensive Flask-based REST API for managing to-do tasks with JWT authentication, rate limiting, CORS support, and complete API documentation.

## Features

- **User Authentication**: Register and login with secure password hashing (Werkzeug)
- **JWT Tokens**: Token-based authentication with separate access (15 min) and refresh tokens (7 days)
- **Token Refresh**: Endpoint to refresh expired access tokens
- **To-Do Management**: Full CRUD operations for managing to-do tasks
- **User-Specific Tasks**: Each user has their own isolated to-do list
- **Task Status Tracking**: Track task status as open, in progress, or completed
- **Advanced Filtering**: Filter todos by status with pagination
- **Search & Sort**: Search todos by title/description and sort by various fields
- **Rate Limiting**: Endpoint rate limiting to prevent abuse (5 requests/minute for auth endpoints)
- **CORS Support**: Cross-Origin Resource Sharing enabled for frontend integration
- **Database Migrations**: Flask-Migrate integration for schema versioning
- **Swagger Documentation**: Complete OpenAPI 3.0 specification included
- **Error Handling**: Comprehensive error responses with appropriate HTTP status codes

## Tech Stack

- **Framework**: Flask 2.x
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (PyJWT) with Werkzeug password hashing
- **Rate Limiting**: Flask-Limiter
- **CORS**: Flask-CORS
- **Database Migrations**: Flask-Migrate
- **Environment Config**: python-dotenv

## Prerequisites

- Python 3.10+
- pip (Python package manager)

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd "To-Do List"
```

### 2. Create a Virtual Environment (Recommended)

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URI=sqlite:///todos.db
SECRET_KEY=your-secret-key-here-min-32-characters
FLASK_ENV=development
```

**Important**:
- Change `SECRET_KEY` to a random 32+ character string for production
- Database will be created automatically on first run

## Running the Project

### Starting the Server

```bash
python run.py
```

The API will be available at `http://localhost:5000`

### Running in Development Mode

For development with auto-reload:
```bash
python -m flask run
```

## API Endpoints

Complete API documentation is available in `swagger.json`. View it using:
- [Swagger Editor](https://editor.swagger.io) (drag and drop the file)
- [ReDoc](https://redoc.ly/) for alternative documentation format

### Authentication Endpoints

#### Register a New User
- **URL**: `/register`
- **Method**: `POST`
- **Rate Limit**: 5 requests per minute
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response** (201):
  ```json
  {
    "message": "User successfully Registered. Please login"
  }
  ```

#### Login
- **URL**: `/login`
- **Method**: `POST`
- **Rate Limit**: 5 requests per minute
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response** (200):
  ```json
  {
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
  ```

#### Refresh Access Token
- **URL**: `/refresh`
- **Method**: `POST`
- **Rate Limit**: 5 requests per minute
- **Headers**: `Authorization: Bearer <refresh_token>`
- **Response** (200): New access and refresh tokens
- **Note**: Use refresh token to get a new access token when it expires

### To-Do Endpoints

#### Create a To-Do
- **URL**: `/todos`
- **Method**: `POST`
- **Auth**: Required (Bearer token)
- **Body**:
  ```json
  {
    "title": "Task Title",
    "description": "Task Description (optional)"
  }
  ```
- **Response** (201): Created todo object

#### Get All To-Dos
- **URL**: `/todos`
- **Method**: `GET`
- **Auth**: Required (Bearer token)
- **Query Parameters**:
  - `page` (default: 1): Page number for pagination
  - `limit` (default: 10): Items per page
  - `status` (optional): Filter by status (open, in progress, completed)
  - `sort_by` (optional): Sort field (title, status, id)
  - `order` (optional): Sort order (asc, desc)
  - `search` (optional): Search in title and description
- **Response** (200):
  ```json
  {
    "data": [...],
    "page": 1,
    "limit": 10,
    "total": 25
  }
  ```

#### Get a Specific To-Do
- **URL**: `/todos/<id>`
- **Method**: `GET`
- **Auth**: Required (Bearer token)
- **Response** (200): Single todo object

#### Update a To-Do
- **URL**: `/todos/<id>`
- **Method**: `PUT` or `PATCH`
- **Auth**: Required (Bearer token)
- **Body** (all fields optional):
  ```json
  {
    "title": "Updated Title",
    "description": "Updated Description",
    "status": "in progress"
  }
  ```
- **Supported Statuses**: open, in progress, completed
- **Response** (200): Success message

#### Delete a To-Do
- **URL**: `/todos/<id>`
- **Method**: `DELETE`
- **Auth**: Required (Bearer token)
- **Response** (204): No content
- **Note**: Soft delete - marks todo as completed rather than removing from database

## Configuration

Configuration is managed via environment variables in a `.env` file:

```env
DATABASE_URI=sqlite:///todos.db
SECRET_KEY=your-secure-random-key-min-32-chars
FLASK_ENV=development
```

**Environment Variables Explained**:
- **DATABASE_URI**: Database connection string (SQLite recommended for development)
- **SECRET_KEY**: Secure key for JWT signing (must be 32+ characters in production)
- **FLASK_ENV**: Set to 'development' or 'production'

## Project Structure

```
To-Do List/
├── app/
│   ├── __init__.py           # Application factory
│   ├── extensions.py         # Database, limiter, CORS, migrate initialization
│   ├── models.py             # User and Todo database models
│   ├── routes/
│   │   ├── auth_routes.py    # Authentication endpoints
│   │   └── todo_routes.py    # Todo CRUD endpoints
│   └── utils.py              # Token validation and error handlers
├── tests/
│   └── test_app.py           # Test suite
├── run.py                    # Application entry point
├── swagger.json              # OpenAPI 3.0 specification
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (create this)
└── README.md                 # This file
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

| Status | Meaning |
|--------|---------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 204 | No Content - Successful deletion |
| 400 | Bad Request - Invalid input or missing required fields |
| 401 | Unauthorized - Missing, invalid, or expired token |
| 403 | Forbidden - Access denied or resource not owned by user |
| 404 | Not Found - Resource doesn't exist |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

### Error Response Format

```json
{
  "message": "Descriptive error message",
  "error": "error_type (optional)"
}
```

## Authentication & Authorization

### Token Expiration
- **Access Token**: 15 minutes (use for API requests)
- **Refresh Token**: 7 days (use to get new access token)

### Using Tokens

1. Register and login to receive both tokens
2. Use access token for API requests:
   ```
   Authorization: Bearer <access_token>
   ```
3. When access token expires, use refresh endpoint with refresh token:
   ```
   POST /refresh
   Authorization: Bearer <refresh_token>
   ```

### Token Validation

The `token_required` decorator validates:
- Token presence in Authorization header
- Token format (Bearer scheme)
- Token signature and expiration
- Token type (access vs refresh - only access tokens can access protected resources)

## Database

The SQLite database (`todos.db`) will be created automatically in the project root when you first run the application.

### Database Models

**User Model**:
- id (Integer, Primary Key)
- username (String, Unique, Required)
- password_hash (String, Required)

**Todo Model**:
- id (Integer, Primary Key)
- title (String, Required)
- description (String, Optional)
- status (String, Default: "open")
- user_id (Foreign Key to User)

## Rate Limiting

The API implements rate limiting on authentication endpoints:
- `/register`: 5 requests per minute per IP
- `/login`: 5 requests per minute per IP
- `/refresh`: 5 requests per minute per IP

Rate limit errors return status code 429 with descriptive messages.

## CORS Support

The API has CORS enabled for frontend integration. Configure allowed origins in `app.config['CORS_ORIGINS']` if needed.

## Testing

Run the test suite:

```bash
python -m pytest tests/
```

Tests are located in the `tests/` directory and can be expanded as the API grows.

## API Documentation

Complete, interactive API documentation is available in the `swagger.json` file:

### Viewing Swagger Documentation

1. **Online (Recommended)**:
   - Visit https://editor.swagger.io
   - Drag and drop the `swagger.json` file or paste its contents

2. **Local Tools**:
   - ReDoc: https://redoc.ly/docs/redoc/
   - Swagger UI: Use Docker or Node.js packages

3. **Features**:
   - Try out all endpoints with example data
   - View complete request/response schemas
   - See all error codes and examples
   - Test authentication flows

## Future Enhancements

- Task categories/tags
- Due dates and reminders
- Task priority levels
- Subtasks/nested todos
- Task sharing between users
- Webhook notifications
- Batch operations
- Advanced analytics

## License

[Add your license here]

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

For issues, questions, or suggestions:
- Open an issue on the GitHub repository
- Check existing issues for similar problems
- Include detailed error messages and reproduction steps

## Changelog

### Version 1.0.0
- Initial release
- User authentication with JWT tokens
- Todo CRUD operations
- Rate limiting on auth endpoints
- CORS support
- Complete Swagger/OpenAPI documentation
- Database migrations with Flask-Migrate
- Advanced filtering and search functionality
