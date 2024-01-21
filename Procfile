users-primary: ./bin/litefs mount -config ./etc/litefs/users-primary.yml
users-secondary: ./bin/litefs mount -config ./etc/litefs/users-secondary.yml
users-tertiary: ./bin/litefs mount -config ./etc/litefs/users-tertiary.yml
enrollment: uvicorn --port $PORT api.services.enrollment.main:app --reload
notification: uvicorn --port $PORT api.services.notification.main:app --reload
krakend: echo ./etc/krakend.json | entr -nrz krakend run --config etc/krakend.json --port $PORT
amazon-dynamodb-local: java -Djava.library.path=./bin/DynamoDBLocal_lib -jar ./bin/DynamoDBLocal.jar -sharedDb -dbPath ./var/db/enrollment/ -port 8000

email-worker: python3 share/notification/rabbitmq/recieve_email.py
webhook-worker: python3 share/notification/rabbitmq/recieve_webhook.py

smtpd: python -m aiosmtpd -n -d