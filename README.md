# Multi-Scanner API Gateway (with Kong & API Key Auth)

This project demonstrates a **config-driven, containerized API gateway** using [Kong](https://konghq.com/), providing easy routing to multiple scanner backends, secured with API key authentication. All configuration is done through version-controlled YAML files, supporting future expansion and CI/CD workflows.

---

## Features

- **API Gateway** powered by Kong (DB-less mode)
- **Declarative config** (`kong.yml`) for all routes, services, plugins, and consumers
- **Plug-and-play backend services** (add/remove scanners by editing config)
- **API Key authentication** (per-consumer)
- Simple, Docker Compose-based stack

---

## Folder Structure

multi-scanner/
├── docker-compose.yml
├── kong.yml
├── scanner1/
│ └── (Dockerfile + code)
├── scanner2/
│ └── (Dockerfile + code)
└── README.md


---

## Setup

### 1. Clone the repository & install [Docker](https://www.docker.com/products/docker-desktop)


git clone <your-repo-url>
cd multi-scanner

2. Project configuration (kong.yml)

Edit kong.yml to define routes, services, and consumers.

Example:

_format_version: "3.0"

services:
  - name: scanner1
    url: http://scanner1:5001
    routes:
      - name: scan1
        paths:
          - /scan1
        plugins:
          - name: key-auth
            config:
              key_names:
                - x-api-key

  - name: scanner2
    url: http://scanner2:5002
    routes:
      - name: scan2
        paths:
          - /scan2
        plugins:
          - name: key-auth
            config:
              key_names:
                - x-api-key

consumers:
  - username: myfriend
    keyauth_credentials:
      - key: secretkey1
  - username: you
    keyauth_credentials:
      - key: secretkey2

    Add/remove scanners: just add/remove service blocks.

    Add/remove users or keys: edit the consumers block.

3. Start all services

docker-compose up --build

    Kong listens on port 8000 (API gateway) and 8001 (admin API).

    Scanners run internally, not exposed outside the network.

Usage
API Gateway Endpoints

    POST or GET http://localhost:8000/scan1 (proxies to scanner1)

    POST or GET http://localhost:8000/scan2 (proxies to scanner2)

Authentication

All routes require an API key as an HTTP header:

    Header: x-api-key

    Value: any valid key defined in the consumers block of kong.yml

Example request:

curl -H "x-api-key: secretkey1" http://localhost:8000/scan1

If the key is missing or invalid, you will receive 401 Unauthorized.
Adding/Removing Scanners or Keys

    To add a new backend: Add a new service and route in kong.yml.

    To revoke/add a user: Edit or add to the consumers block.

    Apply changes: Restart Kong container:

    docker-compose restart kong

Customization

    Custom header for API key: Change key_names in the plugin config.

    Additional Kong plugins: Add to the plugins: section of any route/service in kong.yml (e.g., rate limiting, logging, etc.)

Future Directions

    Config-driven selection of which scanners are active (external config generator).

    Automated API key rotation/management.

    UI frontend integration (add a new service/route in kong.yml).

    CI/CD workflow for safe config changes.

Contributions

Feel free to fork, improve, or suggest changes via Pull Requests!
License
