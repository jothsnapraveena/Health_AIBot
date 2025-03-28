from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigateway,
    aws_dynamodb as dynamodb,
    aws_iam as iam,
    aws_logs as logs,
    Duration

)
from constructs import Construct
from pathlib import Path

class ChatbotStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # DynamoDB table to store chatbot messages/sessions
        table = dynamodb.Table(
            self, "ChatbotSessionTable",
            partition_key={"name": "session_id", "type": dynamodb.AttributeType.STRING}
        )

        # Lambda function: Bedrock handler
        bedrock_fn = _lambda.Function(
            self, "BedrockHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="bedrock.lambda_handler",
            code=_lambda.Code.from_asset(str(Path(__file__).resolve().parent.parent / "lambda_handlers")),
            environment={"TABLE_NAME": table.table_name},
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        bedrock_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["bedrock:InvokeModel"],
                resources=["*"]
            )
        )

        chat_handler_fn = _lambda.Function(
            self, "ChatHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="chat_handler.lambda_handler",
            code=_lambda.Code.from_asset(str(Path(__file__).resolve().parent.parent / "lambda_handlers")),
            timeout=Duration.seconds(30),
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        chat_handler_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["comprehend:DetectSentiment", "comprehend:DetectPiiEntities", "bedrock:InvokeModel"],
                resources=["*"]
            )
        )




        # Lambda function: Kendra handler
        kendra_fn = _lambda.Function(
            self, "KendraHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="kendra.lambda_handler",
            code=_lambda.Code.from_asset(str(Path(__file__).resolve().parent.parent / "lambda_handlers")),
            environment={},
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        # Lambda function: Pre-validation (Comprehend)
        prevalidate_fn = _lambda.Function(
            self, "PrevalidationHandler",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="prevalidation.lambda_handler",
            code=_lambda.Code.from_asset(str(Path(__file__).resolve().parent.parent / "lambda_handlers")),
            environment={},
            log_retention=logs.RetentionDays.ONE_WEEK,
        )

        prevalidate_fn.add_to_role_policy(
            iam.PolicyStatement(
                actions=["comprehend:DetectSentiment","comprehend:DetectPiiEntities"],
                resources=["*"]
            )
        )


        # REST API Gateway
        api = apigateway.RestApi(self, "ChatbotAPI",
            rest_api_name="Chatbot Service",
            description="Serves chatbot requests."
        )

        chat_resource = api.root.add_resource("chat")

        chat_resource.add_method(
            "POST",
            apigateway.LambdaIntegration(chat_handler_fn)
        )

        chat_resource.add_cors_preflight(
            allow_origins=["http://localhost:5173"],
            allow_methods=["POST"],
            allow_headers=["Content-Type"]
        )



        # Grant DynamoDB access to relevant Lambda
        table.grant_read_write_data(bedrock_fn)
        table.grant_read_write_data(prevalidate_fn)
