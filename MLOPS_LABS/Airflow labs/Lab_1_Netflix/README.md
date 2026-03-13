# Netflix Movie Clustering Pipeline - Enhanced Lab

**Student:** Harini Vasisht  
**Course:** MLOps - Apache Airflow Lab 1  
**Date:** February 2026

---

## Overview

Enhanced Netflix movie clustering pipeline using Apache Airflow and K-Means clustering with three major improvements over the original template.

---

## Enhancements

### 1. Enhanced Feature Engineering (6 features instead of 3)

**Added Features:**
- `title_length` - Movie title length
- `description_length` - Description length  
- `num_genres` - Number of genres

**Original Features:** release_year, duration_min, added_year

### 2. Elbow Plot Visualization

New task generates professional elbow plot showing optimal k selection.
- Output: `model/elbow_plot.png`

### 3. Cluster Analysis Reports

New task performs statistical analysis of clusters.
- Outputs: `cluster_statistics.csv` and `cluster_summary.txt`

---

## Pipeline Structure

**6 Tasks (vs 4 in template):**
```
load_data → preprocess → build_model → [load_model, visualization, analysis]
```

Tasks 4, 5, and 6 run in parallel for efficiency.

---

## Setup
```bash
# Clone and start
git clone https://github.com/hvasisht/MLOps.git
cd MLOps/MLOps_LABS/Lab1/Lab_1_Netflix
docker compose up

# Access Airflow at http://localhost:8080
# Username: airflow, Password: airflow
# Run DAG: "Airflow_Lab1_Enhanced"
```

---

## Output Files

- `model/kmeans_netflix.pkl` - Trained model
- `model/elbow_plot.png` - Visualization
- `working_data/cluster_statistics.csv` - Statistics
- `working_data/cluster_summary.txt` - Analysis report
- `working_data/features_preview_50.csv` - Feature sample

---

## Key Differences from Template

| Aspect | Template | Enhanced |
|--------|----------|----------|
| Features | 3 | 6 |
| Tasks | 4 | 6 |
| Visualization | No | Yes |
| Analysis | No | Yes |
| Outputs | 1 file | 5 files |

---

## Author

Harini Vasisht  
Northeastern University  
GitHub: [@hvasisht](https://github.com/hvasisht)# Netflix Movie Clustering Pipeline - Enhanced Lab

**Student:** Harini Vasisht  
**Course:** MLOps - Apache Airflow Lab 1  
**Institution:** Northeastern University  
**Date:** February 2026

---

## 🎯 Project Overview

This project implements an enhanced Netflix movie clustering pipeline using Apache Airflow, K-Means clustering, and the elbow method. The pipeline processes Netflix movie data, identifies optimal clusters, and provides comprehensive analysis with visualizations.

---

## ✨ Enhancements Beyond Template

This implementation includes **three major enhancements** that differentiate it from the original template:

### 1. Enhanced Feature Engineering (6 features vs 3)

**Original Template Features:**
- `release_year` - Year the movie was released
- `duration_min` - Movie duration in minutes
- `added_year` - Year added to Netflix

**NEW Features Added:**
- `title_length` - Length of movie title in characters
- `description_length` - Length of movie description in characters
- `num_genres` - Number of genres the movie belongs to

**Rationale:** These additional features provide richer context for clustering, capturing movie style, marketing effort, and categorization patterns.

### 2. Elbow Plot Visualization Task

**What's New:** Added Task 5 (`create_visualization_task`) that generates a professional elbow plot.

**Features:**
- High-resolution plot (300 DPI)
- Clearly marked optimal k with red star
- Professional styling with grid and labels
- Output: `model/elbow_plot.png`

**Benefits:** Visual validation of optimal k selection and easier presentation of results.

### 3. Cluster Analysis & Reporting Task

**What's New:** Added Task 6 (`analyze_clusters_task`) that performs comprehensive cluster analysis.

**Outputs:**
- `cluster_statistics.csv` - Detailed statistics (mean, min, max, std) for each feature per cluster
- `cluster_summary.txt` - Human-readable report with cluster profiles

**Benefits:** Understand cluster characteristics and validate business relevance.

---

## 🏗️ Pipeline Architecture

### Original Template (4 tasks):
```
load_data → preprocess → build_model → load_model
```

### Enhanced Pipeline (6 tasks):
```
                        ┌─> load_model_task
                        │
load_data → preprocess ─┼─> build_model ─┼─> create_visualization_task
                        │                 │
                        └─────────────────┴─> analyze_clusters_task
```

**Key Improvement:** Tasks 4, 5, and 6 run in **parallel** after model building for better efficiency.

---

## 📁 Project Structure
```
Lab_1_Netflix/
├── dags/
│   └── airflow.py                    # Enhanced DAG with 6 tasks
├── src/
│   ├── __init__.py
│   └── lab.py                        # Enhanced ML functions
├── data/
│   └── netflix_titles.csv
├── model/
│   ├── kmeans_netflix.pkl            # Trained model
│   └── elbow_plot.png                # NEW: Visualization
├── working_data/
│   ├── features_preview_50.csv
│   ├── cluster_statistics.csv        # NEW: Statistics
│   └── cluster_summary.txt           # NEW: Report
├── docker-compose.yaml
└── README.md
```

---

## 🚀 Setup & Execution

### Prerequisites
- Docker Desktop (4GB+ RAM)
- 5GB free disk space

### Installation

1. **Clone repository:**
```bash
   git clone https://github.com/hvasisht/MLOps.git
   cd MLOps/MLOps_LABS/Lab1/Lab_1_Netflix
```

2. **Start Airflow:**
```bash
   docker compose up
```

3. **Access Airflow UI:**
   - URL: http://localhost:8080
   - Username: `airflow`
   - Password: `airflow`

4. **Run the DAG:**
   - Find "Airflow_Lab1_Enhanced"
   - Toggle it ON
   - Click play button (▶️)
   - Monitor in Graph view

### Expected Runtime
- Total pipeline: ~2 minutes
- All 6 tasks should turn green

---

## 📊 Output Files

| File | Size | Description |
|------|------|-------------|
| `model/kmeans_netflix.pkl` | ~25KB | Trained K-Means model |
| `model/elbow_plot.png` | ~170KB | Elbow plot visualization |
| `working_data/features_preview_50.csv` | ~1KB | Feature preview sample |
| `working_data/cluster_statistics.csv` | ~1KB | Detailed cluster statistics |
| `working_data/cluster_summary.txt` | ~1KB | Human-readable analysis report |

---

## 🔍 Sample Results

### Cluster Profiles (from cluster_summary.txt)

**Cluster 0 - Recent Short Films:**
- Avg Release Year: 2019
- Avg Duration: 85 minutes
- Avg Title Length: 19 characters
- Avg Number of Genres: 1.0

**Cluster 1 - Classic Long Films:**
- Avg Release Year: 2005
- Avg Duration: 111 minutes
- Avg Title Length: 28 characters
- Avg Number of Genres: 3.0

**Cluster 2 - Mid-Era Medium Films:**
- Avg Release Year: 2015
- Avg Duration: 107 minutes
- Avg Title Length: 19 characters
- Avg Number of Genres: 2.0

---

## 🛠️ Technical Details

- **Clustering Algorithm:** K-Means with k-means++ initialization
- **Optimization:** Elbow method using KneeLocator
- **Feature Scaling:** MinMaxScaler (0-1 normalization)
- **Optimal k:** Typically 3-4 clusters
- **Dataset Size:** ~6,000-8,000 movies after filtering

---

## 📈 Key Differences from Template

| Aspect | Template | Enhanced Version |
|--------|----------|------------------|
| **Features** | 3 | **6** |
| **Tasks** | 4 | **6** |
| **Visualization** | None | **Elbow plot** |
| **Analysis** | None | **Statistical reports** |
| **Output Files** | 1 | **5** |
| **Parallel Execution** | No | **Yes (3 tasks)** |

---

## 🎓 Learning Outcomes

- Apache Airflow DAG creation and task dependencies
- Parallel task execution optimization
- K-Means clustering implementation
- Feature engineering for better clustering
- Data visualization with Matplotlib
- Statistical analysis and reporting

---

## 📚 References

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Scikit-learn K-Means](https://scikit-learn.org/stable/modules/clustering.html#k-means)
- [Original Lab Instructions](https://www.mlwithramin.com/blog/airflow-lab1)

---

## 👤 Author

**Harini Vasisht**  
MS Data Analytics Engineering  
Northeastern University  
GitHub: [@hvasisht](https://github.com/hvasisht)

---

## 📝 Submission Summary

✅ Enhanced feature engineering (6 features)  
✅ Added visualization task (elbow plot)  
✅ Added cluster analysis task (reports)  
✅ Implemented parallel task execution  
✅ Generated 5 output files  
✅ Clearly differentiated from template# Airflow lab

- In order to install Airflow using docker you can watch our [Airflow Lab1 Tutorial Video](https://youtu.be/exFSeGUbn4Q?feature=shared)
- For latest step-by-step instructions, check out this blog - [AirFlow Lab-1](https://www.mlwithramin.com/blog/airflow-lab1)

### ML Model

This script is designed for data clustering using K-Means clustering and determining the optimal number of clusters using the elbow method. It provides functionality to load data from a CSV file, perform data preprocessing, build and save a K-Means clustering model, and determine the number of clusters based on the elbow method.

#### Prerequisites

Before using this script, make sure you have the following libraries installed:

- pandas
- scikit-learn (sklearn)
- kneed
- pickle

#### Usage

You can use this script to perform K-Means clustering on your dataset as follows:

```python
# Load the data
data = load_data()

# Preprocess the data
preprocessed_data = data_preprocessing(data)

# Build and save the clustering model
sse_values = build_save_model(preprocessed_data, 'clustering_model.pkl')

# Load the saved model and determine the number of clusters
result = load_model_elbow('clustering_model.pkl', sse_values)
print(result)
```

#### Functions

1. **load_data():**
   - *Description:* Loads data from a CSV file, serializes it, and returns the serialized data.
   - *Usage:*
     ```python
     data = load_data()
     ```

2. **data_preprocessing(data)**
   - *Description:* Deserializes data, performs data preprocessing, and returns serialized clustered data.
   - *Usage:*
     ```python
     preprocessed_data = data_preprocessing(data)
     ```

3. **build_save_model(data, filename)**
   - *Description:* Builds a K-Means clustering model, saves it to a file, and returns SSE values.
   - *Usage:*
     ```python
     sse_values = build_save_model(preprocessed_data, 'clustering_model.pkl')
     ```

4. **load_model_elbow(filename, sse)**
   - *Description:* Loads a saved K-Means clustering model and determines the number of clusters using the elbow method.
   - *Usage:*
     ```python
     result = load_model_elbow('clustering_model.pkl', sse_values)
     ```
### Airflow Setup

Use Airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The Airflow scheduler executes your tasks on an array of workers while following the specified dependencies.

References

-   Product - https://airflow.apache.org/
-   Documentation - https://airflow.apache.org/docs/
-   Github - https://github.com/apache/airflow

#### Installation

Prerequisites: You should allocate at least 4GB memory for the Docker Engine (ideally 8GB).

Local

-   Docker Desktop Running

Cloud

-   Linux VM
-   SSH Connection
-   Installed Docker Engine - [Install using the convenience script](https://docs.docker.com/engine/install/ubuntu/#install-using-the-convenience-script)

#### Tutorial

1. Create a new directory

    ```bash
    mkdir -p ~/app
    cd ~/app
    ```

2. Running Airflow in Docker - [Refer](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#running-airflow-in-docker)

    a. You can check if you have enough memory by running this command

    ```bash
    docker run --rm "debian:bullseye-slim" bash -c 'numfmt --to iec $(echo $(($(getconf _PHYS_PAGES) * $(getconf PAGE_SIZE))))'
    ```

    b. Fetch [docker-compose.yaml](https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml)

    ```bash
    curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.5.1/docker-compose.yaml'
    ```

    c. Setting the right Airflow user

    ```bash
    mkdir -p ./dags ./logs ./plugins ./working_data
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

    d. Update the following in docker-compose.yml

    ```bash
    # Donot load examples
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'

    # Additional python package
    _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:- pandas }

    # Output dir
    - ${AIRFLOW_PROJ_DIR:-.}/working_data:/opt/airflow/working_data

    # Change default admin credentials
    _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow2}
    _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow2}
    ```

    e. Initialize the database

    ```bash
    docker compose up airflow-init
    ```

    f. Running Airflow

    ```bash
    docker compose up
    ```

    Wait until terminal outputs

    `app-airflow-webserver-1  | 127.0.0.1 - - [17/Feb/2023:09:34:29 +0000] "GET /health HTTP/1.1" 200 141 "-" "curl/7.74.0"`

    g. Enable port forwarding

    h. Visit `localhost:8080` login with credentials set on step `2.d`

3. Explore UI and add user `Security > List Users`

4. Create a python script [`dags/sandbox.py`](dags/sandbox.py)

    - BashOperator
    - PythonOperator
    - Task Dependencies
    - Params
    - Crontab schedules

    You can have n number of scripts inside dags dir

5. Stop docker containers

    ```bash
    docker compose down
    ```
### Airflow DAG Script

This Markdown file provides a detailed explanation of the Python script that defines an Airflow Directed Acyclic Graph (DAG) for a data processing and modeling workflow.

#### Script Overview

The script defines an Airflow DAG named `your_python_dag` that consists of several tasks. Each task represents a specific operation in a data processing and modeling workflow. The script imports necessary libraries, sets default arguments for the DAG, creates PythonOperators for each task, defines task dependencies, and provides command-line interaction with the DAG.

#### Importing Libraries

```python
# Import necessary libraries and modules
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from src.lab import load_data, data_preprocessing, build_save_model, load_model_elbow
from airflow import configuration as conf
```
The script starts by importing the required libraries and modules. Notable imports include the `DAG` and `PythonOperator` classes from the `airflow` package, datetime manipulation functions, and custom functions from the `src.lab` module.



#### Enable pickle support for XCom, allowing data to be passed between tasks
```python
conf.set('core', 'enable_xcom_pickling', 'True')
```

#### Define default arguments for your DAG
```python
default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 9, 17),
    'retries': 0,  # Number of retries in case of task failure
    'retry_delay': timedelta(minutes=5),  # Delay before retries
}
```
Default arguments for the DAG are specified in a dictionary named default_args. These arguments include the DAG owner's name, the start date, the number of retries, and the retry delay in case of task failure.

#### Create a DAG instance named 'your_python_dag' with the defined default arguments
``` python 
dag = DAG(
    'your_python_dag',
    default_args=default_args,
    description='Your Python DAG Description',
    schedule_interval=None,  # Set the schedule interval or use None for manual triggering
    catchup=False,
)
```
Here, the DAG object dag is created with the name 'your_python_dag' and the specified default arguments. The description provides a brief description of the DAG, and schedule_interval defines the execution schedule (in this case, it's set to None for manual triggering). catchup is set to False to prevent backfilling of missed runs.


#### Task to load data, calls the 'load_data' Python function
``` python 
load_data_task = PythonOperator(
    task_id='load_data_task',
    python_callable=load_data,
    dag=dag,
)
```

#### Task to perform data preprocessing, depends on 'load_data_task'
```python 
data_preprocessing_task = PythonOperator(
    task_id='data_preprocessing_task',
    python_callable=data_preprocessing,
    op_args=[load_data_task.output],
    dag=dag,
)
```
The 'data_preprocessing_task' depends on the 'load_data_task' and calls the data_preprocessing function, which is provided with the output of the 'load_data_task'.

#### Task to build and save a model, depends on 'data_preprocessing_task'
```python
build_save_model_task = PythonOperator(
    task_id='build_save_model_task',
    python_callable=build_save_model,
    op_args=[data_preprocessing_task.output, "model.sav"],
    provide_context=True,
    dag=dag,
)
```
The 'build_save_model_task' depends on the 'data_preprocessing_task' and calls the build_save_model function. It also provides additional context information and arguments.

#### Task to load a model using the 'load_model_elbow' function, depends on 'build_save_model_task'
``` python
load_model_task = PythonOperator(
    task_id='load_model_task',
    python_callable=load_model_elbow,
    op_args=["model.sav", build_save_model_task.output],
    dag=dag,
)
```
The 'load_model_task' depends on the 'build_save_model_task' and calls the load_model_elbow function with specific arguments.

#### Set task dependencies
```python
load_data_task >> data_preprocessing_task >> build_save_model_task >> load_model_task
```
Task dependencies are defined using the >> operator. In this case, the tasks are executed in sequence: 'load_data_task' -> 'data_preprocessing_task' -> 'build_save_model_task' -> 'load_model_task'.

#### If this script is run directly, allow command-line interaction with the DAG
```python
if __name__ == "__main__":
    dag.cli()
```
- Lastly, the script allows for command-line interaction with the DAG. When the script is run directly, the dag.cli() function is called, providing the ability to trigger and manage the DAG from the command line.
- This script defines a comprehensive Airflow DAG for a data processing and modeling workflow, with clear task dependencies and default arguments.

### Running an Apache Airflow DAG Pipeline in Docker

This guide provides detailed steps to set up and run an Apache Airflow Directed Acyclic Graph (DAG) pipeline within a Docker container using Docker Compose. The pipeline is named "your_python_dag."

#### Prerequisites

- Docker: Make sure Docker is installed and running on your system.

#### Step 1: Directory Structure

Ensure your project has the following directory structure:

```plaintext
your_airflow_project/
├── dags/
│   ├── airflow.py     # Your DAG script
├── src/
│   ├── lab.py                # Data processing and modeling functions
├── data/                       # Directory for data (if needed)
├── docker-compose.yaml         # Docker Compose configuration
```

#### Step 2: Docker Compose Configuration
Create a docker-compose.yaml file in the project root directory. This file defines the services and configurations for running Airflow in a Docker container.

#### Step 3: Start the Docker containers by running the following command

```plaintext
docker compose up
```

Wait until you see the log message indicating that the Airflow webserver is running:

```plaintext
app-airflow-webserver-1 | 127.0.0.1 - - [17/Feb/2023:09:34:29 +0000] "GET /health HTTP/1.1" 200 141 "-" "curl/7.74.0"
```

#### Step 4: Access Airflow Web Interface
- Open a web browser and navigate to http://localhost:8080.

- Log in with the credentials set in the .env file or use the default credentials (username: admin, password: admin).

- Once logged in, you'll be on the Airflow web interface.

#### Step 5: Trigger the DAG
- In the Airflow web interface, navigate to the "DAGs" page.

- You should see the "your_python_dag" listed.

- To manually trigger the DAG, click on the "Trigger DAG" button or enable the DAG by toggling the switch to the "On" position.

- Monitor the progress of the DAG in the Airflow web interface. You can view logs, task status, and task execution details.

#### Step 6: Pipeline Outputs

- Once the DAG completes its execution, check any output or artifacts produced by your functions and tasks. 
