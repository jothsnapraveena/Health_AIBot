from pathlib import Path
import os

# Define the AI Chatbot project structure you prefer
list_of_files = [
    ".github/workflows/.gitkeep",
    "src/__init__.py",
    "src/infrastructure/__init__.py",
    "src/infrastructure/cdk_app.py",
    "src/infrastructure/stack.py",
    "src/lambda_handlers/__init__.py",
    "src/lambda_handlers/prevalidation.py",
    "src/lambda_handlers/kendra.py",
    "src/lambda_handlers/bedrock.py",
    "src/lambda_handlers/websocket_router.py",
    "src/pipeline/__init__.py",
    "src/pipeline/trigger_pipeline.py",
    "src/utils/__init__.py",
    "src/utils/common.py",
    "src/logger/__init__.py",
    "src/logger/logging.py",
    "src/exception/__init__.py",
    "src/exception/exception.py",
    "frontend/README.md",
    "requirements.txt",
    "setup.py",
    "setup.config",
    "README.md"
]

# Create the directories and files
for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass

