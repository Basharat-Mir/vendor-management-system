# Vendor Management System

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Basharat908/vendor-management-system.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd vendor-management-system
    ```

3. **Set up a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment:**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

5. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

6. **Run migrations:**

    ```bash
    python manage.py migrate
    ```

7. **Create a superuser (if applicable):**

    ```bash
    python manage.py createsuperuser
    ```

8. **Run Server:**

    ```bash
    python manage.py runserver
    ```

9. **Access Swagger APIs:**

    [Swagger API Documentation](http://localhost:8000/swagger/)

10. **Access Swagger Redoc:**

    [Swagger Redoc Documentation](http://localhost:8000/redoc/)


11. **To run tests:**
     python manage.py test