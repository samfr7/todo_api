# To-Do List API

https://roadmap.sh/projects/todo-list-api

A Flask-based REST API for managing to-do tasks with user authentication and JWT tokens.

## Features

- **User Authentication**: Register and login with secure password hashing
- **JWT Tokens**: Token-based authentication with 24-hour expiration
- **To-Do Management**: Create, read, and manage to-do tasks
- **User-Specific Tasks**: Each user has their own to-do list
- **Task Status Tracking**: Track task status as open, in progress, or completed
- **SQLite Database**: Lightweight database for storing users and tasks

## Tech Stack

- **Framework**: Flask
- **Database**: SQLite
- **Authentication**: JWT (PyJWT), Werkzeug
- **ORM**: SQLAlchemy

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

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
pip install flask flask-sqlalchemy PyJWT werkzeug
```

Or install from a requirements.txt file (if available):
```bash
pip install -r requirements.txt
```

## Running the Project

### Starting the Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

### Running in Development Mode

For development with auto-reload:
```bash
python -m flask run --reload
```

## API Endpoints

### Authentication

#### Register a New User
- **URL**: `/register`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**: Redirects to login

#### Login
- **URL**: `/login`
- **Method**: `POST`
- **Body**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
    "token": "jwt_token_here"
  }
  ```

### To-Do Management

#### Create a To-Do
- **URL**: `/todos`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Body**:
  ```json
  {
    "title": "Task Title",
    "description": "Task Description"
  }
  ```
- **Response**: `201 Created`

#### Get All To-Dos
- **URL**: `/todos`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Query Parameters**:
  - `page` (optional): Page number for pagination (default: 1)
  - `limit` (optional): Number of items per page (default varies)
- **Response**: List of all user's to-dos with pagination info
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
- **Headers**: `Authorization: Bearer <token>`
- **Response**: Single to-do details

#### Update a To-Do
- **URL**: `/todos/<id>`
- **Method**: `PUT` or `PATCH`
- **Headers**: `Authorization: Bearer <token>`
- **Body** (all fields optional):
  ```json
  {
    "title": "Updated Title",
    "description": "Updated Description",
    "status": "in progress"
  }
  ```
- **Response**: `200 OK` with success message

#### Delete a To-Do
- **URL**: `/todos/<id>`
- **Method**: `DELETE`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `204 No Content` (marks task as completed)
- **Note**: Deleting a to-do marks it as completed rather than removing it from the database

## Configuration

Edit the following in `app.py` for production:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'this_is_the_secret'
```

- **SQLALCHEMY_DATABASE_URI**: Database connection string
- **SECRET_KEY**: Change this to a secure random string for production

## Project Structure

```
To-Do List/
├── app.py              # Main application file
├── instance/           # Instance folder (contains database)
│   └── users.db        # SQLite database
└── README.md           # This file
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200 OK`: Successful request
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Authentication failed or token invalid
- `500 Internal Server Error`: Server error

## Token Usage

After logging in, use the token in the Authorization header for protected endpoints:

```
Authorization: Bearer <your_jwt_token>
```

## Database

The SQLite database (`users.db`) will be created automatically in the `instance/` folder when you first run the application.

## Future Enhancements

- Refresh token mechanism
- Task filtering and sorting by status or date
- Rate limiting
- Input validation and error handling improvements
- Unit tests
- Swagger/OpenAPI documentation

## License

[Add your license here]

## Support

For issues or questions, please open an issue on the repository.
