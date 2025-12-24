# Paylio - Payment System

Paylio is a robust, full-stack payment system built with Django. It features a comprehensive user dashboard, secure authentication, and a powerful admin interface optimized for managing financial transactions and user accounts.

## 🚀 Features

*   **Secure Authentication**: Custom user authentication system (`userauths`).
*   **User Dashboard**: Interactive dashboard for managing accounts and transactions.
*   **Admin Interface**: Enhanced admin UI using `django-jazzmin` for easy management.
*   **Multi-language Support**: Built-in support for Arabic (`ar`) and English (`en`).
*   **REST API**: API endpoints powered by **Django Rest Framework** (DRF).
*   **Modern UI**: utilizing **Bootstrap 5** for a responsive design.

## 🛠 Tech Stack

*   **Backend**: Python, Django 5.x
*   **API**: Django Rest Framework (DRF)
*   **Database**: SQLite (default), extensible to PostgreSQL/MySQL
*   **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
*   **Utilities**: `django-import-export`, `django-filter`, `shortuuid`

## 📦 Installation

Follow these steps to set up the project locally.

### Prerequisites

*   Python 3.8+
*   pip (Python package manager)

### Steps

1.  **Clone the repository**
    ```bash
    git clone <repository-url>
    cd payment-system/src
    ```

2.  **Create and activate a virtual environment**
    ```bash
    # Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (Admin)**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server**
    ```bash
    python manage.py runserver
    ```

    Access the application at `http://127.0.0.1:8000/`.

## 📂 Project Structure

*   `account/`: Manages user accounts and balances.
*   `core/`: Core functionalities and business logic.
*   `userauths/`: Custom user authentication and profile management.
*   `templates/`: HTML templates.
*   `static/`: Static assets (CSS, JS, Images).
*   `media/`: User-uploaded media files.

## 🛡 License

This project is licensed for personal and educational use.
