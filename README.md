
Course Enrollment API Microservice

This project aims to create a RESTful web service with FastAPI for course enrollment, authentication, and
notifications.I have used krakend for API gateway implementation. Redis is used for wait lists, DynamoDB local for enrollment data partitioning,
and RabbitMQ integration is done for precise email and Webhook notifications to subscribers.



# Development

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
