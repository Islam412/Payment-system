# Paylio Payment System
## Integrated Electronic Payment Platform

## Description

Welcome to Paylio is a comprehensive full-stack payment system designed to facilitate secure and efficient financial transactions. Built on the robust Django framework, it offers a seamless experience for both users and administrators. The system features a user-centric dashboard for fund management, a secure authentication mechanism, and an intuitive back-office admin interface for complete control of operations. This project showcases the integration of modern web technologies to create a reliable financial platform.

## Tech Stack

This project employs a modern and powerful technology stack:

- **Backend Framework**: Python (Django 5.x)
- **API**: Django Rest Framework (DRF)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Database**: SQLite (development), adaptable to PostgreSQL/MySQL
- **Authentication**: Custom `user authentication` with JWT support
- **Admin UI**: `django-jazzmin` for an enhanced administrative experience
- **Utilities**:
  - `django-import-export`
  - `shortuuid`
  - `Pillow`

## Getting Started

To set up the project on your local machine, follow these instructions:

### Prerequisites

- **Python**: Version 3.8 or higher
- **pip**: Python package installer
- **Git**: Version control system

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Islam412/Payment-system.git
   cd payment-system/src
   ```

2. **Set Up Virtual Environment**:
    ```bash
    # For Linux/mac:
    python3 -m venv venv
    source venv/bin/activate

    # For Windows:
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    Install Dependencies:
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

Project Demo
![Home Image](media/reademe_photo/home.png)
![Home Image AR](media/reademe_photo/home_ar.png)

User Dashboard
![User Dashboard Image](media/reademe_photo/dashboard.png)

Admin Interface
![Admin Dashboard Interface Image](media/reademe_photo/admin%20dashboard.png)

Paylio serves as a complete solution for payment processing, demonstrating best practices in full-stack web development. By merging a secure Django backend with a responsive Bootstrap frontend and a feature-rich admin panel, it offers a solid foundation for scalable payment applications. Whether handling user accounts, processing transactions, or managing system data, Paylio is equipped to meet diverse payment application needs.