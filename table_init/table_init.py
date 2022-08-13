import json
import yaml
import boto3
import requests


def load_items(filename):
    file = open(filename, "r")
    y = file.read()
    file.close()
    return yaml.safe_load(y)


def lambda_handler(event, context):
    print(json.dumps(event))
    tables = load_items('tables.yaml')
    if event['RequestType'] == 'Delete':
        # Just return the response.
        # The table deletion will clean up the items.
        pass

    elif event['RequestType'] in ["Create", "Update"]:
        dydbResource = boto3.resource("dynamodb")
        for table_name, records in tables.items():
            dydbTable = dydbResource.Table(table_name)
            for record in records:
                dydbTable.put_item(
                    Item=record
                )

    responseStatus = 'SUCCESS'
    responseData = {
        'Success': 'Test Passed.'
    }
    sendResponse(
        event,
        context,
        responseStatus,
        responseData
    )


def sendResponse(event, context, responseStatus, responseData):
    responseBody = {'Status': responseStatus,
                    'Reason': 'See the details in CloudWatch Log Stream: ' + context.log_stream_name,
                    'PhysicalResourceId': context.log_stream_name,
                    'StackId': event['StackId'],
                    'RequestId': event['RequestId'],
                    'LogicalResourceId': event['LogicalResourceId'],
                    'Data': responseData}
    print ('RESPONSE BODY:n' + json.dumps(responseBody))
    try:
        req = requests.put(event['ResponseURL'], data=json.dumps(responseBody))
        if req.status_code != 200:
            print (req.text)
            raise Exception('Recieved non 200 response while sending response to CFN.')
        return
    except requests.exceptions.RequestException as e:
        print (e)
        raise
