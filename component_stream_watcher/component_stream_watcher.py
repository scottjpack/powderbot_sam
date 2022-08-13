import boto3
import json
import os


def lambda_handler(event, context):
    print(json.dumps(event))
    destination_sns_topic = os.environ['topic_arn']

    update_op = event['Records'][0]
    if update_op['eventName'] == "MODIFY":
        new_image = update_op['dynamodb']['NewImage']
        old_image = update_op['dynamodb']['OldImage']
        if "component_availability" in old_image.keys():
            component_name = new_image['component_name']['S']
            if not old_image['component_availability']['BOOL'] and new_image['component_availability']['BOOL']:
                print("Hallelujah, something is in stock.  Send to SNS")
                print(new_image)
                sns_client = boto3.client("sns")
                response = sns_client.publish(
                    TopicArn=destination_sns_topic,
                    Message=f'Component {component_name} is in stock!',
                    Subject=f'{component_name}',
                    MessageAttributes={
                        'component_name': {
                            'DataType': 'String',
                            'StringValue': component_name
                        }
                    }
                )