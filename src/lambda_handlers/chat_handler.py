import boto3
import json

# Initialize clients
comprehend = boto3.client("comprehend")
bedrock = boto3.client("bedrock-runtime")

MODEL_ID = "anthropic.claude-instant-v1"

def cors_response(status_code, body_dict):
    """
    Return the CORS enabled response
    """
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Allow all origins or use a specific origin like "http://localhost:5173"
            "Access-Control-Allow-Headers": "*",  # Allow all headers
            "Access-Control-Allow-Methods": "OPTIONS,POST"  # Allow preflight OPTIONS and POST requests
        },
        "body": json.dumps(body_dict)
    }

def redact_pii(text):
    """
    Redact PII using Amazon Comprehend
    """
    try:
        print("🔍 Detecting PII...")
        response = comprehend.detect_pii_entities(Text=text, LanguageCode="en")
        entities = response.get("Entities", [])

        redacted_text = text
        for entity in sorted(entities, key=lambda e: e["BeginOffset"], reverse=True):
            start, end = entity["BeginOffset"], entity["EndOffset"]
            redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]

        print("✅ Redacted Text:", redacted_text)
        return redacted_text, entities
    except Exception as pii_err:
        print("❌ Error in redact_pii:", pii_err)
        raise pii_err

def lambda_handler(event, context):
    try:
        print("🔹 Incoming Event:", event)
        body = json.loads(event.get("body", "{}"))
        user_input = body.get("message", "")

        if not user_input:
            return cors_response(400, {"error": "Missing 'message'"})

        print("✉️ User Input:", user_input)

        # Step 1: Redact PII
        redacted_input, pii_entities = redact_pii(user_input)

        # Step 2: Sentiment analysis
        print("🧠 Detecting Sentiment...")
        sentiment_result = comprehend.detect_sentiment(
            Text=redacted_input,
            LanguageCode="en"
        )
        sentiment = sentiment_result.get("Sentiment", "NEUTRAL")
        score = sentiment_result.get("SentimentScore", {})
        print("📊 Sentiment:", sentiment, score)

        if sentiment == "NEGATIVE" and score.get("Negative", 0) > 0.9:
            return cors_response(403, {
                "validated": False,
                "reason": "Message too negative",
                "sentiment": sentiment,
                "score": score
            })

        # Step 3: Add a system message to inform the AI's purpose
        system_message = (
            "You are an AI-powered assistant who helps people with medical procedures, "
            "insurance queries, and paperwork related to healthcare. You provide helpful, accurate, and "
            "friendly responses to assist users in understanding their healthcare rights and navigating the system. "
            "You should ensure that you maintain privacy and security, particularly when dealing with personally identifying information (PII)."
        )

        # Step 4: Construct the user prompt with system message context
        prompt = (
            f"{system_message}\n\n"
            f"Human: {user_input}\n\nAssistant:"
        )

        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps({
                "prompt": prompt,
                "max_tokens_to_sample": 200,
                "temperature": 0.7
            }),
            contentType="application/json",
            accept="application/json"
        )

        print("✅ Bedrock Response Received")
        response_body = json.loads(response["body"].read())
        ai_reply = response_body.get("completion", "")
        print("💬 AI Reply:", ai_reply)

        return cors_response(200, {
            "validated": True,
            "sentiment": sentiment,
            "score": score,
            "redacted_input": redacted_input,
            "pii_entities": pii_entities,
            "response": ai_reply.strip()
        })

    except Exception as e:
        print("🔥 Exception in Lambda:", str(e))
        return cors_response(500, {"error": str(e)})
