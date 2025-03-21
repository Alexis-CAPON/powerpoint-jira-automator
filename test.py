import base64
import os
import json

def convert_ppt_to_base64(ppt_path):
    """
    Converts a PowerPoint (PPTX) file into a Base64-encoded string.

    :param ppt_path: Path to the PPTX file.
    :return: Base64-encoded string of the PPTX file.
    """
    with open(ppt_path, "rb") as ppt_file:
        encoded_string = base64.b64encode(ppt_file.read()).decode("utf-8")
    return encoded_string

ppt_path = "/Users/alexis/Dev/scripts/jiraUpdater/VISA_template_jira_autoupdater.pptx"  # Replace with your PPTX file path
base64_string = convert_ppt_to_base64(ppt_path)

# Convert the body dict to a JSON string
body_content = json.dumps({
    "epic_key": "FDSO-63542",
    "pptBase64": base64_string
})

event = {
    "body": body_content,
    "resource": "/updatejira",
    "path": "/prod/updatejira",
    "httpMethod": "PUT",
    "isBase64Encoded": False,
    "headers": {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "en-US,en;q=0.8",
        "Cache-Control": "max-age=0",
        "CloudFront-Forwarded-Proto": "https",
        "CloudFront-Is-Desktop-Viewer": "true",
        "CloudFront-Is-Mobile-Viewer": "false",
        "CloudFront-Is-SmartTV-Viewer": "false",
        "CloudFront-Is-Tablet-Viewer": "false",
        "CloudFront-Viewer-Country": "US",
        "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Custom User Agent String",
        "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "cDehVQoZnx43VYQb9j2-nvCh-9z396Uhbp027Y2JvkCPNLmGJHqlaA==",
        "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
        "X-Forwarded-Port": "443",
        "X-Forwarded-Proto": "https"
    },
    "requestContext": {
        "stage": "prod",
        "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
        "requestTime": "09/Apr/2015:12:34:56 +0000",
        "requestTimeEpoch": 1428582896000,
        "path": "/prod/updatejira",
        "resourcePath": "/updatejira",
        "httpMethod": "POST",
        "apiId": "1234567890",
        "protocol": "HTTP/1.1"
    }
}

json_file = os.path.join("/Users/alexis/Dev/scripts/jiraUpdater/jira-updater/events", "event.json")

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(event, f, indent=4, ensure_ascii=False)
