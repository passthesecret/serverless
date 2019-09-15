import json
import os
from ptscore.manager import Manager

if 'PTS_DDB_SECRET_TABLE' in os.environ:
    from ptscore.storage.dynamodb import DynamoDB
    manager = Manager(DynamoDB())
else:
    from ptscore.storage.memorydb import MemoryDB
    manager = Manager(MemoryDB())


def create_secret(event, context):
    body = json.loads(event['body'])
    # Sanitize Secret Field
    if 'secret' not in body:
        return {'statusCode': 400, 'body': 'Request Must Contain Secret Field'}
    elif len(body['secret']) == 0:
        return {'statusCode': 400, 'body': 'Secret Must Be At Least One Character'}
    else:
        secret = body['secret']
    # Sanitize Expiration Field
    if 'expire_in_seconds' not in body:
        expire_in_seconds = 86400
    elif body['expire_in_seconds'] == 0:
        expire_in_seconds = 86400
    else:
        expire_in_seconds = int(body['expire_in_seconds'])
    # Sanitize Burn After Reading Field
    if 'burn_after_reading' not in body:
        burn_after_reading = False
    else:
        burn_after_reading = bool(body['burn_after_reading'])
    # Create The Secret
    create_response = manager.create_secret(secret, expire_in_seconds, burn_after_reading)
    # Return The URLs to The User
    return {
        'statusCode': 201,
        'body': json.dumps(create_response)
    }


def get_secret(event, context):
    try:
        get_response = manager.get_secret(event['pathParameters']['requestString'])
    except ValueError as err:
        return {'statusCode': 400, 'body': err.args[0]}
    except LookupError as err:
        return {'statusCode': 404, 'body': 'Not Found'}
    return {
        'statusCode': 200,
        'body': json.dumps(get_response)
    }
