import json
import os
import uuid
import boto3
from datetime import datetime
from shared.scraper import scrape_metadata

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME'))

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        
        if not url: return {"statusCode": 400, "body": "URL is required"}

        # Scrape
        meta = scrape_metadata(url)
        
        item = {
            'bookmark_id': str(uuid.uuid4()),
            'created_at': datetime.utcnow().isoformat(),
            'url': url,
            'title': meta['title'],
            'description': meta['description'],
            'image_url': meta['image']
        }
        
        table.put_item(Item=item)

        return {
            "statusCode": 201,
            "headers": {"Access-Control-Allow-Origin": "*"},
            "body": json.dumps(item)
        }
    except Exception as e:
        return {"statusCode": 500, "body": str(e)}