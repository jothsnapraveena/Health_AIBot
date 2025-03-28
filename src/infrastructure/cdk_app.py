

import sys
import os
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))  # Add src/ to path

import aws_cdk as cdk
from infrastructure.stack import ChatbotStack

app = cdk.App()

ChatbotStack(app, "ChatbotStack", env=cdk.Environment(
    account=os.getenv("CDK_DEFAULT_ACCOUNT"),
    region=os.getenv("CDK_DEFAULT_REGION"),
))

app.synth()

