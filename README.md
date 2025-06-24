# Late Show API

This project implements a Flask API for a Late Show application, managing episodes, guests, and their appearances on the show.

## Features

* **RESTful Endpoints:** Standard CRUD operations for Episodes, Guests, and Appearances.
* **Database Management:** Uses SQLAlchemy for ORM and Flask-Migrate for database migrations.
* **Data Models:** Defines relationships between Episodes, Guests, and Appearances, including cascading deletes.
* **Data Validation:** Ensures appearance ratings are within a valid range.
* **Serialization:** Handles complex object serialization to JSON, preventing recursion issues.

## Data Models

The API interacts with the following data models:

* **`Episode`**: Represents a single episode of the show.
    * `id` (Primary Key)
    * `date` (String)
    * `number` (Integer)
* **`Guest`**: Represents a guest who appeared on the show.
    * `id` (Primary Key)
    * `name` (String)
    * `occupation` (String)
* **`Appearance`**: Represents a specific guest's appearance on an episode, acting as a join table.
    * `id` (Primary Key)
    * `rating` (Integer, validated between 1 and 5)
    * `episode_id` (Foreign Key to `Episode.id`, with `ondelete='CASCADE'`)
    * `guest_id` (Foreign Key to `Guest.id`, with `ondelete='CASCADE'`)

**Relationships:**
* An `Episode` has many `Guest`s through `Appearance`.
* A `Guest` has many `Episode`s through `Appearance`.
* An `Appearance` belongs to a `Guest` and belongs to an `Episode`.

## Setup Instructions

Follow these steps to get the project up and running:

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd lateshow-firstname-lastname # Replace with your actual repo name
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Seed Data:**
    Download the `lateshow_episodes.csv` file from the challenge instructions and place it in the root of this project directory (where `seed.py` is located).

5.  **Initialize and run database migrations:**
    ```bash
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
    ```

6.  **Seed the database:**
    ```bash
    python seed.py
    ```
    This script will populate your database with initial data from the `lateshow_episodes.csv` file. If the CSV is not found, it will generate some dummy data.

7.  **Run the Flask application:**
    ```bash
    flask run -p 5555
    ```
    The API will be accessible at `http://localhost:5555`.

## API Endpoints

The following endpoints are available:

| HTTP Method | Endpoint               | Description                                           | Request Body (Example)                               | Response Body (Example)                                          |
| :---------- | :--------------------- | :---------------------------------------------------- | :--------------------------------------------------- | :--------------------------------------------------------------- |
| `GET`       | `/episodes`            | Get a list of all episodes.                           | N/A                                                  | `[{"id": 1, "date": "1/11/99", "number": 1}, ...]`               |
| `GET`       | `/episodes/<int:id>`   | Get details for a specific episode.                   | N/A                                                  | `{"id": 1, "date": "1/11/99", "number": 1, "appearances": [...]}` (with nested guest details) |
| `DELETE`    | `/episodes/<int:id>`   | Delete a specific episode and its appearances.        | N/A                                                  | `{} `(204 No Content) or `{"error": "Episode not found"}` (404) |
| `GET`       | `/guests`              | Get a list of all guests.                             | N/A                                                  | `[{"id": 1, "name": "Michael J. Fox", "occupation": "actor"}, ...]` |
| `POST`      | `/appearances`         | Create a new appearance.                              | `{"rating": 5, "episode_id": 2, "guest_id": 3}`    | `{"id": 162, "rating": 5, "episode_id": 2, "guest_id": 3, "episode": {...}, "guest": {...}}` (201 Created) or `{"errors": ["validation errors"]}` (400/404) |

## Error Handling

* **404 Not Found**: Returned for `GET /episodes/<id>` or `DELETE /episodes/<id>` if the episode does not exist, or for `POST /appearances` if `episode_id` or `guest_id` do not exist.
    ```json
    { "error": "Episode not found" }
    ```
    or
    ```json
    { "errors": ["Episode not found"] }
    ```
* **400 Bad Request**: Returned for `POST /appearances` if validation rules (e.g., rating range) are violated.
    ```json
    { "errors": ["Rating must be between 1 and 5, inclusive."] }
    ```

## Technologies Used

* **Flask**: Web framework.
* **Flask-SQLAlchemy**: ORM for interacting with the database.
* **Flask-Migrate**: Extension for handling SQLAlchemy database migrations with Alembic.
* **Flask-RESTful**: Extension for building REST APIs.
* **SQLAlchemy-Serializer**: Used for easy serialization of SQLAlchemy models to dictionaries.
* **SQLite3**: Default database for development.

## Author

* **Newton Muhindi**
    * [GitHub Profile Link] (e.g., `https://github.com/muhindinewton`)


## License

This project is licensed under the MIT License - see the `LICENSE` file (if you create one) for details.