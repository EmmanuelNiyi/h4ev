# eHealth4everyone Python Web Developer Assignment

## Table of Contents

* [Introduction](#introduction)
* [Architecture Overview](#architecture-overview)
* [Task 1: Onadata API Integration](#task-1-onadata-api-integration)
* [Task 2: Django REST API with Authentication & Logging](#task-2-django-rest-api-with-authentication--logging)
* [Getting Started](#getting-started)
* [License](#license)

---

## Introduction

This repository contains a Dockerized Django application that implements two main objectives:

1. **API Integration with Onadata**: Fetch and display form submissions from the Onadata API.
2. **Django REST API**: Provide secured endpoints with JWT authentication, request/response logging, and Redis caching with a cache-busting mechanism.

Both objectives are handled within a single Django project that contains two apps:

* **onadata**: Manages interactions with the Onadata API (Task 1).
* **accounts**: Manages user authentication/authorization, JWT, and helper endpoints (Task 2).

---

## Architecture Overview

```
+------------------+        +--------------------+        +-------------+
|    Docker Host   | <-->   |   Django Project   | <-->   |  Onadata    |
|  (Containers)    |        |                    |        |    API      |
|                  |        | +--------------+   |        +-------------+
|  +------------+  |        | | onadata app |    |        
|  |     web    |  |        | +--------------+   |        
|  +------------+  |        | +--------------+   |        
|  +------------+  |        | | accounts app|    |        
|  | redis cache|  |        | +--------------+   |        
|  +------------+  |        +--------------------+        
+------------------+                                     
```

Key components:

* **Django**
* **Redis** for response caching
* **JWT** authentication via `djangorestframework_simplejwt`
* **Requests** library for Onadata HTTP calls
* **File-based** JSON logging

---

## Task 1: Onadata API Integration

The **onadata** app provides two endpoints to interact with the Onadata API:

* **Get all forms for a user**
  `GET /api/onadata/user/<username>/forms/`
  Fetches all forms associated with the specified Onadata username.

* **Get submissions for a form**
  `GET /api/onadata/form/<form_id>/`
  Fetches all submissions for the given form ID.

Both endpoints use the `requests` library to perform external HTTP calls and return the raw JSON payload.

### Error Handling

* **Invalid `username` or `form_id`**: Returns `404 Not Found` with an error message.
* **Network issues/timeouts**: Returns `503 Service Unavailable` with retry instructions.

---

## Task 2: Django REST API with Authentication & Logging

The **accounts** app manages users and secures API endpoints via JWT tokens.

* **Endpoints**:

  * `POST /api/accounts/create/user/` — Create a new user
  * `GET /api/accounts/users/get/all/` — List all users (protected)
  * `POST /api/accounts/login/` — Obtain JWT tokens
  * `GET /api/accounts/user/<user_id>/` — Retrieve/update/delete a user (protected)

* **Logging**:

  * Logs request and response details (start/end times, duration, status, size)
  * Stored as JSON files in the `logs/` directory, one per user or endpoint.

* **Caching & Cache Busting**:

  * Redis caches Onadata responses using keys like `onadata_forms_<username>` and `onadata_submissions_<form_id>`.
  * A `cache_bust` URL parameter (e.g., timestamp or user role) forces cache refresh.

---

## Getting Started

### Clone & Run with Docker

```bash
# Clone the repository
git clone https://github.com/EmmanuelNiyi/h4ev.git
cd ehealth4everyone

# Build and start containers - migrations are applied automatically
docker-compose up --build -d
```

After containers are up:

* The web API will be available at `http://localhost:8006/`.
* Onadata endpoints: `/api/onadata/...`
* Accounts endpoints: `/api/accounts/...`

---

## License

This project is licensed under the MIT License. Please see [LICENSE](LICENSE) for details.
