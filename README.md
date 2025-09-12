# Wellness Tracker API

## Overview
The Wellness Tracker API is a robust backend service designed to help users log and manage personal wellness activities. The core purpose of this API is to 
provide a digital journal for tracking daily habits, workouts, and recipes, offering a foundation for a comprehensive wellness application. This project 
serves as a practical demonstration of building a RESTful API from the ground up, with a focus on core backend principles, including database management, user 
authentication, and API endpoint design.

## Features
### Current Functionality
- **User Management:** Secure user registration, authentication, and login using JWT (JSON Web Tokens).
   - `POST /v1/users/:` Creates a new user.
   - `POST /v1/users/token:` Authenticates a user and returns a JWT access token.
- **Habit Tracking:** CRUD (Create, Read, Update, Delete) operations for managing a user's habits. Each habit is securely tied to a specific user, ensuring data privacy.
   -  `POST /v1/habits/:` Creates a new habit for the authenticated user.
   - `GET /v1/habits/:` Retrieves all habits for the authenticated user.
   - `GET /v1/habits/{habit_id}:` Retrieves a specific habit by its ID.
   - `PUT /v1/habits/{habit_id}:` Updates a specific habit.
   - `DELETE /v1/habits/{habit_id}:` Deletes a specific habit.
### Future Enhancements
- **Workout Management:** Endpoints for logging and tracking various workout routines, including resistance training, cardio and more.
- **Recipe Journal:** Functionality to save and manage sustainable recipes for easy future references.
- **Progress Visualization:** API endpoints to provide aggregated data and statistics for user habits and workouts.
### Technology Stack
- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migration:** Alembic
- **Authentication:** `passlib` (for password hashing), `python-jose` (for JWT)
- **Hosting:** Render (for web service and database hosting)
### CI/CD and Testing
This project leverages a CI/CD (Continuous Integration/Continuous Deployment) pipeline using **GitHub Actions**. Upon every push to the main branch, a workflow is triggered to automatically run a suite of tests and deploy the application to Render.
API endpoints are thoroughly tested using a dedicated `tests/` folder to ensure reliability and correct functionality before deployment.

## Getting Started (Local Development)
This section guides a new developer on how to set up and run the API on their local machine. 
### Prerequisites
- Python 3.10+
- A running PostgreSQL instance (e.g., via Docker or a local installation)
### Setup Instructions
1. **Clone the repository:**
   ```
   git clone https://github.com/your-username/wellness-tracker-api.git
   cd wellness-tracker-api
   ```
2. **Create and activate a virtual environment:**
   ```
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On macOS/Linux
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Create a `.env` file in the project root.
   - Add your PostgreSQL database URL.
   - Add your secret key. (e.g., use the `secrets` module)
   ```
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
   - For example:
   ```
   DATABASE_URL="postgresql://user:password@localhost/dbname"
   SECREY_KEY="your-super-secret-key-goes-here"
   ```
5. **Run database migrations:**
   ```
   alembic upgrade head
   ```
6. **Start the application:**
   ```
   uvicorn app.main:app --reload
   ```
   Your API will now be running at http://localhost:8000. You can access the interactive API documentation at http://localhost:8000/docs.
