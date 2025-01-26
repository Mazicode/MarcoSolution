# GameAnalyticsTest
## Fibonacci and Blacklist Service

This service implements two primary features:

1. A Fibonacci sequence calculation endpoint that supports efficient in-memory caching.
2. A blacklist feature that allows adding and removing numbers from a blacklist, using an optimized in-memory storage.

## Task Description

The goal of this service is to provide two features:

1. **Fibonacci Calculation**: A RESTful API that calculates the Fibonacci sequence for a given number. The Fibonacci sequence is calculated using both recursive methods (for the first draft) and optimized methods (with caching).
   
2. **Blacklist Management**: A simple system to add and remove numbers from a blacklist. It initially uses temporary in-memory lists to store blacklisted numbers, and later optimizes it using Redis to enhance performance and manage race conditions.

## Why FastAPI?

FastAPI was chosen for this project because it provides several advantages that make it a perfect fit for building high-performance APIs:

1. **Performance**: FastAPI is built on top of **Starlette** and **Pydantic**, making it one of the fastest Python frameworks available. It uses asynchronous programming to handle many requests concurrently, which is crucial for handling high-traffic applications efficiently.

2. **Automatic Data Validation**: FastAPI integrates **Pydantic** for data validation, which ensures that inputs to the API are automatically checked and validated, reducing boilerplate code and potential bugs.

3. **Asynchronous Support**: FastAPI's native support for asynchronous operations is beneficial when interacting with external services, like Redis, as well as handling I/O-bound tasks, such as waiting for database responses or slow API calls.

4. **Developer Productivity**: FastAPI has automatic interactive documentation using **Swagger** and **ReDoc**, making it easier to test and interact with the API without needing separate tools.

5. **Security and Authentication**: FastAPI provides built-in support for common security features like **OAuth2** and **JWT** token-based authentication, making it easy to add authentication and authorization mechanisms.

Overall, FastAPI allows us to build fast, scalable, and easy-to-maintain APIs with minimal effort, which is ideal for this project.

## Thinking Process: First Draft (Using Recursion and Simple Lists)

In the initial version of the application:

- **Fibonacci Calculation**: 
  We implemented a recursive approach to calculate Fibonacci numbers. While this approach is simple, it can be inefficient for larger numbers due to repeated calculations. The first draft used basic recursion without any caching.
  
- **Blacklist and Stored Numbers**: 
  We maintained a simple list to temporarily store blacklisted numbers. Numbers could be added or removed from the list using basic list operations in Python. However, this approach becomes slow as the number of blacklisted numbers grows, especially when handling requests concurrently.

## Optimizing the Service

### Replacing Recursion for Fibonacci

In the first draft, the Fibonacci sequence was computed using recursion. This method, while elegant, is highly inefficient due to redundant calculations. The Fibonacci sequence grows exponentially, so calculating the same Fibonacci numbers multiple times creates unnecessary overhead. We optimized this by using an **iterative approach** to calculate Fibonacci numbers, reducing time complexity to O(n).

### Introducing Redis for Optimized Caching

To handle the growing size of blacklisted numbers and improve performance, we switched to **Redis** for caching:

- **Redis**: This external data store is fast and efficient for temporary storage and retrieval, and it helps solve issues like race conditions that might occur when multiple requests try to update the blacklist at the same time.
  
- **Improved Performance**: Redis enables faster lookups and modifications compared to Python's in-memory lists, especially when handling a large number of requests. Redis also scales well for higher traffic, providing better support for future growth.

By using Redis, we avoid memory leaks and inconsistencies while managing state across multiple requests, ensuring higher scalability and performance.

## How to Run the App

### Requirements

To run the app, you must first install the required dependencies. 

After cloning the repository, you need to install the dependencies listed in `requirements.txt`. You can install them using `pip`:
    
   `
   pip install -r requirements.txt
   `

### Before running the app
Just to make sure you are running the service in the right work dir

    export PYTHONPATH=$(pwd)
   
### Running Locally
After installing the requirements, you can run the app locally using the following command:

    uvicorn app.main:app --host 0.0.0.0 --port 8000

The app will be available at http://localhost:8000.

### Running Using Docker
To run the application using Docker and Docker Compose, follow these steps:

    docker-compose up --build

The service will be accessible at http://localhost:8000.

This command will build the Docker image, set up the FastAPI application, and also run Redis in a separate container. The application will use Redis for caching and managing the blacklist.

### Running Tests locally
    pytest

## Testing the Endpoints:

### GET Fibonacci
To get the Fibonacci number for a given n, make a GET request to http://localhost:8000/fibonacci/{n}

### GET Fibonacci List
To get the Fibonacci list stored so far, make a GET request to http://localhost:8000/fibonacci

### POST Blacklist
To add a number to the blacklist, send a POST request to http://localhost:8000/blacklist with the number in the request body.

### DELETE Blacklist
To remove a number from the blacklist, send a DELETE request to http://localhost:8000/blacklist with the number in the request body.

### GET Health Check
Health Check: The app exposes a simple health check endpoint at http://localhost:8000/health.

## Future Steps for Improvements
While the service is functional and optimized, there are still some areas for further improvement:

### Error Handling:
Improve error handling, including custom exception handling, and provide more informative error messages for users when things go wrong (e.g., invalid input or system failures).

### Authentication and Authorization:
Add security layers such as JWT authentication to ensure that only authorized users can modify the blacklist.

### Rate Limiting:
Implement rate limiting for both Fibonacci and blacklist endpoints to prevent abuse and ensure the system can handle high loads.

### Persistent Storage:
Currently, Redis is being used as an in-memory cache. If persistence is required (i.e., data should survive a server restart), we could configure Redis to persist data to disk.

### Performance Metrics and Monitoring:
Integrate monitoring tools to track the application's performance (e.g., Prometheus or Grafana) and optimize based on real-time data.