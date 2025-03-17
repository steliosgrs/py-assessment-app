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

### Firebase Setup

1. Create a Firebase project at [https://console.firebase.google.com/](https://console.firebase.google.com/)
2. Enable Email/Password Authentication in the Firebase console
3. Enable Firebase Storage
4. Create a service account key:
   - Go to Project Settings > Service accounts
   - Click "Generate new private key"
   - Save the JSON file as `firebase-credentials.json` in the project root

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Update the Firebase configuration:

   - Place your `firebase-credentials.json` in the project root
   - Update the `FIREBASE_STORAGE_BUCKET` in `docker-compose.yml` with your Firebase project ID

3. Start the application using Docker Compose:

   ```bash
   docker-compose up -d
   ```

4. Access the Streamlit application:
   - Open your browser and navigate to `http://localhost:8501`

### Local Development

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
