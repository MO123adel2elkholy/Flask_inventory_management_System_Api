# Flask Inventory Management System API

A comprehensive, modular REST API for inventory management built with Flask. This project demonstrates production-level Flask development with database migrations, background task processing, admin interfaces, rate limiting, and GraphQL support.

## 🎯 Overview

This Flask application provides a scalable inventory management system with the following capabilities:
- RESTful API endpoints for inventory operations
- Database migrations and ORM support
- Asynchronous task processing (email, image processing, etc.)
- Scheduled background jobs
- Admin dashboard for database management
- GraphQL API support
- Request rate limiting
- Social authentication integration

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Web Framework** | Flask |
| **Database** | SQLAlchemy + Alembic |
| **Serialization** | Marshmallow / apifairy |
| **Task Queue** | Celery |
| **Task Scheduler** | Celery Beat / RedBeat |
| **Admin Interface** | Flask-Admin |
| **GraphQL** | Ariadne |
| **Rate Limiting** | Flask-Limiter |
| **Authentication** | Flask-Dance (social auth) |
| **Code Formatting** | Ruff |
| **Message Broker** | Redis |

## 📋 Prerequisites

- **OS**: Windows 10/11
- **Python**: 3.9 or higher
- **Git**: For version control
- **Redis**: For Celery broker (optional but recommended)

## 🚀 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd Flask_inventory_management_System_Api
```

### 2. Create Virtual Environment

**Command Prompt:**
```bash
python -m venv venv
venv\Scripts\activate
```

**PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:
```env
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=sqlite:///inventory.db
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
DEBUG=True
```

## 📁 Project Structure

```
Flask_inventory_management_System_Api/
├── app/                          # Main application package
│   ├── __init__.py              # Factory function: create_app()
│   ├── models/                  # SQLAlchemy models
│   ├── routes/                  # Blueprint routes
│   ├── schemas/                 # Marshmallow schemas
│   ├── services/                # Business logic
│   └── tasks/                   # Celery background tasks
├── migrations/                  # Alembic migration files
├── tests/                       # Unit & integration tests
├── config.py                    # Configuration (Dev, Prod, Test)
├── make_celery.py               # Celery factory
├── requirements.txt             # Dependencies
├── Flask_Notes.md               # Project documentation
└── README.md                    # This file
```

## 🏗️ Architecture Highlights

### Factory Pattern
The `create_app()` function in `app/__init__.py` follows Flask's factory pattern:
- Supports multiple configurations (Development, Production, Testing)
- Enables code isolation and maintainability
- Separates concerns: business logic from configuration

### Blueprints
Routes are organized as modular blueprints for:
- Better code organization
- Easy feature addition
- Scalability for large projects

### Database Migrations
Alembic (via Flask-Migrate) manages schema changes:
- Version control for database
- Rollback capability
- Safe production deployments

## 🚀 Running the Application

### Start Flask Development Server
```bash
flask --app app run
```

Or with Python module:
```bash
python -m flask --app app run
```

Access API at: `http://localhost:5000`

## 🗄️ Database Management

### Initialize Migrations
```bash
flask db init
```

### Create Migration After Model Changes
```bash
flask db migrate -m "Add inventory table"
```

### Apply Migrations
```bash
flask db upgrade
```

### Rollback Migration
```bash
flask db downgrade
```

## 🔄 Background Tasks (Celery)

### Start Celery Worker
Process long-running tasks (email, image processing, etc.):
```bash
celery -A make_celery worker --pool=solo --loglevel=INFO
```

### Schedule Tasks with Celery Beat
Run tasks at specified intervals:
```bash
celery -A make_celery beat --loglevel=INFO
```

### Dynamic Scheduling with RedBeat
For production with dynamic schedules (e.g., user-defined):
```bash
celery -A make_celery beat -S redbeat.RedBeatScheduler --loglevel=INFO
```

## 📊 Admin Interface

Access Flask-Admin dashboard at: `http://localhost:5000/admin`

Features:
- CRUD operations on database models
- Filtering and searching
- Bulk actions
- User-friendly interface for non-technical staff

## 🔐 Code Quality & Formatting

### Configure Ruff in VS Code

Add to `.vscode/settings.json`:
```json
{
  "[python]": {
    "editor.formatOnSave": true,
    "editor.defaultFormatter": "charliermarsh.ruff"
  }
}
```

### Run Linting & Formatting
```bash
ruff check .
ruff format .
```

## 🧪 Testing

Run unit and integration tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=app
```

## 📚 API Documentation

### RESTful Endpoints
Documented via Marshmallow schemas and apifairy decorators.

### GraphQL API (Optional)
Available at `/graphql` when Ariadne is integrated.

### Rate Limiting
Protected endpoints with Flask-Limiter to prevent brute force attacks:
```python
@limiter.limit("10 per minute")
def my_endpoint():
    pass
```

## 🔐 Authentication

### Social Authentication
Configured via Flask-Dance for:
- GitHub
- Google
- Other OAuth 2.0 providers

Setup environment variables:
```env
GITHUB_OAUTH_CLIENT_ID=xxx
GITHUB_OAUTH_CLIENT_SECRET=xxx
GOOGLE_OAUTH_CLIENT_ID=xxx
GOOGLE_OAUTH_CLIENT_SECRET=xxx
```

## 🚨 Security Best Practices

1. **Environment Variables**: Never commit `.env` file
2. **Secret Key**: Use strong, random `SECRET_KEY`
3. **Database**: Use connection pooling in production
4. **CORS**: Configure CORS policies as needed
5. **Rate Limiting**: Enable on public endpoints
6. **Input Validation**: Use Marshmallow schemas

## 📝 Common Development Tasks

| Task | Command |
|------|---------|
| Run dev server | `flask --app app run` |
| Create migration | `flask db migrate -m "message"` |
| Apply migrations | `flask db upgrade` |
| Start Celery worker | `celery -A make_celery worker --pool=solo --loglevel=INFO` |
| Start Celery beat | `celery -A make_celery beat --loglevel=INFO` |
| Run tests | `pytest` |
| Format code | `ruff format .` |
| Check linting | `ruff check .` |
| Access admin | `http://localhost:5000/admin` |

## 🐛 Troubleshooting

### Redis Connection Error
Ensure Redis is running:
```bash
redis-cli ping
```

### Database Lock Error
Reset database:
```bash
flask db downgrade base
flask db upgrade
```

### Celery Tasks Not Processing
Check worker logs and ensure broker is accessible.

## 📖 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Celery Documentation](https://docs.celeryproject.io/)
- [Marshmallow Serialization](https://marshmallow.readthedocs.io/)
- [Alembic Migrations](https://alembic.sqlalchemy.org/)

## 👥 Contributing

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Commit changes: `git commit -m "Add feature"`
3. Run tests and linting before push
4. Submit pull request

## 📄 License

[Specify your license here - MIT, Apache 2.0, etc.]

## ✉️ Support

For issues, questions, or contributions, please open an issue on the repository.

---

**Last Updated**: April 27, 2026
