# LUMINA - Apartment Management System

**Automated management for short-term rental properties on Airbnb and Booking.com.**

Version 3.0.0 | Production Ready

---

## Table of Contents

- [Overview](#overview)
- [For Property Owners](#for-property-owners)
- [Technical Documentation](#technical-documentation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [License](#license)

---

## Overview

Lumina is a self-hosted system that synchronizes booking calendars from Airbnb and Booking.com, detects scheduling conflicts, generates property documents, sends automated email notifications, and provides a visual dashboard for monitoring occupancy and revenue.

The system is designed for individual property owners or small managers who need a centralized tool to handle multi-platform bookings without manual cross-referencing.

---

## For Property Owners

This section explains what Lumina does in practical terms, without technical jargon.

### What does Lumina do?

Lumina connects to your Airbnb and Booking.com calendars and keeps them synchronized. It alerts you when two guests are booked for the same dates, generates condominium authorization documents automatically, and sends check-in reminders to your guests by email.

### Main features

**Calendar synchronization** -- Lumina reads the booking calendars from Airbnb and Booking.com automatically. You do not need to check both platforms manually. All reservations appear in a single calendar view.

**Conflict detection** -- If a guest books on Airbnb for dates that overlap with a Booking.com reservation, the system flags this immediately and shows you exactly which dates overlap and how many nights are affected.

**Document generation** -- The system generates condominium authorization letters in DOCX format with the guest's name, dates, and property information already filled in. You can download and print them directly.

**Email notifications** -- Lumina sends booking confirmation emails and check-in reminders to guests automatically. It supports Gmail, Outlook, and Yahoo.

**Telegram notifications** -- Optionally, you can receive real-time alerts through a Telegram bot when new bookings arrive, conflicts are detected, or synchronization completes.

**Dashboard** -- A web interface shows your current occupancy rate, monthly revenue, upcoming check-ins, active conflicts, and recent activity. Statistics are available with charts covering occupancy, revenue, and platform distribution over time.

### How to use it daily

1. Open the web interface (http://localhost:5173 during setup, or your domain in production).
2. The dashboard shows your current status at a glance.
3. Click "Synchronize" on the Calendar page to pull the latest bookings.
4. Check the Conflicts page if any conflicts were detected.
5. Use the Documents page to generate authorization letters for upcoming guests.
6. Configure email and Telegram settings on the Settings page.

---

## Technical Documentation

### Architecture

Lumina uses a layered architecture with clear separation of concerns.

**Backend**: FastAPI (Python 3.11+) with SQLAlchemy ORM, Pydantic v2 validation, JWT authentication with token blacklist, bcrypt password hashing, and rate limiting via slowapi.

**Frontend**: React 18 with Vite build system. Uses state-based routing (switch/case in App.jsx) instead of React Router. CSS design system with custom properties and glassmorphism theme. Recharts for data visualization.

**Database**: SQLite for development, PostgreSQL recommended for production.

**Email**: Async IMAP/SMTP via aioimaplib and aiosmtplib with configurable providers (Gmail, Outlook, Yahoo, custom).

**Documents**: python-docx with Jinja2 templating for DOCX generation.

**Notifications**: Optional Telegram bot integration with python-telegram-bot.

### Security measures

- JWT authentication with token blacklist and automatic cleanup
- Account lockout after repeated failed login attempts
- Bcrypt password hashing with configurable rounds
- Rate limiting (global and per-endpoint)
- CSRF protection middleware
- Content Security Policy headers (strict for app, relaxed only for Swagger UI routes)
- HSTS, X-Frame-Options, X-Content-Type-Options headers
- Input validation and sanitization (XSS, path traversal, SSTI, header injection)
- IDOR protection on document endpoints
- Automatic log sanitization (tokens, passwords, and connection strings are redacted)
- SECRET_KEY validation (minimum 32 characters enforced in production)

### Key design decisions

**State-based routing**: The frontend uses a switch/case pattern in App.jsx controlled by Sidebar.jsx via a `currentPage` state variable. This was chosen over React Router to keep the bundle small and avoid unnecessary complexity for a single-page management tool.

**PropertyContext**: All pages that need a property_id access it via React Context (`usePropertyId` hook) rather than hardcoding values. This prepares the system for future multi-property support.

**ErrorBoundary**: A React class-based error boundary wraps each page with `key={currentPage}` for automatic reset on navigation.

**Centralized formatters**: Date, currency, and time formatting functions are consolidated in `frontend/src/utils/formatters.js` to eliminate duplication across pages.

**NotificationService consolidation**: A single NotificationService class accepts an optional database session, providing auto-persistence when available while remaining usable without a database connection for logging-only scenarios.

**Concurrent email sending**: Bulk email operations use `asyncio.gather` with a semaphore (max 5 concurrent connections) to avoid SMTP connection exhaustion.

**Log sanitization**: All log output passes through a sanitization layer that redacts tokens, passwords, Bearer headers, and connection strings before writing to any sink.

---

## Quick Start

### Prerequisites

- Python 3.11 or later
- Node.js 18 or later (for the frontend)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/Sitr3n01/AP_Controller.git
cd AP_Controller

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your settings (see Configuration section below)

# Initialize the database
python -c "from app.database.session import create_all_tables; create_all_tables()"

# Create the default admin user
python scripts/create_default_admin.py

# Start the backend server
uvicorn app.main:app --reload
```

The API will be available at http://localhost:8000. Interactive API docs at http://localhost:8000/docs.

```bash
# In a separate terminal, start the frontend
cd frontend
npm install
npm run dev
```

The web interface will be available at http://localhost:5173.

**Default credentials**: admin / Admin123!

Change the default password immediately after first login.

---

## Configuration

All configuration is done through the `.env` file. Copy `.env.example` and adjust the values.

### Required settings

| Variable | Description |
|---|---|
| `SECRET_KEY` | JWT signing key. Minimum 32 characters. Generate with: `python -c "import secrets; print(secrets.token_urlsafe(32))"` |
| `DATABASE_URL` | Database connection string. Default: `sqlite:///./data/lumina.db` |
| `APP_ENV` | Environment: `development`, `staging`, or `production` |

### Calendar integration

| Variable | Description |
|---|---|
| `AIRBNB_ICAL_URL` | iCal feed URL from your Airbnb listing |
| `BOOKING_ICAL_URL` | iCal feed URL from your Booking.com property |
| `CALENDAR_SYNC_INTERVAL_MINUTES` | Auto-sync interval in minutes. Default: 30 |

### Email (optional)

| Variable | Description |
|---|---|
| `EMAIL_PROVIDER` | `gmail`, `outlook`, `yahoo`, or `custom` |
| `EMAIL_FROM` | Sender email address |
| `EMAIL_PASSWORD` | Email password or app-specific password |

For Gmail, use an App Password (not your regular password). Generate one at https://myaccount.google.com/apppasswords.

### Telegram (optional)

| Variable | Description |
|---|---|
| `TELEGRAM_BOT_TOKEN` | Token from @BotFather |
| `TELEGRAM_ADMIN_USER_IDS` | Comma-separated Telegram user IDs |

### Property information

| Variable | Description |
|---|---|
| `PROPERTY_NAME` | Name of your property |
| `PROPERTY_ADDRESS` | Full address |
| `OWNER_NAME` | Property owner name |
| `OWNER_EMAIL` | Owner email for reports |
| `CONDO_NAME` | Condominium name (used in document generation) |

---

## Deployment

### Docker (recommended)

```bash
cp .env.example .env.production
# Edit .env.production with production values

docker compose up -d
docker compose logs -f
```

### VPS with Systemd

Detailed deployment guides are available in the `docs/deployment/` directory:

- `DEPLOYMENT_VPS.md` -- Full VPS deployment with Nginx and Let's Encrypt
- `DOCKER_DEPLOYMENT.md` -- Docker-based deployment guide

### Pre-deployment checklist

1. Set `APP_ENV=production` in your .env file.
2. Generate a strong SECRET_KEY (minimum 32 characters).
3. Set `ALLOWED_HOSTS` to your domain.
4. Change the default admin password.
5. Configure SSL/TLS (Let's Encrypt recommended).
6. Review rate limiting settings for your expected traffic.

---

## Project Structure

```
AP_Controller/
|
|-- app/                          # Backend application
|   |-- api/v1/                   # Auth and health endpoints
|   |-- core/                     # Calendar sync, conflict detection, security
|   |-- database/                 # SQLAlchemy connection and sessions
|   |-- middleware/                # Auth, CSRF, security headers
|   |-- models/                   # ORM models (User, Booking, Property, etc.)
|   |-- routers/                  # API route handlers
|   |   |-- bookings.py           # Booking CRUD
|   |   |-- calendar.py           # Calendar sync and events
|   |   |-- conflicts.py          # Conflict detection and resolution
|   |   |-- documents.py          # Document generation and download
|   |   |-- emails.py             # Email send/fetch (IMAP/SMTP)
|   |   |-- notifications.py      # In-app notification system
|   |   |-- settings.py           # Application settings
|   |   |-- statistics.py         # Occupancy, revenue, reports
|   |   +-- sync_actions.py       # Platform sync actions
|   |-- schemas/                  # Pydantic request/response models
|   |-- services/                 # Business logic layer
|   |-- telegram/                 # Telegram bot integration
|   +-- utils/                    # Logger (with sanitization), validators
|
|-- frontend/                     # React 18 + Vite frontend
|   +-- src/
|       |-- components/           # Sidebar, Calendar, ErrorBoundary, EventModal
|       |-- contexts/             # PropertyContext (property_id management)
|       |-- pages/                # Dashboard, Calendar, Conflicts, Statistics,
|       |                         # Documents, Emails, Notifications, Settings
|       |-- services/             # API client (axios)
|       |-- styles/               # Global CSS design system
|       +-- utils/                # Shared formatters (date, currency, time)
|
|-- docs/                         # Documentation
|   |-- architecture/             # API reference, system architecture, Telegram
|   |-- deployment/               # VPS and Docker deployment guides
|   +-- guides/                   # Daily usage guide
|
|-- scripts/                      # Utility scripts (DB init, admin creation)
|-- deployment/                   # Docker and Nginx configurations
|-- templates/                    # DOCX document templates
+-- data/                         # Runtime data (DB, logs, generated docs)
```

---

## API Reference

The API is organized under the following route prefixes:

| Prefix | Module | Description |
|---|---|---|
| `/api/bookings` | bookings.py | Booking CRUD and upcoming bookings |
| `/api/calendar` | calendar.py | Calendar events and synchronization |
| `/api/conflicts` | conflicts.py | Conflict detection, summary, resolution |
| `/api/statistics` | statistics.py | Occupancy, revenue, platform stats, monthly reports |
| `/api/sync-actions` | sync_actions.py | Sync action management |
| `/api/v1/documents` | documents.py | Document generation, listing, download |
| `/api/v1/emails` | emails.py | Email send, fetch, templates, bulk reminders |
| `/api/v1/settings` | settings.py | Application settings (get/update) |
| `/api/v1/notifications` | notifications.py | Notification list, summary, mark as read |
| `/api/v1/auth` | auth.py | Login, register, logout, token refresh |
| `/api/health` | health.py | Health check and system metrics |

All endpoints require JWT authentication except `/api/v1/auth/login`, `/api/health`, and the documentation routes (`/docs`, `/redoc`).

Full interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

---

## License

MIT License. See LICENSE file for details.
