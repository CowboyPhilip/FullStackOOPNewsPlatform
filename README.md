# 🧠 OOP-FastAPI Backend

## 📌 Overview

`oop-fastapi-backend` is a scalable, modular, and secure **Object-Oriented Programming (OOP)** backend system built using **FastAPI**. Designed with **SOLID** principles, this project demonstrates advanced backend architecture tailored for **maintainability**, **testability**, and **real-world production** use cases.  

Whether you're a beginner trying to understand FastAPI through structure or a professional looking for reusable OOP architecture — this repo serves both purposes.


> 🧩 **Note:**

---

## 🎯 Purpose

The primary goal of this repository is to **teach and implement FastAPI the right way** using clean OOP patterns. It demonstrates:

- OOP design in Python backend development
- SOLID principles in FastAPI applications
- Real-world features like authentication, email sending, JWT tokens, and middleware
- A clean, layered, and maintainable project structure
- A powerful **path aliasing system** for modular architecture
- Deep exploration of OOP concepts
- Practical implementation of design patterns and system design

---


## 🚀 You’ll Learn:

### 🔹 1. How to Isolate Concerns with Services and Controllers
- Understand the separation of business logic (`Services`) from HTTP handling (`Controllers`) to write clean, maintainable code.
- Learn how each service class handles specific business responsibilities while controllers remain thin and focused on request/response mapping.

### 🔹 2. How to Define and Use DTOs with Pydantic
- Design clear data contracts using **Pydantic** models (also called DTOs – Data Transfer Objects).
- Validate incoming and outgoing data effectively.
- Structure schemas for `Create`, `Update`, and `Read` operations following SOLID principles.

### 🔹 3. How to Use ODMantic with MongoDB
- Leverage **ODMantic**, an async ODM built on Pydantic, to define MongoDB models and interact with the database.
- Use features like `find_one`, `find`, and `model_validate_doc()` to query MongoDB asynchronously with ease.
- Learn how to structure and validate data at the model level.

### 🔹 4. How to Implement Token Authentication Securely
- Master authentication flows with **OAuth2PasswordBearer** and JWTs.
- Secure endpoints using access tokens and refresh tokens.
- Refresh expired tokens automatically using middleware.
- Protect routes with role-based and permission-based access control.
- Giving roles while creating users with *FACTORY* design pattern

### 🔹 5. How to Build and Send Real Emails with Templates
- Use **Jinja2** templating and **emails** or **smtplib** to craft professional HTML emails.
- Implement the **Command Behavioral Design Pattern** for reusable email commands (e.g., OTP, email verification).
- Configure SMTP settings and abstract email logic from controllers and services.

### 🔹 6. How to Structure a Production-Grade FastAPI App
- Organize your FastAPI app using industry-standard folder structure with OOP principles.
- Apply **SOLID principles** (especially Single Responsibility & Dependency Inversion) for better scalability.
- Implement configuration management using a `config.py` or `.env` files with validation.

### 🔹 7. How to Manage Dependencies Cleanly with FastAPI
- Use `Depends()` to inject services, authenticated user objects, or parsed headers.
- Centralize shared logic (like database or authentication) with dependency injection.

### 🔹 8. How to Handle Errors and Exceptions Gracefully
- Use try-except blocks to catch and manage runtime errors.
- Raise **FastAPI HTTPException** with proper status codes and messages.
- Create global exception handlers for consistent API error responses.

### 🔹 9. How to Version Your API
- Implement **API versioning** (e.g., `/api/v1`, `/api/v2`) to support backward compatibility and better maintainability.

### 🔹 10. How to Use Middleware for Auth and Header Management
- Build middleware that automatically:
  - Deserializes and attaches user info from access tokens.
  - Updates headers like `Authorization` or custom ones (`x-refresh`) in every request.

### 🔹 11. How to Secure User Passwords and JWTs
- Hash and verify passwords using **Passlib** (`bcrypt` , `argon2` hashing scheme).
- Sign and verify JWT tokens securely using **Python-JOSE**.
- Manage token expiry and refresh lifecycle effectively.

### 🔹 12. How to Design Singleton Database Connection
- Use the **Singleton Design Pattern** to maintain a single database engine instance across your app.
- Avoid duplicate connections and improve performance in production.


---

## 📁 Folder Aliases (tsconfig.json)

```json
"paths": {
  "main": ["app/main.py"],
  "server": ["server/main.py"],
  "config": ["app/config"],
  "db": ["app/db"],
  "controllers/*": ["controllers/*"],
  "templates/*": ["templates/*"],
  "interfaces/*": ["interfaces/*"],
  "middlewares/*": ["middlewares/*"],
  "models/*": ["models/*"],
  "routes/*": ["routes/*"],
  "schemas/*": ["schemas/*"],
  "services/*": ["services/*"],
  "utils/*": ["utils/*"],
}
```

## 🧱 Technologies & Packages

| Tool / Package        | Purpose                                                                 |
|-----------------------|-------------------------------------------------------------------------|
| `FastAPI`             | High-performance web framework                                          |
| `uvicorn`             | ASGI server to run FastAPI app                                          |
| `odmantic`            | ODM for MongoDB (based on pydantic)                                     |
| `pydantic`            | Data validation and settings management                                 |
| `passlib[bcrypt]`     | Secure password hashing                                                 |
| `python-jose`         | JWT encoding, decoding, and verification                                |
| `jinja2`              | HTML templating engine for emails                                       |
| `emails`              | Email sending via SMTP                                                  |
| `python-dotenv`       | Environment variable management                                         |
| `typing`              | For type checking and linting errors                                    |
| `motor.motor_asyncio` | MongoDB client connection interface                                     |

---

## 🏗️ Core Components & Structure

| Folder / File         | Description                                                                 |
|-----------------------|-----------------------------------------------------------------------------|
| `app/main.py`         | App entry point – sets up app, middleware, and starts server                |
| `app/config/`         | Environment config management using `pydantic.BaseSettings`                 |
| `app/db/mongo.py`     | MongoDB connection using **singleton pattern** with ODMantic                |
| `app/models/`         | ODMantic models representing MongoDB schemas                                |
| `app/interfaces/`     | Interface definitions for controllers and routes                            |
| `app/services/`       | Business logic (service layer)                                              |
| `app/controllers/`    | Handles interactions between services and routers                           |
| `app/routes/`         | API endpoints using class-based routes                                      |
| `app/schemas/`        | Pydantic request/response DTOs                                              |
| `app/utils/`          | Helpers (e.g., password hashing, JWT, OTP, etc.)                            |
| `app/middleware/`     | Custom middleware for serialization and token handling                      |
| `app/templates/`      | Jinja2 HTML templates for emails                                            |
| `app/utils/emails`    |  Email command Invoker + SMTP implementation                                |


---

## 🧪 Key Features

### ✅ Routes & Class-Based Views
All routes are defined inside classes and registered through custom routers for modularity.

### ✅ Config Management
All config values (DB URI, secret keys, SMTP credentials) are read from `.env` via `pydantic.BaseSettings`.

### ✅ Singleton DB Connection
MongoDB connection via ODMantic is implemented using a singleton pattern to avoid redundant connections.

### ✅ Interfaces
All controllers and routes implement interfaces to enforce contracts and reusability.

### ✅ Models (ODMantic)
MongoDB models are defined using ODMantic, which combines `pydantic` with MongoDB modeling.

### ✅ Email Sending with Templating
- Command Design Pattern used to send emails
- `jinja2` used to render OTP, verification emails
- `emails` package used to send via SMTP

### ✅ Authentication
- Secure login using **OAuth2PasswordBearer**
- **JWT tokens** signed/verified using `python-jose`
- Token middleware injects user data into request context
- Passwords are hashed using **`passlib[bcrypt]`**

### ✅ Exception Handling
- Business logic is wrapped in `try/except`
- Custom FastAPI exceptions raised with meaningful messages

### ✅ Middleware
- Serializes JWT payloads
- Validates and embeds user in request
- Embeds headers like tokens automatically

### ✅ API Versioning
Support for clean versioning via prefixes like `/api/v1`, enabling scalable API evolution

---

## 🔐 Security Features

- Token-based auth via `OAuth2PasswordBearer`
- Password hashing via `bcrypt, argon2`
- JWT signed with a secret key and verified on every request
- Role-based permission system with middleware

---


## 🚀 Running the Project

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/Omsmir/fastapi-oop-backend.git
cd fastapi-oop-backend
```

### ✅ 2. Create `.env` File

```env
MONGO_USER='mongo user'
MONGO_PASS='mongo db pass'
MONGO_HOST=localhost
MONGO_PORT=27017
DB_NAME=fastapi

SMTP_USER='example@gmail.com'
SMTP_PASSWORD='app password'

EMAILS_FROM_EMAIL='example@gmail.com'
EMAILS_FROM_NAME='project name'

ACCESSTOKENPRIVATEKEY='ACCESSTOKENPRIVATEKEY'
ACCESSTOKENPUBLICKEY='ACCESSTOKENPUBLICKEY'
REFRESHTOKENPRIVATEKEY='REFRESHTOKENPRIVATEKEY'
REFRESHTOKENPUBLICKEY='REFRESHTOKENPUBLICKEY'

BACKEND_CORS_ORIGINS="http://localhost,http://localhost:3000"
```

### ✅ 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### ✅ 4. Run the Server

```bash
uvicorn app.main:app --reload
```

---

## 📫 API Access & Authentication

- All protected routes require an `Authorization: Bearer <token>` header.
- Use `/auth/login` to get JWT tokens.
- Token is verified and decoded in middleware before each request.

---

## 📘 Learn by Structure

This repo is built to **teach developers** how to structure scalable FastAPI projects using OOP and design principles.


---


## 💡 Contributions

PRs, suggestions, and improvements are welcome!

---

## 🧑‍💻 Author

**Omar [@omsmir]**

---

## 📜 License

MIT License