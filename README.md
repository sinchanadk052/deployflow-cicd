# 🐙 DeployFlow CI/CD

![CI/CD](https://img.shields.io/github/actions/workflow/status/sinchanadk052/deployflow-cicd/deploy.yml?label=CI%2FCD&logo=github-actions&style=flat-square)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.0-009688?style=flat-square&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Hub-2496ED?style=flat-square&logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=flat-square&logo=amazon-aws)

> A production-style **CI/CD pipeline** that automatically builds, containerizes, and deploys a **FastAPI** app to **AWS EC2** on every push to `main` — using **GitHub Actions** and **Docker Hub**.

---

## ✨ What It Does

- 🔍 **GitHub Profile Card App** — enter any GitHub username and get a beautiful profile card with stats and top repos, powered by the GitHub REST API
- ⚙️ **Fully automated pipeline** — push code → Docker image built & pushed → EC2 auto-updated, zero manual steps
- 🐳 **Dockerized** — runs identically in local dev and production
- ♻️ **Self-healing container** — restarts automatically on EC2 reboot (`--restart unless-stopped`)

---

## 🏗️ Pipeline Architecture

```
  Git Push (main)
       │
       ▼
 GitHub Actions
       │
       ├─▶ Checkout Code
       ├─▶ Setup Docker Buildx
       ├─▶ Login to Docker Hub
       ├─▶ Build & Push Image
       │       ├── deployflow:latest
       │       └── deployflow:<commit-sha>
       │
       └─▶ SSH into AWS EC2
               ├── Pull latest image
               ├── Stop old container
               ├── Run new container (:8000)
               └── Prune old images
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | FastAPI 0.115.0, Uvicorn |
| **Containerization** | Docker |
| **CI/CD** | GitHub Actions |
| **Registry** | Docker Hub |
| **Cloud** | AWS EC2 |
| **External API** | GitHub REST API v3 |
| **Language** | Python 3.11 |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Web UI — GitHub Profile Card |
| `GET` | `/api/profile/{username}` | Profile + top 5 repos as JSON |
| `GET` | `/health` | Health check |
| `GET` | `/api/info` | API metadata |
| `GET` | `/docs` | Swagger UI (auto-generated) |

---

## 📁 Project Structure

```
deployflow-cicd/
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline definition
├── main.py                  # FastAPI app + GitHub Profile Card UI
├── Dockerfile               # Container build instructions
├── requirements.txt         # Python dependencies
├── .dockerignore
└── .gitignore
```

---

## ⚙️ GitHub Secrets Required

**Settings → Secrets and variables → Actions → New repository secret**

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password or access token |
| `EC2_HOST` | Public IP of your AWS EC2 instance |
| `EC2_USER` | SSH username (`ubuntu` for Ubuntu AMI) |
| `EC2_SSH_KEY` | Full contents of your `.pem` private key |

---

## 🖥️ Run Locally

**Without Docker:**
```bash
git clone https://github.com/sinchanadk052/deployflow-cicd.git
cd deployflow-cicd
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**With Docker:**
```bash
docker build -t deployflow .
docker run -d -p 8000:8000 --name deployflow-app deployflow
```

App runs at → `http://localhost:8000`  
Swagger docs → `http://localhost:8000/docs`

---
## 🔮 Future Enhancements

- [ ] Add Slack/email notifications on deployment success or failure
- [ ] Multi-environment support (staging + production branches)
- [ ] Rollback mechanism on failed deployments
- [ ] Docker multi-stage builds to reduce image size
- [ ] Add unit and integration tests to the CI pipeline

--------

## 👩‍💻 Author

**Sinchana DK** — [@sinchanadk052](https://github.com/sinchanadk052)
