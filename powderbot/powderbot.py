import boto3

import random
import bs4  # pip install beautifulsoup4
import requests  # pip install requests
import os


COMPONENTS_TABLE_NAME = os.environ['components_table']

class Component(object):
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.available = None

def update_items(all_components, user_agent='powderbot/1.0'):
    dynamodb = boto3.resource('dynamodb')
    components_table = dynamodb.Table(COMPONENTS_TABLE_NAME)

    headers = {
        'User-Agent': user_agent
    }

    print('Refreshing inventory list')

    for name in all_components:
        component = all_components[name]

        # Download the product page
        r = requests.get(component.url, headers=headers)
        if r.status_code != 200:
            print(f'  ERROR - {r.status_code}')
            continue

        # Get availability from meta tag
        soup = bs4.BeautifulSoup(r.content, 'html.parser')
        availability = soup.find("meta", property="product:availability")
        is_available = availability.get("content") == 'instock'
        # Update component's availability
        component.available = is_available
        print(f"Setting {name} availability as {is_available}")
        components_table.update_item(
            Key={'component_name': name},
            AttributeUpdates={
                "component_availability":
                {
                    "Value": component.available,
                    "Action": "PUT"
                }
            }
        )
    return


def load_components():
    # Load the component names and urls
    dynamodb = boto3.resource('dynamodb')
    components_table = dynamodb.Table(COMPONENTS_TABLE_NAME)
    components = {}
    items = components_table.scan()
    for component in items['Items']:
        components[component['component_name']] = Component(component['component_name'], component['component_url'])
    return components


def lambda_handler(event, context):
    components = load_components()
    update_items(components)
