# MuscleForge AI

AI-Powered Fitness Web Application - Build muscle, lose fat, and track your progress with intelligent guidance.

## Features

- 🤖 **AI Personal Coach** - Powered by Groq API with Llama 3.3 70B
- 📊 **Progress Tracking** - Weight, measurements, photos
- 🥗 **Nutrition Planner** - Indian diet with macros tracking
- 💪 **Workout Plans** - Home and gym workouts
- 📈 **Analytics** - Charts and insights
- 🏆 **Challenges** - 30/60/90 day challenges with XP system
- 📝 **Blog** - Fitness articles and tips
- 📱 **Responsive Design** - Works on all devices

## Tech Stack

### Backend
- Python 3.13
- Django 5.0.6
- Django REST Framework
- SQLite (Development) / PostgreSQL (Production)
- Groq API for AI

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Chart.js
- ApexCharts
- JavaScript

### Deployment
- Docker
- Docker Compose
- Gunicorn
- Nginx
- Redis (Caching)

## Quick Start

### Prerequisites
- Python 3.13+
- Node.js (for frontend)
- Docker & Docker Compose (optional)

### Installation

#### Option 1: Direct Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/muscleforge-ai.git
cd muscleforge

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load initial data
python manage.py loaddata muscle_groups.json
python manage.py loaddata food_categories.json
python manage.py loaddata foods.json
python manage.py loaddata exercises.json

# Run development server
python manage.py runserver
```

#### Option 2: Docker

```bash
# Copy environment file
cp .env.example .env
# Edit .env with your settings

# Build and run
docker-compose up --build

# Or run in detached mode
docker-compose up -d --build
```

## Environment Variables

Create a `.env` file in the root directory:

```env
# Environment
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Groq AI
GROQ_API_KEY=your-groq-api-key-here

# Email
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Security (Production)
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
```

## Project Structure

```
muscleforge/
├── apps/
│   ├── accounts/      # User authentication & profiles
│   ├── ai_coach/      # AI chat & recommendations
│   ├── analytics/     # Analytics & habit tracking
│   ├── api/           # REST API endpoints
│   ├── blog/          # Blog posts
│   ├── challenges/    # Challenges & achievements
│   ├── dashboard/     # Main dashboard
│   ├── nutrition/     # Nutrition & meal tracking
│   ├── progress/      # Progress tracking
│   └── workout/       # Workout plans & exercises
├── muscleforge_project/
│   ├── settings.py    # Django settings
│   ├── urls.py        # URL routing
│   └── wsgi.py        # WSGI configuration
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User uploads
├── fixtures/          # Initial data
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## AI Features

The AI Coach can help with:
- Personalized workout plans
- Diet plans (Indian & budget-friendly)
- Exercise form guidance
- Supplement advice
- Recovery & sleep optimization
- Motivation & mindset

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Powered by [Groq API](https://groq.com/)
- Built with [Django](https://www.djangoproject.com/)
- UI components from [Bootstrap](https://getbootstrap.com/)

## Support

For issues and questions, please open an issue on GitHub.

---

Made with ❤️ for fitness enthusiasts
