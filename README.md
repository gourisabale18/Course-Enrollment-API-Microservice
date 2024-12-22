
## Course Enrollment API Microservice

## Project Overview
This project is an immersive exercise in implementing polyglot persistence, a contemporary approach to database management in web back-end systems. The core of this project revolves around the integration of Redis and DynamoDB Local, two robust and versatile database systems.

### Tech Stack Used:
1. Python FastAPI web application framework
2. Krakend API gateway
3. JWT token authentication
4. RabbitMQ, Webhooks
5. AWS Dynamo DB Local
6. Microservices, Swagger APIs
7. GraphQL Queries, SQLite database
8. Redis cache

## Project Objectives
In this project, our goal is to immerse ourselves in the world of polyglot persistence, a key aspect of modern back-end development. We will achieve this by integrating two distinct database systems - Redis and Amazon DynamoDB Local - into our existing back-end architecture. Our approach involves a strategic split of data between these databases, utilizing each for its strengths.
### Database Configuration:
   Configure and fine-tune Redis and DynamoDB Local.
   Ensure both databases are seamlessly integrated into our back-end setup.
### Data Partitioning:
   Allocate waiting list data to Redis, leveraging its high performance and scalability for real-time data handling.
   Store all other data in DynamoDB Local, utilizing its robustness and consistency for comprehensive data management.
### Functional Partitioning:
   Implement functional partitioning within the enrollment service.
   Optimize each database's functionality to support specific aspects of the service.
### Data Modeling:
   Develop a tailored data model for each database.
   Ensure that the data models align with our application's requirements and the databases' capabilities.
### Testing:
   Conduct thorough testing of enrollment API endpoints.
   Validate the effectiveness of our polyglot persistence approach in handling diverse data needs.

## Project Tasks
To successfully implement our project goals, we have outlined a series of tasks that cover the entire scope of integrating polyglot persistence using Redis and DynamoDB Local in our back-end setup. These tasks are designed to ensure a comprehensive and methodical approach to the project:

### Installation and Configuration:
   ●	Redis Configuration: Setting up and configuring Redis to work seamlessly with our back-end.
   ●	AWS CLI Installation: Installing the AWS Command Line Interface, essential for interacting with Amazon Web Services.
   ●	DynamoDB Local Setup: Installing and configuring DynamoDB Local for a development environment.
### SDK Installation and Usage:
   ●	AWS SDK for Python (Boto3) Installation: Installing the AWS SDK to enable Python applications to interact with DynamoDB Local.
   ●	Connecting to DynamoDB Local from Python: Establishing a connection between our Python applications and DynamoDB Local.
### Data Partitioning for Enrollment Service:
   ●	Redis for Waiting Lists: Utilizing Redis for managing waiting list data due to its efficiency in handling real-time, mutable data.
   ●	DynamoDB Local for Other Data: Storing other types of data in DynamoDB
   Local, leveraging its capabilities for handling larger and more complex data sets.
### Database Design and Modeling:
   ●	Redis Data Model: Designing a data model for Redis that optimizes its key-value store nature.
   ●	DynamoDB Local Data Model: Creating a data model for DynamoDB Local, considering its NoSQL characteristics.
   ●	Indexing and Query Optimization: Implementing indexing strategies and query optimizations to enhance database performance.
### Testing and Validation:
   ●	Endpoint Functionality Tests: Conducting tests to ensure that all API endpoints function as expected, interacting correctly with both Redis and DynamoDB Local.
   ●	Data Integrity Checks: Performing checks to ensure data integrity and consistency across both databases.

## Project Requirements
To ensure the smooth execution and success of our polyglot persistence project, there are several key requirements that must be met. These requirements are crucial for creating an efficient and effective development environment, particularly given our focus on integrating Redis and DynamoDB Local. Here's what we need:
### Operating System:
   ●	Ubuntu 22
### Database Systems:
   ●	Redis Installation: Redis must be installed and properly configured on all team members' systems. Redis will play a crucial role in managing real-time, mutable data such as waiting lists.
   ●	DynamoDB Local Installation: We need to install DynamoDB Local to handle more complex data sets. This will allow us to simulate the AWS DynamoDB environment locally for development and testing purposes.
### Programming Language and Libraries:
   ●	Python Setup: As our primary programming language, Python needs to be installed on all machines. Ensure that the Python version is compatible with all the tools and libraries we will be using.
   ●	Necessary Python Libraries: Several Python libraries are integral to our project. This includes Boto3 for AWS interactions, libraries for connecting and interacting with Redis, and any other libraries essential for our project's development.
### Development Tools:
   ●	IDEs and Code Editors: Team members should have their preferred Integrated Development Environments (IDEs) and code editors ready. These tools should support Python development and be compatible with Tuffix 2022.
   ●	Version Control: A version control system, like Git, will be necessary for collaborative development and code management.
### Documentation and Reporting Tools:
   ●	Documentation Software: Since documentation is key to our project's success, we should have access to tools for creating and managing documentation, such as Markdown editors or LaTeX for more formal documentation needs.


### Development

1. Set working directory as this project's directory

2. Create and enter virtual environment

   ```bash
   python3.10 -m venv .venv
   source .venv/bin/activate
   ```

3. Install requirements

   ```bash
   pip install -r requirements.txt
   ```

4. Configure Redis CLI

   You will need to have Redis CLI installed and running on the system at port 6379. You can verify this by running the following command:

   ```bash
   redis-cli ping
   ```

   Otherwise install redis:
   ```bash
   sudo apt update
   sudo apt install --yes redis
   ```

5. Configure AWS CLI

   You will need to follow the instructions on the Long-term credentials tab of [Configuring using AWS CLI commands](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html#getting-started-quickstart-new-command) to configure dummy credentials for DynamoDB local.


6. Start API

   ```bash
   foreman start
   ```

7. Initialize databases
   
   If databases haven't been initialized yet (ie. this is the first run), run the following **after running one of the commands above, which activates the LiteFS replication service**:

   ```bash
   ./bin/init.sh
   ```

   You may also wish to run this in development to reset the database, especially if a schema has been changed.

   ## Project Tasks Screenshots
   1.	Subscribe to notifications for a new course
      ![image](https://github.com/user-attachments/assets/a28ca487-5331-4010-bde1-55a987cdfba9)
     	
      ![image](https://github.com/user-attachments/assets/5191c477-97b9-41ec-8b0a-8f788a3ce0cd)

   2.	List their current subscriptions
     ![image](https://github.com/user-attachments/assets/0948d000-6228-4c4e-b86d-2450dce7f721)

   3.	Unsubscribe from a course
      ![image](https://github.com/user-attachments/assets/b5c61cc4-e01a-4f06-8972-151676cc0240)
     	
   4.	Consume an enrollment notification
      a.	Subscribe a student to the notification service
     	![image](https://github.com/user-attachments/assets/6c5dc8e6-e595-4735-a994-65700c3ff1e7)
     	
     	b.	Attempt to enroll the student in a class that is full to be added to the waitlist
     	![image](https://github.com/user-attachments/assets/2670b058-6183-4321-9c7e-ac084b44c78b)

      c.	Drop another student from the waitlist so waitlisted student will be auto enrolled
      ![image](https://github.com/user-attachments/assets/d9ad5365-5c05-452c-9ec5-81de2a2b58a1)

      d.	Check notification in the console
      ![image](https://github.com/user-attachments/assets/6aa007d8-631a-4c69-88e8-c9f93702285c)

   5.	Cache waiting list positions
      a.	Attempt to enroll a student in a class that is full so they are added to waitlist
     	![image](https://github.com/user-attachments/assets/7c48d711-47e8-400f-9cbf-9a4ff10a5cd8)

      b.	Check position in the browser and look at response code
      ![image](https://github.com/user-attachments/assets/c7ecaab6-b7dc-416a-b7d5-9b975562d90a)
   
   Here we see the return was successful given the response and the status code returned

      ![image](https://github.com/user-attachments/assets/c337c206-c16d-4d67-8a13-e922f0bfc7f1)



