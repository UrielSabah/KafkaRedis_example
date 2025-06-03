# Python Client

This mini-project contains a Python 3 application that subscribes to a topic on a Confluent Cloud Kafka cluster and sends a sample message, then consumes it and prints the consumed record to the console.

Also uses Redis for caching :)

## Prerequisites

This project assumes that you already have:
- Python 3 installed. The template was last tested against Python 3.13.1.

## Installation

Create and activate a Python `venv` environment, so that you have an isolated workspace:

```shell
python3 -m venv venv
source env/bin/activate 
```

Install the dependencies of this application:

```shell
pip3 install -r requirements.txt
```

## Usage + Debugging with PyCharm

To set up a PyCharm Run/Debug Configuration for your project, follow these steps:

- Click Run > Edit Configurations...
- Click the + icon (Add New Configuration) and choose Python.
- Configure the settings as follows:
  - Name: getting_started_with_kafka_and_redis.
  - Module name: Enter uvicorn.
  - Parameters: Enter app.main:app --reload.
  - Python interpreter: Select your project's virtual environment (e.g., env or env/bin/python).
  - Working directory: Set this to the root directory of your project.

## Running the API from CLI
Start the development server:
```
    uvicorn app.main:app --reload
```


## API Endpoints
#### 1. Retrieve user data + publish request(GET)
```
  GET http://127.0.0.1:8000/user/<user_id>
```

| Parameter | Type  | Description  |
|:----------|:------|:-------------|
| `user_id` | `int` | **Required** |

This endpoint retrieves information about a specific user by its user_id. It uses caching for 60 seconds. 
Also publishes the data from the user

Example Request:
```
  GET http://127.0.0.1:8000/user/<user_id>
```

Example Response:
```
{
    "status": "success",
    "event": {
        "user_id": 1787,
        "action": "play",
        "context": {
            "movie": "Matrix"
        }
    }
}
```

#### 2. Consumes user data(GET)
```
  GET http://127.0.0.1:8000/events/consume
```

This endpoint consumes published user_id data events 

Example Request:
```
  GET http://127.0.0.1:8000/events/consume
```

Example Response:
```
{
    "messages": [
        {
            "key": "122",
            "event": {
                "user_id": 122,
                "action": "play",
                "context": {
                    "movie": "Inception"
                }
            }
        },
        {
            "key": "1787",
            "event": {
                "user_id": 1787,
                "action": "play",
                "context": {
                    "movie": "Matrix"
                }
            }
        }
    ]
}
```