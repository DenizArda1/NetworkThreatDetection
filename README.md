# 🛡️ Network Threat Detection: MLOps Project

An end-to-end Machine Learning system designed to detect network security threats (e.g., Phishing) using a robust MLOps pipeline. This project exposes a **FastAPI** web interface for real-time predictions and asynchronous model training, containerized with **Docker**, and managed via **Celery** and **Redis**.

## 🚀 Key Features

* **End-to-End ML Pipeline:** Modular components for Data Ingestion, Validation, Transformation, and Model Training.
* **Real-time Prediction API:** Fast and efficient inference using **FastAPI**.
* **Asynchronous Training:** Heavy model training tasks are offloaded to background workers using **Celery** and **Redis**.
* **Experiment Tracking:** Integration with **MLflow** and **DagsHub** to track model metrics and parameters.
* **Data Validation:** Drift detection and schema validation using **Scipy** and custom logic.
* **Containerization:** Fully Dockerized application for consistent deployment.
* **Database Integration:** **MongoDB** for data storage and retrieval.

---

## 🛠️ Tech Stack

This project utilizes a modern stack of technologies for Data Science and Backend Development:

### **Programming & Frameworks**
* **[Python 3.11](https://www.python.org/):** The core programming language.
* **[FastAPI](https://fastapi.tiangolo.com/):** High-performance web framework for building APIs.
* **[Uvicorn](https://www.uvicorn.org/):** ASGI web server implementation.
* **[Jinja2](https://jinja.palletsprojects.com/):** Templating engine for serving HTML frontend.

### **Machine Learning & Data Processing**
* **[Scikit-Learn](https://scikit-learn.org/):** Main library for machine learning algorithms.
* **[Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/):** Data manipulation and numerical analysis.
* **[Dill](https://pypi.org/project/dill/):** Advanced serialization for saving model objects.
* **[Scipy](https://scipy.org/):** Used for scientific computing and statistical checks (e.g., drift reports).

### **MLOps & Experiment Tracking**
* **[MLflow](https://mlflow.org/):** For managing the ML lifecycle (experiment tracking, model registry).
* **[DagsHub](https://dagshub.com/):** Remote storage and collaboration for MLflow.

### **Infrastructure & DevOps**
* **[Docker](https://www.docker.com/):** Containerization of the application.
* **[Docker Compose](https://docs.docker.com/compose/):** Multi-container orchestration.
* **[Celery](https://docs.celeryq.dev/):** Distributed task queue for handling background training jobs.
* **[Redis](https://redis.io/):** Message broker used by Celery.
* **[GitHub Actions](https://github.com/features/actions):** CI/CD pipeline for code quality and build checks.

### **Database & Utilities**
* **[MongoDB](https://www.mongodb.com/):** NoSQL database for storing training data.
* **[PyMongo](https://pymongo.readthedocs.io/):** MongoDB driver for Python.
* **[Certifi](https://pypi.org/project/certifi/):** Validating SSL certificates for secure DB connections.
* **[Python-Dotenv](https://pypi.org/project/python-dotenv/):** Loading environment variables.

---

## 📂 Project Structure

```text
NetworkSecurity/
├── .github/workflows/   # CI/CD Pipelines
├── data_schema/         # Schema validation files (schema.yaml)
├── final_model/         # Serialized models (model.pkl, preprocessor.pkl)
├── src/
│   ├── components/      # ML Pipeline Modules (Ingestion, Validation, etc.)
│   ├── pipeline/        # Training and Prediction Pipelines
│   ├── utils/           # Helper functions and metrics
│   ├── entity/          # Config and Artifact definitions
│   ├── constants/       # Constant variables
│   ├── logging/         # Custom Logger
│   └── exception/       # Custom Exception Handling
├── templates/           # HTML templates for the UI
├── app.py               # Main FastAPI application entry point
├── Dockerfile           # Docker image configuration
├── docker-compose.yml   # Services configuration (Web, Worker, Redis)
├── requirements.txt     # Python dependencies
└── setup.py             # Package installation script
```

# ⚙️ Installation & Setup Guide

This guide provides step-by-step instructions to set up the **Network Security Prediction** system locally or using Docker.

## ✅ Prerequisites

Ensure you have the following installed on your system:
* **[Docker Desktop](https://www.docker.com/products/docker-desktop/)** (for containerized setup)
* **[Python 3.11+](https://www.python.org/downloads/)** (for local setup)
* **[Git](https://git-scm.com/)**
* **MongoDB Atlas Account** (or a local MongoDB instance)

---

## 1️⃣ Clone the Repository

First, clone the project repository to your local machine:

```bash
git clone https://github.com/DenizArda1/NetworkThreatDetection.git
cd NetworkThreatDetection
```

## 2️⃣ Environment Configuration

Regardless of the installation method (Docker or Local), you must configure your environment variables.

1. Create a .env file in the root directory:
```bash
touch .env  # Linux/Mac
# or manually create .env in Windows
```

2. Add the following credentials to the .env file. You will need a MongoDB connection string.
```bash
# .env
MONGO_DB_URL="mongodb+srv://<username>:<password>@<cluster-url>/?appName=Cluster0"

# Optional: If you use MLflow/DagsHub, add credentials here (if applicable)
# MLFLOW_TRACKING_URI=...
# MLFLOW_TRACKING_USERNAME=...
# MLFLOW_TRACKING_PASSWORD=...
```
Note: The application uses python-dotenv to load these variables automatically.

## 3️⃣ Method A: Docker Installation (Recommended)

This is the easiest way to run the application as it orchestrates the API, Celery Worker 
and Redis automatically.

Build and Run
Run the following command in the project root (where docker-compose.yml is located):
```bash
docker-compose up --build
```
What happens?
* API Service: Starts on port 8000.

* Redis: Starts a Redis instance for message brokering.

* Worker: Starts a Celery worker to handle background training tasks.

Once the logs show the services are healthy, you can access the application.

* Frontend UI: http://localhost:8000

* API Docs (Swagger): http://localhost:8000/docs

## 4️⃣ Method B: Local Installation (Manual)

If you prefer to run the services manually without Docker, follow these steps.

Step 1: Create Virtual Environment
It is recommended to use a virtual environment to manage dependencies.

```bash
# Create environment
python -m venv venv

# Activate environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

Step 2: Install Dependencies
Install the required Python packages from requirements.txt:
```bash
pip install -r requirements.txt
```

Step 3: Run Redis
The asynchronous training pipeline requires Redis.

* Option A: Install Redis locally on your machine.

* Option B: Run a lightweight Redis container:
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

Step 4: Run the Application
You need to run the API and the Celery worker in separate terminal windows.

Terminal 1: Start FastAPI Server
```bash
python app.py
# OR using uvicorn directly
python -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Terminal 2: Start Celery Worker Make sure your virtual environment is activated here as well.
```bash
celery -A src.utils.main_utils.app_utils.celery_app worker --loglevel=info
```

## 🖥️ Usage Guide

1. Web Interface
Navigate to http://localhost:8000. 
  * Predict: Upload a CSV file (e.g., test.csv) containing network data. The system will display the prediction results in a table.

2. Trigger Model Training to retrain the model with new data fetched from MongoDB:

  * Endpoint: GET /train

  * Response: Returns a task_id.

  * The training runs in the background using Celery. You can check the logs of the "worker" container/terminal to see progress.

3. Check Task Status
  * Endpoint: GET /task/{task_id}

  * Use the task_id received from the /train endpoint to check if training is PENDING, STARTED, or SUCCESS.

## 🧪 Running Tests (Optional)

To verify the MongoDB connection or other components:
```bash
python test_mongodb.py
```