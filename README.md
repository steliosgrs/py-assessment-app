# Multi-Framework Web Application with Firebase

This project implements a web application with Firebase authentication (login, register, logout) using two different frameworks:

1. **Streamlit** implementation (complete)
2. **Taipy** implementation (planned for future)

The application uses Firebase Authentication and Firebase Storage, all containerized with Docker.

## Project Structure

```
/project
├── /shared           # Shared components, utilities, Firebase integrations
├── /streamlit_app    # Streamlit implementation
├── /taipy_app        # Taipy implementation (future)
└── /storage          # Shared file storage or handlers
```

## Features

- User authentication (login, register, logout) with Firebase
- Protected content only accessible to logged-in users
- Firebase Storage integration for file uploads
- Docker containerization
- Shared code between different framework implementations

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Firebase project with Authentication and Storage enabled

1. Clone the repository:

```bash
git clone https://github.com/steliosgrs/py-assessment-app.git
cd py-assessment-app
```

2. Update the Firebase configuration:

   - Place your `firebase-credentials.json` in the project root
   - Create a `secrets.toml` under `.streamlit` and add `FIREBASE_API_KEY`.
     (Optional)
   - Update the `FIREBASE_STORAGE_BUCKET` in `docker-compose.yml` with your Firebase project ID

### Firebase Setup

1. Create a Firebase project at [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Enable Email/Password Authentication in the Firebase console
3. Enable Firebase Storage
4. Create a service account key:
   - Go to Project Settings > Service accounts
   - Click "Generate new private key"
   - Save the JSON file as `firebase-credentials.json` in the project root

#### Local Development

For local development without Docker:

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables or update `shared/config.py` with your Firebase configuration.

3. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app/app.py
   ```

#### Docker Installation

Start the application using Docker Compose:

```bash
docker compose up -d
```

#### Development Server

Access the Streamlit application:

- Open your browser and navigate to `http://localhost:8501`

Access the MongoDB server (if using MongoDB):

- MongoDB Compass or any MongoDB client can connect to `http://localhost:8080/`

## Security Considerations

- Keep your Firebase credentials secure and never commit them to version control
- Use environment variables for sensitive information
- Set up Firebase Security Rules for Storage and Firestore
- Enable Firebase Authentication security features like email verification
- Use HTTPS in production

## Future Enhancements

- Complete Taipy implementation
- Add user profile management
- Implement password reset functionality
- Add email verification
- Implement user roles and permissions
- Add more Firebase features like Firestore for storing application data

## New Structure

Following the Repository Pattern, the project structure has been updated to:

```
/project_root/
├── shared/
│   ├── __init__.py
│   ├── config.py                      # Configuration settings
│   │
│   ├── database/                      # NEW: Database layer
│   │   ├── __init__.py               # Exports repositories based on ENV
│   │   │
│   │   ├── repositories/             # Repository interfaces (contracts)
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py    # IUserRepository (abstract)
│   │   │   ├── module_repository.py  # IModuleRepository (abstract)
│   │   │   └── exercise_repository.py # IExerciseRepository (abstract)
│   │   │
│   │   ├── firestore/                # Firestore implementations
│   │   │   ├── __init__.py
│   │   │   ├── connection.py         # Firestore client setup
│   │   │   ├── user_store.py         # FirestoreUserStore
│   │   │   ├── module_store.py       # FirestoreModuleStore
│   │   │   └── exercise_store.py     # FirestoreExerciseStore
│   │   │
│   │   └── mongodb/                  # MongoDB implementations
│   │       ├── __init__.py
│   │       ├── connection.py         # MongoDB client setup
│   │       ├── user_store.py         # MongoUserStore
│   │       ├── module_store.py       # MongoModuleStore
│   │       └── exercise_store.py     # MongoExerciseStore
│   │
│   ├── course_loader.py              # MODIFIED: Now uses repositories
│   ├── exercise_runner.py            # Testing utilities (unchanged)
│   └── markdown_converter.py         # Markdown utilities (unchanged)
│
├── streamlit_app/
│   ├── __init__.py
│   ├── app.py                        # MODIFIED: Uses repository layer
│   └── pages/
│       ├── __init__.py
│       ├── login.py                  # MODIFIED: Uses UserRepository
│       ├── register.py               # MODIFIED: Uses UserRepository
│       ├── modules.py                # MODIFIED: Uses ModuleRepository
│       └── exercises.py              # MODIFIED: Uses ExerciseRepository
│
├── docker-compose.yml                # UPDATED: Adds MongoDB service
├── requirements.txt                  # UPDATED: Adds pymongo
└── .env                              # ENV variables (DATABASE=firestore|mongodb)
```

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Application                     │
│                  (app.py, pages/*.py)                        │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ Uses repositories via interface
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              Repository Layer (Interfaces)                   │
│    IUserRepository | IModuleRepository | IExerciseRepository│
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┴──────────────┐
        │                             │
        ↓                             ↓
┌──────────────────┐         ┌──────────────────┐
│ Firestore Stores │         │  MongoDB Stores  │
│  (Production)    │         │  (Development)   │
└─────────┬────────┘         └────────┬─────────┘
          │                           │
          ↓                           ↓
    [Firebase Cloud]            [MongoDB Container]
```

## Environment Variables

```
# Development
DATABASE=mongodb
MONGODB_URI=mongodb://localhost:27017
MONGODB_NAME=python_learning_dev

# Production
DATABASE=firestore
FIREBASE_CREDENTIALS=firebase-credentials.json
FIREBASE_API_KEY=your-api-key

```

https://github.com/haohanyang/compass-web
