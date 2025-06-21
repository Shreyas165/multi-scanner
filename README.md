
# NOTE- PROJECT STILL CONTANS SOME ERRORS THAT NEED TO BE FIXED AND CREATE A NEW BRANCH WHEN WORKING ON NEW FEATURES 
# Multi-Scanner Application with API Gateway







This project is a microservice-based application designed to demonstrate a modern, distributed scanning architecture. A central `master` service orchestrates tasks, which are processed by multiple `scanner` services. All results are stored in a PostgreSQL database.

This version has been enhanced with a **Kong API Gateway**, which acts as a secure and managed entry point for all incoming API traffic.

## Architecture

The application consists of five main components that work together. The API Gateway serves as the single entry point, securing and routing traffic to the backend services.


Client Request --> Kong API Gateway (Port 8000)
|
+--> (Routes /scan requests)
|
Master Service
/
/
Scanner 1 Service Scanner 2 Service
\ /
\ /
PostgreSQL Database



### Core Components

*   **Kong API Gateway**: The new front door for our application. It is responsible for:
    *   Receiving all incoming client requests.
    *   Routing requests to the appropriate backend service.
    *   Providing a centralized place to enforce security (like authentication) and traffic control (like rate-limiting).
*   **Master Service**: A Flask application that receives tasks from the gateway, delegates them to both scanner services, and records their responses in the database.
*   **Scanner Services (scanner1 & scanner2)**: Two independent Flask applications that perform the "scanning." They receive data from the master, process it, and return a result.
*   **Database**: A PostgreSQL database used to persist the scan results from all scanner services.

## Getting Started (Local Development)

This project is configured to run locally using Docker and Docker Compose.

### Prerequisites

*   [Docker](https://docs.docker.com/get-docker/)
*   [Docker Compose](https://docs.docker.com/compose/install/) (usually included with Docker Desktop)
*   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Running the Application

1.  **Clone the repository:**
    ```sh
    git clone <repository-url>
    cd <repository-name>
    ```

2.  **Build and run all services:**
    This command will build the images for all services (including the gateway) and start them in the background.
    ```sh
    docker-compose up --build -d
    ```

3.  **Check that all containers are running:**
    ```sh
    docker-compose ps
    ```
    You should see `kong-gateway`, `master`, `scanner1`, `scanner2`, and `db` services in the `Up` state.

### Testing the Application

Once all services are running, you can send a `POST` request to the API Gateway's `/scan` endpoint. Note that you are now targeting **port 8000**, which is managed by Kong.

```sh
curl -i -X POST http://localhost:8000/scan \
     -H "Content-Type: application/json" \
     -d '{"url": "example.com"}'

ou should receive a HTTP/1.1 200 OK response containing the results from both scanners.
Stopping the Services
To stop all running containers, run:
docker-compose down
API Usage
POST /scan
Initiates a scan by sending data to the system.
URL: http://localhost:8000/scan
Method: POST
Headers:
Content-Type: application/json
Request Body: A JSON object representing the data to be scanned.
Generated json
{
  "url": "some-url-to-scan.com",
  "some_other_data": "value"
}
Use code with caution.
Json
Success Response: A JSON object containing the individual responses from each scanner.
Generated json
{
  "scanner1": {
    "result": "Processed: {'url': 'example.com'}",
    "scanner": "1",
    "status": "success"
  },
  "scanner2": {
    "result": "Processed: {'url': 'example.com'}",
    "scanner": "2",
    "status": "success"
  },
  "status": "success"
}
Use code with caution.
Json
Configuration
docker-compose.yml: Defines all the services, networks, and volumes for the local development environment.
kong/kong.yml: The declarative configuration file for the Kong API Gateway. This file defines the backend services and the routes that map to them.
Kubernetes Deployment (Work in Progress)
The original Kubernetes manifests in the /k8s directory are now outdated. The next phase of this project will involve updating these manifests to deploy the new API Gateway architecture to a Kubernetes cluster. This will include creating new deployment and service files for Kong and updating the master service to use the correct environment variables.
