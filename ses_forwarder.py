from flask import Flask
from flask import request, jsonify

import sys
import boto3
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = boto3.client('ses', region_name='us-east-1')

config = json.load(file(os.path.join(BASE_DIR, "config.json"),))

FROM_ADDRESS=config['from_address']
TO_ADDRESS=config['to_address']


def send_email(subject, body):
    response = client.send_email(
        Source=FROM_ADDRESS,
        Destination={
            'ToAddresses': [
                TO_ADDRESS,
            ]
        },
        Message={
            'Subject': {'Data': subject},
            'Body': {
                'Text': {'Data': body},
            }
        },
    )


@app.route('/contact', methods=['POST'])
def post_email():
    logger.info("Recieved mail post request")
    result = {}
    print request

    try:
        json = request.get_json()
        subject = "NONE"
        if json is not None:
            subject = json['subject']
            send_email(subject=subject,
                       body=json['body'])

        result['subject'] = subject
        result['status'] = 'success'
    except Exception as e:
        logger.error(e)
        result['error'] = e.message
        result['status'] = 'error'

    return jsonify(**result)


if __name__ == '__main__':
   app.run()
