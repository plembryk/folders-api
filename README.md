# Word Grouping and Folder Management API

## Project Overview

This application provides an API for grouping lists of words based on their prefixes and managing folders that contain these word groups. It includes the following features:

- **Word Grouping by Prefix**: The application identifies common prefixes in words based on a specified delimiter and groups them accordingly.
- **Folder Management**: Allows creating folders and moving word groups between folders.
- **REST API with Django REST Framework (DRF)**: The API provides CRUD functionality and support for word grouping and folder management.

The application is containerized using Docker and configured with persistent storage.

## Prerequisites

Make sure you have the following versions of Poetry, Docker and Docker Compose installed:

- **Docker**: `24.0.5`
- **Docker Compose**: `v2.29.7`
- **Poetry**: `1.8.4`
## Data Structure

### Models

- **Folder**: Stores folders containing word groups.
- **WordGroup**: Represents a group of words based on prefixes.
- **Word**: Stores individual words, their delimiters, and references to a group.

## Installation and Running the Project

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/plembryk/folders-api.git
   cd https://github.com/plembryk/folders-api.git
   ```

2. **Run with Docker Compose**:

    To start the project with Docker, run:

    ```bash
    docker-compose up --build
   ```
   The application should now be available at http://localhost:8000
## Running tests

To run the tests in the project, you need to set the appropriate environment variables. You can export them in your terminal before running the tests. Here are the variables you should export:
```bash
DJANGO_DATABASE_USER={db_user}
DJANGO_DATABASE_HOST={db_host}
DJANGO_ALLOWED_HOSTS=*
DJANGO_DATABASE_PORT={db_port}
DJANGO_DATABASE_PASSWORD={db_password}
DJANGO_DATABASE_NAME={db_name}
DJANGO_DATABASE_ENGINE=django.db.backends.postgresql
PYTHONPATH=${PWD}/src
```

To run the tests using Pytest, follow these steps:

1. Ensure that you have all the required dependencies installed. If you haven't installed them yet, you can do so using poetry:

    ```bash
    poetry install
    ```

2. Next, in the main project directory, run the tests with the following command:

    ```bash
    pytest
    ```

After executing the above steps, Pytest will run all the tests in the project, and the results will be displayed in the terminal.


## API Endpoints

### API Documentation

This project uses Swagger for API documentation, providing a UI for exploring the available endpoints.

- **Swagger UI endpoint**: `/swagger`
- **Redoc endpoint**: `/redoc`

You can use these interfaces to explore and test the API endpoints for word grouping and folder management functionalities.


### Folder Endpoints
#### List All Folders
- **Endpoint**: `api/folders`
- **Method**: `GET`
- **Response**: List of folders.

#### Create a Folder
- **Endpoint**: `api/folders`
- **Method**: `POST`
- **Request Body**:
  - `name` (String): Name of the folder to create.
- **Response**: Created folder object.

### Word Group Endpoints
#### List All Word Groups
- **Endpoint**: `api/word-groups`
- **Method**: `GET`
- **Response**: List of word groups with their associated words.

#### Retrieve a Word Group
- **Endpoint**: `api/word-groups/{id}`
- **Method**: `GET`
- **Response**: Details of a single word group.

#### Move Word Groups
- **Endpoint**: `api/word-groups/move`
- **Method**: `POST`
- **Request Body**:
  - `folder_id` (UUID): Target folder to move the word groups to.
  - `word_group_ids` (List[UUID]): List of word group IDs to move.
- **Response**: Confirmation message upon successful move.

### Word Endpoints
#### List All Words
- **Endpoint**: `api/words`
- **Method**: `GET`
- **Response**: List of words.

#### Retrieve a Word
- **Endpoint**: `api/words/{id}`
- **Method**: `GET`
- **Response**: Details of a single word.

#### Batch Create Words
- **Endpoint**: `api/words`
- **Method**: `POST`
- **Request Body**:
  - `delimiter` (Char): Delimiter to apply.
  - `words` (List[String]): List of words to create.
- **Response**: List of created word objects.