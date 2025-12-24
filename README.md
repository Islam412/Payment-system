
<img width="1920" height="5290" alt="home" src="https://github.com/user-attachments/assets/564e7494-8429-40ea-b298-bc0cc4004d6d" />


## Description

Paylio is a comprehensive, full-stack payment system designed to facilitate secure and efficient financial transactions. Built using the robust Django framework, it provides a seamless experience for both users and administrators. Key capabilities include a user-centric dashboard for managing funds, a secure authentication system, and a powerful back-office admin interface for total system control. The project highlights the integration of modern web technologies to create a reliable financial platform.

## Tech Stack

This project leverages a modern and powerful technology stack:

*   **Backend Framework**: Python (Django 5.x)
*   **API**: Django Rest Framework (DRF)
*   **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
*   **Database**: SQLite (Development), adaptable to PostgreSQL/MySQL
*   **Authentication**: Custom `userauths` system with JWT support
*   **Admin UI**: `django-jazzmin` for an enhanced administrative experience
*   **Utilities**: `django-import-export`, `shortuuid`, `Pillow`

## Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

*   **Python**: Version 3.8 or higher
*   **pip**: Python package installer
*   **Git**: Version control system

### Installation Steps

1.  **Clone the Repository**
    ```bash
    git clone <your-repo-url>
    cd payment-system/src
    ```

2.  **Set Up Virtual Environment**
    ```bash
    # For Linux/macOS
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup**
    ```bash
    python manage.py migrate
    ```

5.  **Create Admin User**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Server**
    ```bash
    python manage.py runserver
    ```
    Open your browser and navigate to `http://127.0.0.1:8000/`.

## Project Demo

*Explore the core features of the Paylio Payment System.*

### User Dashboard
![User Dashboard Placeholder](path/to/dashboard-screenshot.png)
*(Replace with actual screenshot of the user dashboard)*

### Transaction View
![Transaction Demo Placeholder](path/to/transaction-screenshot.png)
*(Replace with actual screenshot or GIF of a transaction flow)*

## Project Admin

This project utilizes **Django Jazzmin** to provide a sophisticated and user-friendly admin interface.

*   **Customizable Dashboard**: tailored widgets and quick links.
*   **Enhanced Navigation**: Dropdown menus and search functionality.
*   **Theming**: Modern UI with responsive design (currently configured with 'cyborg' theme).
*   **Model Management**: Easy management of `User`, `Account`, and `Core` application models.

Access the admin panel at: `http://127.0.0.1:8000/admin/`

## Project Summary

Paylio stands as a complete solution for payment processing education and implementation. By combining a secure Django backend with a responsive Bootstrap frontend and a feature-rich admin panel, it demonstrates best practices in full-stack web development. Whether for handling user accounts, processing transactions, or managing system data, Paylio offers a solid foundation for a scalable payment application.
