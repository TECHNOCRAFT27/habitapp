# Flask Habit Tracker – Docker + Cloud Deployment

## Project Overview

This project demonstrates how to build and deploy a simple **Flask web application** using **Docker containers** and host it on a cloud platform.

The goal of the project was to understand:

* Backend development using Flask
* Containerization using Docker
* Version control using GitHub
* Cloud deployment workflow
* Basic DevOps practices

The application was developed locally, containerized with Docker, pushed to GitHub, and then deployed to a cloud platform.

---

# System Architecture

```
Local Development
       │
       ▼
Git Push
       │
       ▼
GitHub Repository
       │
       ▼
Docker Image Build
       │
       ▼
Cloud Deployment
       │
       ▼
Public Web URL
```

---

# Tech Stack

| Component           | Technology              |
| ------------------- | ----------------------- |
| Backend Framework   | Flask                   |
| Containerization    | Docker                  |
| Version Control     | Git                     |
| Code Hosting        | GitHub                  |
| Cloud Deployment    | Render / Cloud platform |
| Database (optional) | PostgreSQL              |

---

# Project Structure

```
habit-tracker/
│
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

# Step 1 — Build the Flask Application

A simple Flask server was created.

Example structure:

```
app.py
```

The Flask application runs on port `5000`.

---

# Step 2 — Define Dependencies

Dependencies are stored in:

```
requirements.txt
```

Example:

```
flask
psycopg2-binary
```

This allows Docker to install required Python packages.

---

# Step 3 — Create Dockerfile

The Dockerfile defines how the container image is built.

Example workflow:

1. Use a Python base image
2. Copy application files
3. Install dependencies
4. Run Flask server

Dockerfile example:

```
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "app.py"]
```

---

# Step 4 — Build Docker Image

The image was built locally using:

```
docker build -t habit-tracker .
```

This creates a container image of the application.

---

# Step 5 — Run Container Locally

To verify the container works:

```
docker run -p 5000:5000 habit-tracker
```

Application becomes accessible at:

```
http://localhost:5000
```

---

# Step 6 — Push Code to GitHub

Project repository created on GitHub.

Commands used:

```
git init
git add .
git commit -m "initial commit"
git branch -M main
git remote add origin https://github.com/username/habit-tracker.git
git push -u origin main
```

Replace `username` with your GitHub username.

---

# Step 7 — Connect Repository to Cloud

The repository was connected to a cloud deployment platform.

Steps:

1. Login using GitHub account
2. Select repository
3. Choose Docker deployment
4. Configure service settings

Example configuration:

```
Service Name: habit-tracker-app
Environment: Docker
Region: Auto
```

---

# Environment Variables (Example)

Sensitive data must **never be stored in GitHub**.

Instead use environment variables.

Example:

```
DATABASE_URL=postgres://demo_user:demo_password@db:5432/habitdb
SECRET_KEY=dummy_secret_key
```

These are only **example values**.

Real credentials should be stored securely in the deployment platform.

---

# Example Dummy Database Credentials

```
DB_NAME=habitdb
DB_USER=demo_user
DB_PASSWORD=dummy_password
DB_HOST=database
DB_PORT=5432
```

These are **placeholders only**.

---

# Step 8 — Deployment

After deployment the cloud platform will:

1. Clone the repository
2. Build the Docker image
3. Start the container
4. Assign a public URL

Example public endpoint:

```
https://habit-tracker-app.example.com
```

---

# Security Notes

Important security practices used:

* No real credentials stored in repository
* Environment variables used for secrets
* Example passwords replaced with dummy values
* Sensitive configuration stored in cloud settings

---

# Learning Outcomes

This project helped understand:

* Flask backend development
* Docker container workflow
* Git version control
* Cloud deployment pipeline
* Basic DevOps concepts

---

# Future Improvements

Possible improvements:

* Add PostgreSQL database container
* Implement authentication system
* Add CI/CD pipeline
* Deploy using GitHub Actions
* Add monitoring and logging

---

# Author

technocraft27
Mechanical Engineering Student | Polymath Builder

Exploring backend development, cloud systems, and robotics-driven software systems.
