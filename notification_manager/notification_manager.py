import boto3
import json
import os


def lambda_handler(event, context):
    print(event)
    # TODO: Use the contents of the NotificationTargetsTable to set up subscriptions with message attribute filters