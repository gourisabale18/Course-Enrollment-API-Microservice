import boto3, botocore
from dataclasses import dataclass

dynamo_db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# Delete table if it already exists
try:
    dynamo_db.Table("enrollments").delete()
except botocore.exceptions.ClientError:
    pass

table = dynamo_db.create_table(
    TableName = 'enrollments',
    KeySchema = [ 
        {
            'AttributeName': 'section_id',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'student_id',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions = [
        {
            "AttributeName": "section_id",
            "AttributeType": "N"
        },
        {
            "AttributeName": "student_id",
            "AttributeType": "N"
        }
    ],
    ProvisionedThroughput={
        "ReadCapacityUnits": 10,
        "WriteCapacityUnits": 10,
    },
)

@dataclass
class Item:
    student_id: int
    section_id: int
    add_date: str
    is_dropped: bool

table.put_item(
    Item = Item(1, 1, '4/20/2023', 0).__dict__
)
table.put_item(
    Item = Item(1, 2, '4/20/2023', 0).__dict__
)
table.put_item(
    Item = Item(2, 2, '4/20/2023', 1).__dict__
)
table.put_item(
    Item = Item(2, 3, '4/20/2023', 0).__dict__
)
table.put_item(
    Item = Item(3, 2, '4/20/2023', 1).__dict__
)
table.put_item(
    Item = Item(3, 3, '4/20/2023', 0).__dict__
)
table.put_item(
    Item = Item(3, 4, '4/20/2023', 0).__dict__
)
