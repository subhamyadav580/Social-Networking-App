# Social networking application API


This Social networking application provides a Django RESTful API for user management, including user registration, login, friend requests, and more.

## Getting Started

To run this project locally using Docker, follow these steps:

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/subhamyadav580/Social-Networking-App.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Social-Networking-App
    ```

3. Build the Docker image:

    ```bash
    docker-compose build . -t accounts:latest
    ```

4. Start the Docker container:

    ```bash
    docker-compose up
    ```

5. Create a superuser:

    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

    Follow the prompts to enter your desired superuser credentials.

## API Endpoints

### User Registration

**Endpoint**: `/signup` (POST)

**Request Body**:
```json
{
  "email": "test@gmail.com",
  "full_name": "test acc",
  "password": "password",
  "password2": "password"
}
```

**Response**:
```json
{
    "message": "User successfully created",
    "user": {
        "email": "test@gmail.com",
        "full_name": "test acc",
        "is_staff": false,
        "is_admin": false,
        "user_id": 12
    },
    "token": "5f8a921b0310e83bc630e5d62d2b0ba8edf78d7e"
}

```

### User Login

**Endpoint**: `/login` (POST)

**Request Body**:
```json
{
  "email": "test@gmail.com",
  "password": "password"
}

```

**Response**:
```json
{
    "message": "Logged in successfully",
    "user": {
        "email": "test@gmail.com",
        "full_name": "test acc",
        "is_staff": false,
        "is_admin": false,
        "user_id": 12
    },
    "token": "5f8a921b0310e83bc630e5d62d2b0ba8edf78d7e"
}
```


### Send Friend Request

**Endpoint**: `/friend-request/send/<user_id>/` (POST)

**Request Header**:
```
Authorization: Token your_token
```


**Response**:
```json
{
    "message": "Friend request sent."
}

```


### Pending Friend Requests


**Endpoint**: `/friend-request/pending/` (GET)

**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
{
    "pending_requests": [
        {
            "from_user": "test@gmail.com",
            "to_user": "admin@gmail.com",
            "is_accepted": false,
            "created_at": "2024-06-08T10:14:15.077341Z",
            "request_id": 10
        }
    ]
}

```


### Accept Friend Request

**Endpoint**: `/friend-request/accept/<request_id>/` (POST)
**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
{
    "message": "Friend request accepted."
}
```

### Reject Friend Request

**Endpoint**: `/friend-request/reject/<request_id>/` (POST)

**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
{
    "message": "Friend request rejected."
}
```

### Friend List

**Endpoint**: `/friend-list` (GET)

**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
[
    {
        "id": 2,
        "email": "friend1@gmail.com",
        "full_name": "Friend One",
        "is_staff": false,
        "is_admin": false
    },
    {
        "id": 3,
        "email": "friend2@gmail.com",
        "full_name": "Friend Two",
        "is_staff": false,
        "is_admin": false
    }
]

```


### User Search

**Endpoint**: `/search/?search=test&page=1` (GET)

**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
[
    {
        "id": 2,
        "email": "test@gmail.com",
        "full_name": "test acc",
        "is_staff": false,
        "is_admin": false
    }
]
```
