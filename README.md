# DataWeave Assignment

## Prerequisites

- Python 3.9
- Docker
- Basic knowledge of command-line operations

## Installation

### Setting Up the Environment

1. Create a Python virtual environment and activate it:

   ```bash
   python3.9 -m venv ./venv
   source ./venv/bin/activate
   ```

2. Navigate to the project directory:

   ```bash
   cd dataweave-assingment/
   ```

3. Upgrade pip to the latest version:

   ```bash
   python3.9 -m pip install --upgrade pip
   ```

### Setting Up RabbitMQ with Docker

1. Pull the RabbitMQ image:

   ```bash
   docker pull rabbitmq:3-management
   ```

2. Run the RabbitMQ container:

   ```bash
   docker network create dataweave-network
   docker run -d --rm -it --network dataweave-network --name rabbitmq -p 15672:15672 -p 5672:5672 rabbitmq:3-management
   ```

### Installing DataWeave

1. Install the DataWeave package:

   ```bash
   pip3.9 install .
   ```

## Configuration

1. Set the environment variables in the `.env` file:

   ```
   Q_HOST=localhost
   Q_NAME=products
   DB_URL=sqlite:///products.db
   WORKERS=1
   PORT=8000
   RABBIT_MQ=localhost:15672
   QUEUE=products
   ```

## Usage

### DataWeave Commands

- Get help and list available commands:

  ```bash
dataweave --help
usage: dataweave [-h] {runserver,runconsumer,ingest,create-db,delete-db} ...

CLI tool for managing server and RabbitMQ tasks

positional arguments:
  {runserver,runconsumer,ingest,create-db,delete-db}
                        commands
    runserver           Run the server
    runconsumer         Run the RabbitMQ consumer
    ingest              Ingest data
    create-db           Create the database
    delete-db           Delete the database

optional arguments:
  -h, --help            show this help message and exit
  ```
  ```bash
  dataweave create-db --help
  usage: dataweave create-db [-h] [--db-url DB_URL]

  optional arguments:
   -h, --help       show this help message and exit
   --db-url DB_URL  Database URL (default: "sqlite:///products.db")
  ```

- Create the database:

  ```bash
  dataweave create-db
  ```

- Start the RabbitMQ consumer:

  ```bash
  dataweave runconsumer
  ```

- Start the server:

  ```bash
  dataweave runserver
  ```
  **Note:** You can access the swagger on `http://0.0.0.0:8000/docs#` after running the server

- Ingest data from a JSON file:

  ```bash
  dataweave ingest --fpath assignment_updated.json
  ```
  **Note:** You can use the `/ingest` api for this
  <img width="1425" alt="image" src="https://github.com/supriyopaul/dataweave-assingment/assets/33823698/5dca23d3-66d6-4bbc-9331-dead42fae02a">


### API Endpoints

- Retrieve products:

  ```bash
  curl -X 'GET' 'http://0.0.0.0:8000/products?limit=20&offset=0' -H 'accept: application/json'
  ```
  <img width="1433" alt="Screenshot 2023-12-20 at 1 13 36 PM" src="https://github.com/supriyopaul/dataweave-assingment/assets/33823698/1aa50358-17e9-4405-aeac-8604b6d40d5e">
  <img width="1427" alt="image" src="https://github.com/supriyopaul/dataweave-assingment/assets/33823698/018d8565-2095-48f2-9d4e-3360a30e3921">


- Get score information:

  ```bash
  curl -X 'GET' 'http://0.0.0.0:8000/score/' -H 'accept: application/json'
  ```
  <img width="1425" alt="Screenshot 2023-12-20 at 1 14 21 PM" src="https://github.com/supriyopaul/dataweave-assingment/assets/33823698/017865ca-56c0-4785-b5eb-a874737d37a2">


## Dockerizing DataWeave Application

To containerize the DataWeave application, a Dockerfile is created. This Dockerfile will define the steps to set up the Python environment, install dependencies, and run the application within a Docker container. Additionally, the Docker commands for building and running the container will be provided, along with instructions on how to use the `.env` file for configuration.

### Building the Docker Image

To build the Docker image, use the following command in your project directory:

```bash
docker build -t dataweave-app .
```

This command builds the Docker image with the tag `dataweave-app`.

### Running the Docker Container

Before running the container, make sure you have an `.env` file with the necessary environment variables set up in your project directory. 

To run the Docker container with the `.env` file, use the following command:

```bash
docker run --name dataweave-container --network dataweave-network --env-file .env -p 8000:8000 dataweave-app
```

This command starts a new container named `dataweave-container` in detached mode. It loads environment variables from the `.env` file and maps port 8000 of the container to port 8000 on the host machine.

### Accessing the Application

Once the container is running, the DataWeave application should be accessible via `http://localhost:8000` on your host machine.
