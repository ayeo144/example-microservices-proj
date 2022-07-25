# Example microservices project

Simple example of a microservices project, developed while learning a bit about microservices architecture and messaging.

## Design

This is a very simple bare-bones design of an application which does some data processing for a user. The user interacts via a REST API, where they can request some data processing service. Their request is logged in a database and they are returned a unique code which can be used to later retrieve the results of the data processing. Meanwhile, their processing request is sent to a queue, which connects the REST API to the data processing service. The data processing service takes their request from the queue, does the processing, and then uses the REST API to update their request in the database. The user can use their unique code to request the results of processing from the REST API.

### Tools used:

1. Python + FastAPI for the REST API
2. Postgres for the database
3. RabbitMQ (with Python + pika) for the queue/messaging service