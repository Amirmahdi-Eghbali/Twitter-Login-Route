# Twitter Login System

A simple FastAPI project for managing user login tasks with Kafka integration and JWT authentication.

## Features
- User registration and login
- Task management using Kafka
- JWT-based authentication
- MongoDB ODM for database operations

---

## How to Run the Project

1. Clone the repository:
    ```bash
    git clone https://github.com/Amirmahdi-Eghbali/Twitter-Login-Route.git
    cd twitter-login
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Start the Kafka server:
    ```bash
    bin/zookeeper-server-start.sh config/zookeeper.properties
    bin/kafka-server-start.sh config/server.properties
    ```

4. Run the FastAPI application:
    ```bash
    uvicorn main:app --reload
    ```

5. Access the API with swagger at:
    ```
    http://127.0.0.1:8000/docs#/default
    ```

---

## API Endpoints

### User Management
- **POST /add-user**: Add a new user.
- **POST /twitter-login**: Login a user and send their credentials as a Kafka message.
- **GET /get-users**: Get a list of all registered users.

### Task Management
- **GET /get-tasks**: Get all task statuses (authentication required).
- **GET /get-by-id?task_id=**: Get the status of a specific task by ID (authentication required).

### JWT Utilities
- **GET /current-user**: Decode the current user's JWT token.


---

## How to Authenticate

1. Register a new user using the `/add-user` endpoint.
2. Login using `/twitter-login` to get a JWT token.
3. Use the token in requests requiring authentication:
    ```bash
    Authorization: Bearer <your-token>
    ```

---
I learned a lot from doing this project.

I hope you enjoy :)

by Amirmahdi Eghbali