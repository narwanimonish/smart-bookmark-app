import json
import os

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ.get("TABLE_NAME"))


def handler(event, context):
    try:
        # Scan is okay for small demos; use Query with GSI for production!
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(items),
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
