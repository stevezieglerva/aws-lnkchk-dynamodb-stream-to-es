import json
from datetime import datetime
from ESLambdaLog import *

def lambda_handler(event, context):
    print("In lambda_handler " + str(datetime.now()))
    
    esraw = ESLambdaLog("aws_lnkchk_cache_stream_raw")
    es = ESLambdaLog("aws_lnkchk_cache_stream")

    print("Logging to ES")
    for record in event["Records"]:
        esraw.log_event(record)
        event_name = record["eventName"]
        url = record["dynamodb"]["Keys"]["url"]["S"]
        image = "NewImage"
        if event_name == "REMOVE":
            image = "OldImage"
        http_response = record["dynamodb"][image]["http_result"]["S"]
        print("\t" + event_name + " " + url)
        link_check = "good"
        if int(http_response) >= 400:
            link_check = "bad"
        es_event = {"event" : event_name, "url" : url, "http_response" : http_response, "link_check" : link_check}
        es.log_event(es_event)
        print(link_check + " - " + url)

    print("Finished.")
 