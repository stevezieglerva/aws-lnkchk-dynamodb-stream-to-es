import json
from datetime import datetime
from ESLambdaLog import *
import logging
import structlog
import sys


def lambda_handler(event, context):
    log = setup_logging()
    log.critical("starting_dynamodb-stream-to-es")
    log.critical("record_count", record_count=len(event["Records"]))
    
    esraw = ESLambdaLog("aws_lnkchk_dynamobd_streams_raw")
    for record in event["Records"]:
        esraw.log_event(record)

    log.critical("finished_dynamodb-stream-to-es")
    return len(event["Records"])


def setup_logging():
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    return structlog.get_logger()
