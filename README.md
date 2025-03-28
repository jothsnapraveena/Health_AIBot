# Virtual Healthcare Assistant Chatbot

This project is an AI-powered chatbot designed to assist users with medical system-related queries, such as insurance, paperwork, and healthcare procedures. It uses AWS Lambda, Amazon Bedrock (Claude Model), Amazon Comprehend, and API Gateway. The bot redacts personally identifiable information (PII) and provides helpful responses to healthcare-related inquiries.

## Table of Contents

- [Overview](#overview)
- [Technologies Used](#technologies-used)
- [Architecture](#architecture)
- [Setup](#setup)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Overview

This chatbot interacts with users to provide information about healthcare procedures, insurance eligibility, and related topics. It offers:
- **Sentiment Analysis** using Amazon Comprehend to assess the tone of user input.
- **PII Redaction** to ensure privacy.
- **Bedrock Model Integration** to provide intelligent responses based on user queries.

The chatbot can handle queries like:
- "Am I eligible for MassHealth insurance?"
- "How can I get my prescription filled?"

## Technologies Used

- **AWS Lambda**: For serverless functions to handle chat interactions.
- **Amazon Bedrock**: To power the chatbot's responses using the Claude AI model.
- **Amazon Comprehend**: To perform sentiment analysis and PII redaction.
- **API Gateway**: To expose the chatbot's backend as a REST API.
- **DynamoDB**: For storing chatbot sessions and messages.
- **AWS IAM**: For handling permissions.

## Architecture

![Architecture](./assets/architecture-diagram.png)

- **API Gateway**: Receives requests from the frontend and triggers the Lambda functions.
- **Lambda Functions**: Handle different tasks (e.g., sentiment analysis, PII redaction, model interaction).
- **Bedrock**: Executes the Claude AI model to generate intelligent responses.
- **Comprehend**: Used for sentiment analysis and detecting personally identifiable information.
- **DynamoDB**: Stores the user sessions and messages.

## Setup

1. **Clone the repository**:
    ```bash
    git clone https://github.com/your-username/virtual-healthcare-assistant.git
    cd virtual-healthcare-assistant
    ```

2. **Set up AWS CLI**:
    - Install the AWS CLI from the [official documentation](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html).
    - Configure the CLI with your AWS credentials:
    ```bash
    aws configure
    ```

3. **Deploy the infrastructure**:
    - Install the AWS CDK if you haven't already:
    ```bash
    npm install -g aws-cdk
    ```
    - Bootstrap the AWS environment:
    ```bash
    cdk bootstrap
    ```
    - Deploy the stack:
    ```bash
    cdk deploy
    ```

4. **Start the React frontend**:
    ```bash
    cd frontend-react
    npm start
    ```

    The frontend should now be available at `http://localhost:5173`.

## Usage

- Open the React app at `http://localhost:5173`.
- Type your queries related to healthcare or insurance in the chat interface.
- The bot will respond with helpful information, such as insurance eligibility, MassHealth-related details, or healthcare procedures.

### Example Interaction:
- **User**: "Am I eligible for MassHealth?"
- **Bot**: "To be eligible for MassHealth, you must meet certain income and residency requirements. You can apply online or contact MassHealth directly."

## API Endpoints

- **POST /chat**: The main endpoint for chatting with the bot.
    - **Request Body**:
      ```json
      {
        "message": "Your query here"
      }
      ```
    - **Response**:
      ```json
      {
        "validated": true,
        "sentiment": "NEUTRAL",
        "score": {
          "Positive": 0.01,
          "Negative": 0.02,
          "Neutral": 0.97
        },
        "response": "Bot's answer"
      }
      ```
![Bot]('Screenshot 2025-03-28 014517.png')

