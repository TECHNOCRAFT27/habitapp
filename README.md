# Flask Habit Tracker – Docker + Cloud Deployment

<img width="1920" height="1030" alt="Screenshot_20260312_212220" src="https://github.com/user-attachments/assets/24db7cd0-7083-438b-82f1-8abfe5ae56c1" />
this is painful
<img width="641" height="360" alt="image" src="https://github.com/user-attachments/assets/0b508f05-3602-4cb8-9029-3058c775ea95" />

## Project Overview

<img width="1885" height="510" alt="Screenshot_20260313_160715-1" src="https://github.com/user-attachments/assets/86f5bd61-0d56-42d9-a528-08273f7283ca" />
<img width="1885" height="510" alt="Screenshot_20260313_160715" src="https://github.com/user-attachments/assets/0b0dfd79-822c-4262-b968-71446e628a9f" />
<img width="1902" height="350" alt="Screenshot_20260313_160643-1" src="https://github.com/user-attachments/assets/d2d7501f-6e71-4b67-a751-6e4c8ec4e709" />
<img width="1902" height="350" alt="Screenshot_20260313_160643" src="https://github.com/user-attachments/assets/e42d9664-5f21-4ac6-8ec1-5bfc4829854a" />
<img width="1901" height="397" alt="Screenshot_20260313_160509-1" src="https://github.com/user-attachments/assets/055bf9e5-f958-4e88-bd8b-9d811469e2c3" />
<img width="1901" height="397" alt="Screenshot_20260313_160509" src="https://github.com/user-attachments/assets/73db5b12-4d68-4d48-81bf-51063d02031f" />


This project demonstrates how to build and deploy a simple **Flask web application** using **Docker containers** and host it on a cloud platform.

The goal of the project was to understand:

* Backend development using Flask
* Containerization using Docker
* Version control using GitHub
* Cloud deployment workflow
* Basic DevOps practices

The application was developed locally, containerized with Docker, pushed to GitHub, and then deployed to a cloud platform.
https://habit-tracker-v1vs.onrender.com/

---

# System Architecture



The application follows a container-based deployment architecture using Docker and cloud hosting.

```
                    ┌──────────────────────┐
                    │      User Browser    │
                    │  http://public-url  │
                    └──────────┬───────────┘
                               │ HTTP Request
                               ▼
                    ┌──────────────────────┐
                    │   Cloud Platform     │
                    │   (Render Service)   │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Docker Container   │
                    │  Flask Application   │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   PostgreSQL DB      │
                    │   habitdb database   │
                    └──────────────────────┘


──────────────── Development & Deployment Pipeline ────────────────

        Developer Laptop
                │
                ▼
        Write Flask Code
                │
                ▼
          Git Commit
                │
                ▼
        Push to GitHub Repository
                │
                ▼
        Docker Image Build
                │
                ▼
        Cloud Platform Pulls Repo
                │
                ▼
        Container Starts Automatically
                │
                ▼
        Application Available Online
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

This project started as a “simple Flask deployment”.

Then came Docker errors.
Then networking errors.
Then cloud deployment errors.
Then more Docker errors.

After many debugging sessions (and help from ChatGPT and Claude), the app is finally alive on the cloud.

If you find it useful, feel free to **use, modify, and improve it**. Welcome to the chaos of open source :)
