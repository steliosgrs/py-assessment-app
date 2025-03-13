# Multi-Framework Web Application

This project implements a web application with authentication (login, register, logout) using two different frameworks:

1. **Streamlit** implementation (complete)
2. **Taipy** implementation (planned for future)

The application uses PostgreSQL for user data storage and is containerized with Docker.

## Project Structure

```
/project
├── /shared           # Shared components, utilities, database models
├── /streamlit_app    # Streamlit implementation
├── /taipy_app        # Taipy implementation (future)
└── /storage          # Shared file storage or handlers
```

## Features

- User authentication (login, register, logout)
- Protected content only accessible to logged-in users
- PostgreSQL database integration
- Docker containerization
- Shared code between different framework implementations

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Start the application using Docker Compose:

   ```bash
   docker-compose up -d
   ```

3. Access the Streamlit application:
   - Open your browser and navigate to `http://localhost:8501`

### Local Development

For local development without Docker:

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Set up a PostgreSQL database and update the connection details in the environment variables or `shared/db.py`.

3. Run the Streamlit application:
   ```bash
   streamlit run streamlit_app/app.py
   ```

## Security Considerations

- Change the `SECRET_KEY` in the Docker Compose file for production
- Use HTTPS in production
- Consider implementing rate limiting for login attempts
- Store passwords securely (already implemented with password hashing)

## Future Enhancements

- Complete Taipy implementation
- Add user profile management
- Implement password reset functionality
- Add email verification
- Implement user roles and permissions
