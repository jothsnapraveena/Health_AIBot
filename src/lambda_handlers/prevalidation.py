import boto3
import json

comprehend = boto3.client("comprehend")

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        user_input = body.get("message", "")

        if not user_input:
            return {"statusCode": 400, "body": "Missing 'message' in request"}

        # Step 1: Analyze sentiment
        sentiment_result = comprehend.detect_sentiment(
            Text=user_input,
            LanguageCode="en"
        )

        sentiment = sentiment_result.get("Sentiment", "NEUTRAL")
        sentiment_score = sentiment_result.get("SentimentScore", {})

        # Step 2: Apply custom logic — block extreme negativity
        if sentiment == "NEGATIVE" and sentiment_score.get("Negative", 0) > 0.9:
            return {
                "statusCode": 403,
                "body": json.dumps({
                    "validated": False,
                    "reason": "Content too negative",
                    "sentiment": sentiment,
                    "score": sentiment_score
                })
            }

        # Step 3: Validated successfully
        return {
            "statusCode": 200,
            "body": json.dumps({
                "validated": True,
                "sentiment": sentiment,
                "score": sentiment_score
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }
