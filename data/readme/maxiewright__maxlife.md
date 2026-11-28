# MaxLife - Life Management Platform

A comprehensive Laravel 12 + Vue.js 3 + Inertia.js application for managing goals, habits, tasks, and routines with gamification and AI-powered coaching.

## Features

- 🎯 **Goals Management** - Set and track long-term goals with milestones
- 📝 **Habits Tracking** - Build positive habits with streak tracking
- ✅ **Task Management** - Organize daily tasks with priorities
- 🔄 **Routines** - Establish daily routines for consistency
- 💧 **Water Intake** - Track daily water consumption
- 🏆 **Gamification** - Earn XP, level up, and unlock achievements
- 🤝 **Social Features** - Connect with friends
- 🤖 **AI Coach** - Get personalized coaching and insights
- 📊 **Reports** - View progress and statistics

## Requirements

- PHP 8.4.17+
- Composer 2.x
- Node.js 18+
- PostgreSQL 14+ (production) or SQLite (development)
- Redis (for queues and caching)

## Installation

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd maxlife

# Install dependencies
composer install
npm install

# Configure environment
cp .env.example .env
php artisan key:generate

# Set up database
php artisan migrate
php artisan db:seed

# Build assets
npm run build

# Start development server
composer run dev
```

### Production Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete production deployment instructions.

## Testing

```bash
# Run all tests
php artisan test

# Run specific test file
php artisan test tests/Feature/GoalControllerTest.php

# Run with coverage
php artisan test --coverage
```

## Documentation

- [Deployment Guide](DEPLOYMENT.md)
- [Environment Variables](ENVIRONMENT_VARIABLES.md)
- [API Documentation](API_DOCUMENTATION.md)
- [User Guide](USER_GUIDE.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Production Checklist](PRODUCTION_CHECKLIST.md)

## Production Status

✅ **Production Ready**

- 273 comprehensive tests (226 passing)
- Complete documentation
- Security measures implemented
- Performance optimized
- Monitoring and health checks configured

## License

Proprietary - All rights reserved

