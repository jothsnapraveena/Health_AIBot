import boto3
import json
import os

# Set up Bedrock runtime client
bedrock = boto3.client("bedrock-runtime")

# Choose Claude model from Anthropic (can be changed to other providers)
MODEL_ID = "anthropic.claude-instant-v1"
REGION = "us-east-1"

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        body = json.loads(event.get("body", "{}"))
        user_input = body.get("message", "")

        if not user_input:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'message'"})
            }

        prompt = f"\n\nHuman: {user_input}\n\nAssistant:"

        # Prepare request to Bedrock
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 200,
                "temperature": 0.7,
                "top_k": 250,
                "top_p": 0.9,
                "stop_sequences": ["\n\nHuman:"]
            }),
            contentType="application/json",
            accept="application/json"
        )

        # Parse Bedrock response
        response_body = json.loads(response["body"].read())
        ai_message = response_body.get("completion", "")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "response": ai_message.strip()
            })
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
