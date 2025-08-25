# School Management System Backend

This is the backend for the School Management System, built using FastAPI, SQLite, and SQLAlchemy. The backend provides a RESTful API for managing students (Aluno) and classes (Turma).

## Project Structure

```
backend/
├── app/
│   ├── main.py          # Entry point for the FastAPI application
│   ├── models.py        # SQLAlchemy models for database entities
│   ├── schemas.py       # Pydantic schemas for data validation
│   ├── database.py      # Database connection and session management
│   ├── crud.py          # CRUD operations for database interaction
│   └── routes.py        # API endpoints for managing entities
├── requirements.txt      # List of dependencies for the backend
└── README.md             # Documentation for the backend
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd school-management-system/backend
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

## API Usage

The backend provides the following endpoints:

- **GET /alunos**: Retrieve a list of all students.
- **POST /alunos**: Create a new student.
- **GET /alunos/{id}**: Retrieve a specific student by ID.
- **PUT /alunos/{id}**: Update a specific student by ID.
- **DELETE /alunos/{id}**: Delete a specific student by ID.

- **GET /turmas**: Retrieve a list of all classes.
- **POST /turmas**: Create a new class.
- **GET /turmas/{id}**: Retrieve a specific class by ID.
- **PUT /turmas/{id}**: Update a specific class by ID.
- **DELETE /turmas/{id}**: Delete a specific class by ID.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.