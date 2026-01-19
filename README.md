# Loan Origination System (Backend)

## Overview

This project implements a backend **Loan Origination System (LOS)** that
handles loan submissions, automated system-based processing, agent
reviews, and mocked notifications. The system is designed to safely
process multiple loan applications concurrently while maintaining clean
architecture and extensibility.

The implementation focuses on backend fundamentals such as API design,
concurrency handling, database modeling, and service separation.

---

## Features

- Submit loan applications via REST APIs
- Background multithreaded loan processing simulation
- Automated system approval / rejection logic
- Agent--Manager hierarchy for manual loan review
- Mocked notification service (SMS / push logs)
- Real-time loan status monitoring
- Top customers analytics
- Pagination support for loan queries
- PostgreSQL database integration
- Docker-based database setup

---

## Tech Stack

- **Backend Framework:** FastAPI
- **Language:** Python 3.11+
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy
- **Migrations:** Alembic
- **Async Server:** Uvicorn
- **Containerization:** Docker (for DB)
- **Testing:** Pytest

---
## Project Structure

```txt
loan-origination-system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   └── api/v1/
├── scripts/
│   └── seed_agents.py
├── tests/
├── postman/
│   └── LOS_API_Collection.json
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
└── README.md


## Setup & Run Instructions

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Git

---

### 1. Clone the Repository

```bash
git clone https://github.com/sahils281/loan-origination-system
cd loan-origination-system
```

---

### 2. Create & Activate Virtual Environment

**Windows (PowerShell):**

```powershell
python -m venv venv
.\venv\Scripts\Activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Environment Variables

Create `.env` from the example file:

```powershell
copy .env.example .env
```

---

### 5. Start PostgreSQL (Docker)

```bash
docker-compose up -d
```

---

### 6. Seed Initial Agents (One-time)

```bash
python -m scripts.seed_agents
```

---

### 7. Start the Backend Server

```bash
uvicorn app.main:app --reload
```

---

## Access the Application

- **API Base URL:** http://127.0.0.1:8000
- **Swagger Docs:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

---

## Key API Endpoints

- `POST /api/v1/loans`
- `GET /api/v1/loans/status-count`
- `GET /api/v1/loans?status=&page=&size=`
- `PUT /api/v1/agents/{agent_id}/loans/{loan_id}/decision`
- `GET /api/v1/customers/top`

---

## Design Highlights

- Thread-safe background loan processing
- Clean separation of concerns
- Idempotent database seeding
- Decoupled notification service
- Scalable and extensible structure

---

## Notes

- Notifications are mocked via logs
- Docker is used only for database setup

---

## Author

Sahil Saini
