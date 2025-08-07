# AI-Powered Resume and Interview Platform

> A comprehensive, multi-layered application for user management, resume analysis, and interview preparation, powered by Google Gemini and integrated with Google Drive.

---

## 📖 Table of Contents
* [Introduction](#-introduction)
* [Features](#-features)
* [Technology-Stack](#-technology-stack)
* [Architecture-Overview](#️-architecture-overview)
* [Getting-Started](#️-getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Configuration](#configuration)
* [API-Endpoints](#-api-endpoints)
* [Contributing](#-contributing)
* [License](#-license)
* [Contact](#-contact)

## 🚀 Introduction
This project is a multi-layered application designed to provide a robust suite of tools for career development. It leverages a microservice-inspired architecture to handle various functionalities such as user authentication, profile management, AI-driven resume analysis, and mock interview services. The system is built with Python and FastAPI for high performance, and its modular design ensures that components can be developed, scaled, and maintained independently.

## ✨ Features
* **Secure User Authentication**: Robust user registration, login, and session management using a dedicated Auth module.
* **User Profile & Resume Management**: Create, update, and manage user profiles. Upload resumes directly to Cloudinary for storage and processing.
* **AI-Powered Resume Analysis**: Integrates with **Google Gemini** to provide deep, intelligent analysis of uploaded resumes.
* **Asynchronous Interview Services**: A dedicated router to handle interview-related tasks and analysis, also powered by the AI service.
* **Google Drive Integration**: Seamlessly connects with Google Drive using OAuth2 for file-related operations.
* **Email Notifications**: Utilizes the **Brevo Email API** for sending automated emails for authentication and other notifications.
* **Robust Data Persistence**: Employs PostgreSQL with SQLAlchemy ORM for efficient, reliable data storage and retrieval.

## 💻 Technology Stack

| Category              | Technology/Service                                                                                             |
| --------------------- | -------------------------------------------------------------------------------------------------------------- |
| **Backend** | Python, FastAPI                                                                                                |
| **Database** | PostgreSQL                                                                                                     |
| **ORM & Validation** | SQLAlchemy, Pydantic                                                                                           |
| **AI Service** | Google Gemini AI                                                                                               |
| **File Storage** | Google Drive, Cloudinary                                                                                       |
| **Email Service** | Brevo Email API (via SMTP)                                                                                     |
| **Frontend** | Static HTML/CSS/JS (`index.html`)                                                                              |
| **Deployment** | Vercel (Frontend), [Your Backend Host, e.g., Render, AWS]                                                      |

## 🗺️ Architecture Overview
The application follows a layered architectural pattern for separation of concerns and maintainability.

* **Presentation Layer**:
    * **FastAPI API Gateway**: The single entry point for all incoming HTTP requests. It directs traffic to the appropriate router.
    * **Routers** (`Auth`, `User Profile & Resume`, `Interview`): Handle specific business logic for different endpoints. They depend on and use the underlying business services.

* **Business Services Layer**:
    * This layer contains the core logic of the application.
    * **Auth Module**: Manages all user authentication logic.
    * **Google Drive Service**: Encapsulates all interactions with the Google Drive API, including OAuth2 handling.
    * **AI Analysis Service**: A dedicated service that communicates with the **Google Gemini AI** to perform complex analytical tasks.
    * **Email Service**: Interfaces with the Brevo Email API to send emails.
    * **Cloudinary Service**: Manages resume uploads and storage via its SDK.

* **Persistence Layer**:
    * **Database Config & Session**: Manages the connection pool and sessions to the PostgreSQL database.
    * **ORM Models & CRUD Operations**: Defines the database tables as Python objects and provides Create, Read, Update, Delete operations.
    * **Pydantic Schemas**: Ensures strict data validation and serialization for API requests and responses.

* **External Dependencies**:
    * The application relies on several powerful third-party APIs: **PostgreSQL**, **Brevo Email API**, **Cloudinary API**, **Google Drive API**, and **Google Gemini AI**.

## 🛠️ Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites
* Python 3.9+
* PostgreSQL Server
* A Google Cloud Platform project with the **Google Gemini API** and **Google Drive API** enabled.
* A Cloudinary account for API keys.
* A Brevo (formerly Sendinblue) account for SMTP credentials.

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/your-repo.git](https://github.com/your-username/your-repo.git)
    cd your-repo
    ```

2.  **Create and activate a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up the PostgreSQL database:**
    Ensure you have a running PostgreSQL instance and create a new database for this project.

### Configuration

1.  Create a `.env` file in the root directory of the project.
2.  Add the following environment variables to the `.env` file with your specific credentials. This file is listed in `.gitignore` and should not be committed to source control.

    ```env
    # PostgreSQL Database
    DATABASE_URL="postgresql://YOUR_DB_USER:YOUR_DB_PASSWORD@YOUR_DB_HOST:5432/YOUR_DB_NAME"

    # Google Gemini API
    GOOGLE_GEMINI_API_KEY="your_google_gemini_api_key"

    # Google OAuth2 for Drive API
    GOOGLE_CLIENT_ID="your_google_client_id.apps.googleusercontent.com"
    GOOGLE_CLIENT_SECRET="your_google_client_secret"

    # Cloudinary
    CLOUDINARY_URL="cloudinary://api_key:api_secret@cloud_name"

    # Brevo Email SMTP
    BREVO_SMTP_HOST="smtp-relay.brevo.com"
    BREVO_SMTP_PORT=587
    BREVO_SMTP_USER="your_brevo_email@example.com"
    BREVO_SMTP_PASSWORD="your_brevo_smtp_password"

    # JWT Secret Key
    SECRET_KEY="your_super_secret_key_for_jwt"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES=30
    ```

### Running the Application

1.  **Run the FastAPI server:**
    ```sh
    uvicorn main:app --reload
    ```
    The `--reload` flag enables hot-reloading for development.

2.  The API will be available at `http://127.0.0.1:8000`.

## 📋 API Endpoints
The API documentation is automatically generated by FastAPI using Swagger UI and ReDoc.

* **Swagger UI**: `http://127.0.0.1:8000/docs`
* **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🤝 Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

## 📄 License
This project is licensed under the MIT License - see the `LICENSE.md` file for details.

## 📧 Contact
Suchith Narayan - **suchithnarayan05@gmail.com**

Project Link: https://github.com/Sagar369r/jri-v2.git
