# Task Manager — DSCC Coursework 1

A Django task management web application containerised with Docker and deployed to a cloud server via an automated CI/CD pipeline.

**Live URL:** https://todo-app-16117.duckdns.org
**Docker Hub:** https://hub.docker.com/r/m1rjalolk24/taskmanager

---

## Features

- User registration and authentication
- Create, read, update, and delete tasks
- Assign categories and tags to tasks
- Responsive UI with custom CSS
- Django admin panel at `/admin`

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Django 5, Gunicorn |
| Database | PostgreSQL 16 |
| Reverse Proxy | Nginx |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| SSL | Let's Encrypt (Certbot) |
| Cloud | VPS (Ubuntu 24.04) |

---

## Project Structure

```
├── .github/workflows/deploy.yml   # CI/CD pipeline
├── taskmanager/
│   ├── Dockerfile                 # Multi-stage Alpine build
│   ├── docker-compose.yml         # 3-service stack
│   ├── nginx/nginx.conf           # Reverse proxy + SSL
│   ├── taskmanager/               # Django project settings
│   ├── tasks/                     # Tasks app
│   ├── accounts/                  # Auth app
│   ├── static/                    # CSS and assets
│   ├── templates/                 # HTML templates
│   └── requirements.txt
```

---

## Running Locally

**Prerequisites:** Docker and Docker Compose installed.

```bash
git clone https://github.com/m1rjalolk24/DSCC-CW1.git
cd DSCC-CW1/taskmanager
```

Create a `.env` file:
```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://taskuser:taskpass@db:5432/taskdb
POSTGRES_DB=taskdb
POSTGRES_USER=taskuser
POSTGRES_PASSWORD=taskpass
```

Start the app:
```bash
docker compose up -d
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

Open http://localhost in your browser.

---

## Docker

The image uses a **multi-stage build** to keep the final size under 200MB:

- **Stage 1 (builder):** Installs Python dependencies
- **Stage 2 (production):** Copies only the compiled packages and app code

The container runs as a **non-root user** (`appuser`) for security.

```bash
# Pull from Docker Hub
docker pull m1rjalolk24/taskmanager:latest
```

---

## CI/CD Pipeline

Every push to `main` triggers three automated jobs:

1. **Test** — runs flake8 linting and 15 pytest tests
2. **Build** — builds the Docker image and pushes to Docker Hub
3. **Deploy** — SSHs into the cloud server, pulls the new image, and restarts containers

### Required GitHub Secrets

| Secret | Description |
|---|---|
| `DOCKERHUB_USERNAME` | Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token |
| `SERVER_HOST` | Cloud server IP |
| `SERVER_USER` | SSH username |
| `SERVER_SSH_KEY` | Private SSH key |

---

## Running Tests

```bash
cd taskmanager
pip install -r requirements.txt
pytest tasks/tests.py -v
```

15 tests covering models, views, authentication, and CRUD operations.

---

## Deployment Architecture

```
Browser → Nginx (443 HTTPS) → Gunicorn (8000) → Django → PostgreSQL
                ↓
         Static files served directly by Nginx
```

- UFW firewall: only ports 22, 80, 443 open
- SSL certificates auto-renewed by Certbot
- Database persisted in a Docker named volume
