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
    "email": "test@user.com",
    "full_name": "test user",
    "password": "test@12345",
    "password2": "test@12345"
}
```

**Response**:
```json
{
    "user": {
        "id": 1,
        "email": "test@user.com",
        "full_name": "test user",
        "is_staff": false,
        "is_admin": false
    },
    "token": "your_token"
}

```

### User Login

**Endpoint**: `/login` (POST)

**Request Body**:
```json
{
    "email": "test@user.com",
    "password": "test@12345"
}

```

**Response**:
```json
{
    "user": {
        "id": 1,
        "email": "test@user.com",
        "full_name": "test user",
        "is_staff": false,
        "is_admin": false
    },
    "token": "your_token"
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

### Pending Friend Requests


**Endpoint**: `/friend-request/pending/` (GET)

**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
[
    {
        "id": 1,
        "from_user": "sender@example.com",
        "to_user": "receiver@example.com",
        "is_accepted": false,
        "created_at": "2024-06-08T12:00:00Z"
    }
]

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
        "email": "friend1@example.com",
        "full_name": "Friend One",
        "is_staff": false,
        "is_admin": false
    },
    {
        "id": 3,
        "email": "friend2@example.com",
        "full_name": "Friend Two",
        "is_staff": false,
        "is_admin": false
    }
]

```


### User Search

**Endpoint**: `/search/?search=<keyword>&page=1` (GET)

**Request Header**:
```
Authorization: Token your_token
```

**Response**:
```json
[
    {
        "id": 2,
        "email": "user@example.com",
        "full_name": "John Doe",
        "is_staff": false,
        "is_admin": false
    }
]
```
