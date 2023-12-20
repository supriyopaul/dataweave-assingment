### Problem Statement

#### Assignment Overview

The task involves building three small applications:

1. **First App**: This application will read a file containing crawled data and transport it to the second application using a mechanism like RabbitMQ.

2. **Second App**: This app consumes the transported data, persists it in a storage layer on an individual product level, and performs aggregated calculations such as calculating a score.

3. **Third App**: This application exposes an API that allows users to retrieve the score for an account or individual products by the account. An authentication layer is not required.

#### Language and Framework Preferences
- **Programming Language**: Python is the preferred language.
- **Web Frameworks**: Any Python web framework can be used.
- **Messaging Frameworks**: Any suitable messaging framework is acceptable.

#### Assumptions
- Assumptions can be made wherever necessary.

#### Specific Requirements

##### App 1: Producer
- Write a producer that reads JSON data from a file and sends this data to a messaging queue like RabbitMQ.

##### App 2: Consumer
- Write a consumer that reads data from the messaging queue, sanitizes the data, and writes it to a database (e.g., PostgreSQL, MySQL).

###### Database Design
- Design a database schema with all fields relevant for score computation.
- Use an appropriate database (e.g., SQLite) and provide the SQL script for creating the necessary tables.

###### Object-Oriented Programming
- Follow OOP best practices while defining classes and functions.

##### App 3: Web API
- Create a RESTful API using a Python web framework (e.g., Flask, Django, FastAPI) for score computation.
- Include endpoints to retrieve all the data from the table and the score API.

#### Submission Guidelines
- Submissions can be via GitHub or other version control utilities with instructions for execution.
- Include sample API requests and responses.
- Dockerizing the solution is considered an added advantage.

#### Evaluation Criteria
- Database design and normalization.
- Adherence to OOP principles in Python.
- Proper use of a web framework to create a RESTful API.
- Correctness and efficiency of database queries.
- Efficient message handling.

#### Additional Information
- **Availability Score Calculation**: `availability_score = total in-stock products / total products tracked`.
- A file with raw crawler data will be provided for sampling purposes.


### Data JSON Explanation

The JSON file `assignment_updated.json` contains a series of records, each representing data about products crawled from an online source. Here's an explanation of the data fields in each record:

1. **index**: A numeric identifier for each record, starting from 0 and incrementing sequentially.

2. **meta_info**: A string containing a nested JSON object with detailed metadata for each product. The fields within `meta_info` include:
   - `account_code`: Identifier for the account under which the product was crawled.
   - `crawl_page_counter`: The page number from where the product was crawled.
   - `postal_zip_code`: The postal or ZIP code associated with the location of the store or product.
   - `postal_zip_name`: Name of the postal or ZIP area.
   - `store_code`: Code identifying the store.
   - `place_name`: Name of the place where the store or product is located.
   - `admin_name1`: Administrative area (like a state or province) where the store or product is located.
   - `bundle_versions_row_pk_hash`, `bundle_variant_field_mapping`, `bundle_definition`, `fulfilment_modes`, `seller_name`, `bundle_match_type`, `reference_product_id`, `bundle_definition_hash`: Various fields related to product bundling, seller information, and fulfillment methods.

3. **available_price**: The price of the product. A negative value might indicate a data error or a specific condition (like out of stock or not available).

4. **stock**: Indicates the stock status of the product, e.g., "In Stock" or "Out Of Stock".

5. **source**: The source from which the product data was crawled, e.g., "Amazon-US".

This data structure provides comprehensive information about each product, which can be used for various purposes such as inventory management, price tracking, and market analysis.

### Detailed Solution for the Assignment

#### System Architecture and Design

1. **Overall Architecture**:
   - Three separate applications (Producer, Consumer, Web API) interacting through RabbitMQ and a database.
   - Data flow: Producer → RabbitMQ → Consumer → Database → Web API.

2. **Producer Application**:
   - Reads JSON data from a file.
   - Use batch-proccessing for larger files.
   - Sends data to RabbitMQ.
   - Libraries: `pika` for RabbitMQ interaction.

3. **Consumer Application**:
   - Consumes data from RabbitMQ.
   - Sanitizes and persists data to a database.
   - Use bulk insert
   - Multiprocessing for more consumers
   - Idempotency
   - ORM
   - Pydantic Models
   - Module for transformation
   - Libraries: `pika` for RabbitMQ, ORM tool like `SQLAlchemy` for database interaction.

4. **Web API Application**:
   - Exposes RESTful API to retrieve scores and product data.
   - /products with pagenation
   - /score for availiblity
   - Frameworks: Flask or FastAPI for API development.

5. **Messaging Framework**:
   - RabbitMQ as the message broker.
   - Ensure idempotency in message processing.

#### Database Design

1. **Schema**:
   - **Products Table**: Stores individual product data.
     - Fields: `product_id`, `account_code`, `price`, `stock_status`, `source`, etc.
   - **Accounts Table**: Stores account information.
     - Fields: `account_id`, `account_code`, `total_products`, `in_stock_products`.

2. **Score Calculation**:
   - `availability_score` calculation can be done on the fly using a SQL query.

3. **Normalization**:
   - Ensure normalization to reduce redundancy and improve data integrity.

#### Best Suited Libraries/Frameworks

1. **Python Web Frameworks**:
   - Flask: Lightweight, easy to use.
   - FastAPI: Modern, fast, supports async, ideal for APIs.

2. **Messaging Frameworks**:
   - `pika` for RabbitMQ integration.
   - Ensures reliable and efficient message handling.

3. **ORM and Database**:
   - SQLAlchemy: Robust ORM for database interactions.
   - SQLite for simplicity, or PostgreSQL/MySQL for production.

4. **Testing and Quality Assurance**:
   - `pytest` for unit and integration testing.
   - `flake8` and `black` for code formatting and linting.

#### Coding Patterns and Best Practices

1. **Object-Oriented Programming**:
   - Encapsulation: Define classes with private variables and public methods.
   - Inheritance: Use abstract classes for common functionality.
   - Polymorphism: Utilize interfaces and abstract methods for flexible code.

2. **Code Quality**:
   - Follow PEP8 guidelines for Python code.
   - Write modular, reusable, and testable code.
   - Document code extensively.

3. **Error Handling and Logging**:
   - Implement comprehensive error handling.
   - Use logging for debugging and monitoring.

4. **Security**:
   - Secure RabbitMQ and database connections.
   - Sanitize input data to prevent SQL injection.

#### Submission and Documentation

1. **Version Control**:
   - Use Git for version control.
   - Host code on GitHub with a README file for instructions.

2. **Dockerization**:
   - Create Dockerfiles for each application.
   - Provide a docker-compose.yml for easy setup and deployment.

3. **API Documentation**:
   - Document API endpoints with examples.
   - Use tools like Swagger for API documentation.

#### Evaluation Criteria Compliance

- **Database Design**: Efficient schema with normalized tables.
- **OOP Principles**: Adherence to OOP best practices.
- **RESTful API**: Use of Flask/FastAPI for API development.
- **Database Queries**: Efficient and correct SQL queries for score calculation.
- **Message Handling**: Robust handling with RabbitMQ and pika.

This solution provides a comprehensive approach to building the three applications, ensuring scalability, maintainability, and efficiency.