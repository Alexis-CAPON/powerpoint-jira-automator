# main.py

import json
import os
import base64

# Import your helper modules
from ppt_extractor import process_pptx
from jira_updater import update_jira_from_extracted_data
from openai_call import openAICall


def lambda_handler(event, context):
    try:

        if "body" in event:
            try:
                body = json.loads(event["body"])
            except json.JSONDecodeError:
                return {
                    "statusCode": 400,
                    "body": json.dumps({"error": "Invalid JSON in body"})
                }
        else:
            body = event

        # Check if 'pptBase64' is provided
        if "pptBase64" not in body:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'pptBase64' in event"})
            }
        # 1) Retrieve the PPT base64 from the event
        ppt_base64 = body.get("pptBase64")
        epic_key = body.get("epic_key")
        
        output_folder = "/tmp/output"
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        # 2) Extract from PPT -> JSON and save png file to be show in JIRA
        extracted_data = process_pptx(ppt_base64)

        # Assume openAICall is defined elsewhere and returns the raw output string.
        raw_output = openAICall(extracted_data)

        # Split into lines and remove markdown code fences if present.
        lines = raw_output.strip().splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        clean_output = "\n".join(lines)

        try:
            transformed_data = json.loads(clean_output)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
            transformed_data = []

        # Ensure the transformed_data is a list.
        if not isinstance(transformed_data, list):
            transformed_data = [transformed_data]


        # 3) Gather Jira environment variables
        jira_base_url = os.environ.get('JIRA_BASE_URL')
        jira_token = os.environ.get('JIRA_TOKEN')

        
        # 4) Update Jira
        result = update_jira_from_extracted_data(transformed_data, epic_key, jira_base_url, jira_token)

        # 5) Return success
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Jira updated successfully",
                "details": result
            })
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }