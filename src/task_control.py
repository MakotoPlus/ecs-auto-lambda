import os
import boto3
import json

from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.data_classes import EventBridgeEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
logger = Logger(level=LOG_LEVEL, service=__name__)


@logger.inject_lambda_context()
def handler(event=EventBridgeEvent, context=LambdaContext) -> None:
    try:
        ecs = boto3.client('ecs')
        logger.info('start')
        logger.info(json.dumps(event))
        action = event['process']
        if action != 'stop' and action !='start':
            raise Exception(f'Invalid argument action=[{action}]')

        cluster_name = event['cluster']
        service_name = event['service']
        desiredCount = event['desiredCount']

        ecs.update_service(
           cluster=cluster_name,
           service=service_name,
           desiredCount=desiredCount
        )
        logger.info('success end')
    except Exception as e:
        raise e

