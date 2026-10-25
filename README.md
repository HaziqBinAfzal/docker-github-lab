# Docker & GitHub Lab

A small Flask application for learning container builds, port mapping, health checks and GitHub Actions. This repository began as a README-only scaffold; the first runnable exercise is now included.

[![Docker lab CI](https://github.com/HaziqBinAfzal/docker-github-lab/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/HaziqBinAfzal/docker-github-lab/actions/workflows/ci.yml)

## What the app does

| Route | Expected response |
| --- | --- |
| `GET /` | `{"message":"Hello from Docker & GitHub Lab!","service":"docker-github-lab"}` |
| `GET /health` | `{"status":"ok"}` with HTTP 200 |

There is no login, database, external API or persistent application data.

## Run with Docker Compose

Install Git and Docker Desktop with Compose v2. Start Docker Desktop before continuing. Use Linux containers on Windows.

```bash
git clone https://github.com/HaziqBinAfzal/docker-github-lab.git
cd docker-github-lab
docker compose config --quiet
docker compose up --build --wait --wait-timeout 120
docker compose ps
```

Open **http://localhost:8080/** and **http://localhost:8080/health**. Compose should report the web service as healthy. The application listens on port 8000 inside the container; Compose publishes it only on the host's loopback interface at port 8080.

If you already have a clone, update it with `git pull --ff-only` from a clean working tree instead of cloning again.

### If port 8080 is in use

PowerShell:

```powershell
$env:LAB_PORT = "8088"
docker compose up --build --wait --wait-timeout 120
```

Bash:

```bash
LAB_PORT=8088 docker compose up --build --wait --wait-timeout 120
```

Then open **http://localhost:8088/**. The container still uses port 8000.

### Logs and cleanup

```bash
docker compose logs --tail=50 web
docker compose down --remove-orphans
```

`down` removes this lab's containers and network. The built image remains cached. Run these commands from the repository folder so Compose can find `compose.yaml`.

## Build an image directly

```bash
docker build -t docker-github-lab:local .
docker run --rm --name docker-github-lab -p 127.0.0.1:8080:8000 docker-github-lab:local
```

Stop that foreground container with Ctrl+C. Do not run it and the Compose service on the same host port simultaneously.

## Python checks without Docker

Python 3.12 is the version used by the image and CI. Create an environment:

```bash
python -m venv .venv
```

Activate with `.venv\Scripts\Activate.ps1` in PowerShell, or `source .venv/bin/activate` in Bash on Linux/WSL. If activation is unavailable, call the environment's Python executable directly.

```bash
python -m pip install -r requirements.txt
python -m unittest -v test_app
python -m flask --app app run --host 127.0.0.1 --port 8080
```

In a second terminal, run `python smoke_test.py` with the same environment. It checks the JSON responses from both live routes. For a different port, use `python smoke_test.py http://127.0.0.1:8088`.

Flask's development server is for this local exercise. The Docker image uses Gunicorn; Gunicorn runs in Linux containers and is not required to run natively on Windows.

## How the container works

- Python 3.12 slim base image; Flask and Gunicorn versions are pinned in `requirements.txt`.
- Application process runs as UID 10001 rather than root.
- Image health check requests `/health` and verifies the response.
- Compose uses a read-only root filesystem, writable temporary storage, dropped capabilities and no-new-privileges.
- `.dockerignore` includes only the application and requirements in the build context.

This is a local learning service. Authentication, TLS, production deployment and image signing are outside this exercise. Base image tags and transitive dependencies can change; this is not a fully locked build.

## GitHub Actions

[View Docker lab CI](https://github.com/HaziqBinAfzal/docker-github-lab/actions)

The workflow in `.github/workflows/ci.yml` runs on pushes to `main`, pull requests and manual dispatch. It checks the Python HTTP contract, validates Compose, builds the image, waits for container health, checks both live endpoints, verifies UID 10001, prints logs and cleans up. It does not publish an image or deploy the app.

**Validation:** four Python tests and both live Gunicorn endpoint checks passed in the authoring environment on 25 October 2026. The [first GitHub Actions run](https://github.com/HaziqBinAfzal/docker-github-lab/actions/runs/40185806722) also passed the image build, Compose health check, live HTTP checks and UID 10001 check. This verifies the synthetic lab on a hosted Linux runner, not on every learner's computer.

## Practice the Git workflow

Create a branch, make one focused change, inspect `git diff`, run the checks and open a pull request explaining the behavior and validation. This is the next exercise; no PR is claimed as completed by these instructions. [Git Practice](https://github.com/HaziqBinAfzal/git-practice) has a separate text-file walkthrough.

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Two read-only HTTP routes |
| `Dockerfile` | Image, non-root runtime and health check |
| `compose.yaml` | Local port mapping and runtime restrictions |
| `test_app.py` | HTTP contract and rejection tests |
| `smoke_test.py` | Real-server endpoint checks |
| `.github/workflows/ci.yml` | Build and container verification |

## Explore related work

[Haziq Afzal](https://github.com/HaziqBinAfzal) · [LinuxOps Enterprise Lab](https://github.com/HaziqBinAfzal/linuxops-enterprise-lab) · [AquaVigil](https://github.com/HaziqBinAfzal/AquaVigil)
