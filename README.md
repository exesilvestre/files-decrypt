# Reverse Engineering File Container Extraction App

## Overview

This is a small application designed to extract and process files through reverse engineering of a container file that holds other files in a custom format.

The app consists of:

- **Backend:** built with **FastAPI**.
- **Frontend:** built with **React**.
- **Database:** MongoDB, used locally to store form files and their metadata.

---

## Technologies Used

-  FastAPI  for the backend API.
-  React for the frontend user interface.
-  MongoDB for storing files and metadata.
-  Docker and Docker Compose to simplify setup and deployment.

---

## Getting Started

The easiest and recommended way to run this app is with Docker Compose.

### Prerequisites

- Docker installed and running.  
- Docker Compose (usually included with Docker Desktop).

### How to Run

1. Clone the repository:

   ```bash
   git clone <your-repo-url>
   cd <repo-folder>
   ```
2. Copy the example environment file (optional, but recommended for local development):

   ```bash
   cp .env.example .env
   ```
3. Start the application using Docker Compose:
   ```bash
   docker-compose up
   ```

This command will build and run all necessary services including the backend, frontend, and MongoDB.

### Running Without Docker

If you prefer to run the backend and frontend separately (without Docker), keep in mind that:

- You need to have **MongoDB** running locally and accessible.
- Install all dependencies:
  - For the backend:
    ```bash
    pip install -r requirements.txt
    ```
  - For the frontend:
    ```bash
    npm install
    ```
    or
    ```bash
    yarn
    ```
- Set up your environment variables based on the `.env.example` file.
- Start each service manually.

Make sure the backend and frontend configurations point to the running MongoDB instance.