def create_secret(event, context):
    print('It works!')
    return {
        'statusCode': 200,
        'body': 'It Works!'
    }