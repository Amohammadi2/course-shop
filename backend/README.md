# E-Learning Platform Backend

This repository contains the backend for a comprehensive e-learning platform built with Django, Django REST Framework, and Django Channels. It features a robust set of functionalities including course management, a credit-based wallet system, secure video streaming, and a real-time support chat.

## Key Features

- **User Authentication**: JWT-based authentication with a custom user model.
- **Course Management**: Admins can create, manage, and delete courses and lessons.
- **Internal Wallet System**: Users have a credit-based wallet for purchasing courses. All transactions are atomic and logged for auditing.
- **Secure Video Streaming**: Only enrolled users can stream lesson videos. Video URLs are never exposed to the public.
- **Real-Time Support Chat**: A WebSocket-based chat system for users to communicate with admins. Admins are assigned to chat tickets based on categories and workload.
- **API Documentation**: The entire API is documented with OpenAPI (Swagger) and can be accessed at `/api/schema/swagger-ui/`.

## Technology Stack

- Django & Django REST Framework
- Django Channels for WebSockets
- PostgreSQL (for production, SQLite for development)
- Redis (as the Channels message broker)
- `djangorestframework-simplejwt` for JWT authentication
- `drf-spectacular` for OpenAPI documentation

---

## Setup and Installation

These instructions will guide you through setting up the backend on both Linux and Windows.

### Prerequisites

- Python 3.8+
- PostgreSQL
- Redis
- A Python virtual environment tool (e.g., `venv`)

### 1. Clone the Repository

```bash
git clone <repository-url>
cd backend
```

### 2. Set Up the Environment

**On Linux/macOS:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**On Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

This project uses environment variables to manage sensitive information. Create a `.env` file in the `backend` directory and add the following:

```
DJANGO_SECRET_KEY='your-secret-key'
DJANGO_DEBUG='True'
DATABASE_URL='sqlite:///db.sqlite3' # Or your PostgreSQL URL
REDIS_URL='redis://localhost:6379'
```

### 4. Set Up the Database

For development, the project is configured to use SQLite out of the box. Simply run the migrations:

```bash
python manage.py migrate
```

For production, you will need to set up PostgreSQL and update the `DATABASE_URL` in your `.env` file accordingly.

### 5. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000`.

---

## API Documentation

The API is fully documented using OpenAPI. Once the server is running, you can access the documentation at:

- **Swagger UI**: `http://127.0.0.1:8000/api/schema/swagger-ui/`
- **ReDoc**: `http://127.0.0.1:8000/api/schema/redoc/`

## WebSocket Protocol

The real-time chat system uses WebSockets. To connect, a client must authenticate by providing a valid JWT in the query string:

`ws://127.0.0.1:8000/ws/chat/{ticket_id}/?token={jwt_token}`

Once connected, messages can be sent and received in JSON format:

**Client to Server:**
```json
{
  "message": "Hello, I need help."
}
```

**Server to Client:**
```json
{
  "message": "Hello, I need help.",
  "sender": "username",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
}
```
---
## Known Limitations
- The JWT authentication for WebSockets has a simplified implementation in the middleware. In a production environment, this should be made more robust.
- The video streaming is handled directly by Django, which is not ideal for a high-traffic production environment. A dedicated media server or cloud service would be more appropriate.
- The project is configured to use SQLite for development. For production, it is highly recommended to use PostgreSQL.

## Future Improvements
- Implement a more robust role-based access control system.
- Integrate a real payment gateway for purchasing credits.
- Add support for file attachments in the chat system.
- Implement a more sophisticated load-balancing algorithm for the chat system.
- Add unit and integration tests for all apps.
