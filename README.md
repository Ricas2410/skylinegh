# Skyline Ghana Constructions

A modern, professional website for Skyline Ghana Constructions - a leading construction company in Ghana specializing in residential, commercial, and industrial projects.

## 🏗️ Features

- **Modern Design**: Clean, professional interface built with Django and Tailwind CSS
- **Project Portfolio**: Showcase of completed construction projects
- **Service Management**: Comprehensive service offerings and descriptions
- **Blog System**: Company news, updates, and industry insights
- **Career Portal**: Job listings and application management
- **Admin Dashboard**: Complete content management system
- **SEO Optimized**: Built-in SEO features and sitemaps
- **Mobile Responsive**: Optimized for all device sizes
- **Performance Optimized**: Fast loading with caching and optimization

## 🚀 Technology Stack

- **Backend**: Django 5.2.5 (Python)
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Database**: PostgreSQL (Production), SQLite (Development)
- **Media Storage**: ImageKit
- **Deployment**: Fly.io
- **Caching**: Redis/Database caching
- **Static Files**: WhiteNoise

## 📋 Prerequisites

- Python 3.11+
- Node.js 16+ (for Tailwind CSS)
- PostgreSQL (for production)
- Redis (optional, for caching)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ricas2410/skylinegh.git
   cd skylinegh
   ```

2. **Create virtual environment**
   ```bash
   python -m venv skyline_env
   source skyline_env/bin/activate  # On Windows: skyline_env\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Node.js dependencies**
   ```bash
   npm install
   ```

5. **Environment setup**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. **Database setup**
   ```bash
   python manage.py migrate
   python manage.py createcachetable
   python manage.py createsuperuser
   ```

7. **Build CSS**
   ```bash
   npm run build-css-prod
   ```

8. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

## 🏃‍♂️ Running the Application

### Development
```bash
# Terminal 1: Start Django development server
python manage.py runserver

# Terminal 2: Watch Tailwind CSS changes
npm run build-css
```

### Production
The application is configured for deployment on Fly.io with the included `Dockerfile` and `fly.toml`.

## 📁 Project Structure

```
skylinegh/
├── blog/                 # Blog application
├── careers/             # Career/Jobs application
├── core/                # Core application (main site)
├── dashboard/           # Admin dashboard
├── projects/            # Project portfolio
├── services/            # Services management
├── skylinegh/           # Main Django project
├── static/              # Static files (CSS, JS, images)
├── templates/           # HTML templates
├── media/               # User uploaded files
├── requirements.txt     # Python dependencies
├── package.json         # Node.js dependencies
├── tailwind.config.js   # Tailwind CSS configuration
├── Dockerfile          # Docker configuration
├── fly.toml            # Fly.io deployment config
└── entrypoint.sh       # Production startup script
```

## 🔧 Configuration

Key environment variables (see `.env.example`):

- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (False in production)
- `DATABASE_URL`: Database connection string
- `IMAGEKIT_*`: ImageKit configuration for media storage
- `EMAIL_*`: Email configuration
- `REDIS_URL`: Redis cache URL (optional)

## 🚀 Deployment

This project is configured for deployment on Fly.io:

1. Install Fly CLI
2. Login to Fly.io: `fly auth login`
3. Deploy: `fly deploy`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is proprietary software owned by Skyline Ghana Constructions.

## 📞 Contact

- **Website**: [skylinegh.com](https://skylinegh.com)
- **Email**: info@skylinegh.com
- **Phone**: +233-XX-XXX-XXXX
- **Address**: East Legon, Accra, Ghana

---

Built with ❤️ by Skyline Ghana Constructions
