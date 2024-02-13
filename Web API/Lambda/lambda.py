"""
This AWS Lambda function interfaces with an Amazon SageMaker endpoint to make predictions based on input data.
The function:
1. Receives a JSON payload from an API Gateway event.
2. Parses the payload to extract model input features.
3. Constructs a payload in the format expected by the SageMaker model.
4. Invokes the SageMaker endpoint with the constructed payload.
5. Receives the prediction result from SageMaker.
6. Returns the prediction result in the response.

The function is designed to work with a linear regression model hosted on SageMaker. It expects numeric input features
and sends them as a CSV string to the SageMaker endpoint. The response from SageMaker is expected to be a prediction result,
which is returned to the caller in JSON format.
"""

import json
import boto3
import logging

# Initialize logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize the SageMaker runtime client
sagemaker_runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    # Log the received event to help with debugging
    logger.info(f"Received event: {event}")
    
    try:
        # Parse the JSON payload from the event object. This is the data received from the API Gateway.
        event_body = json.loads(event['body'])
        # The 'body' field is a stringified JSON. Parse it again to get the actual JSON object with the input data.
        body = json.loads(event_body['body'])
        logger.info(f"Double-parsed body: {body}")  # Log the correctly parsed body for further debugging.
    except json.JSONDecodeError:
        # Log and return an error response if there's an issue with JSON parsing.
        logger.error('Invalid JSON format')
        return error_response(400, 'Invalid JSON format')
    
    # Extract each feature from the parsed JSON object, converting all values to floats.
    # This ensures compatibility with the SageMaker model which expects numeric inputs.
    crim = float(body.get('crim', 0))
    zn = float(body.get('zn', 0))
    indus = float(body.get('indus', 0))
    chas = float(body.get('chas', 0))  # Even though 'chas' might be expected as int, converted to float for consistency
    nox = float(body.get('nox', 0))
    rm = float(body.get('rm', 0))
    age = float(body.get('age', 0))
    dis = float(body.get('dis', 0))
    rad = float(body.get('rad', 0))
    tax = float(body.get('tax', 0))
    ptratio = float(body.get('ptratio', 0))
    b = float(body.get('b', 0))
    lstat = float(body.get('lstat', 0))

    # Log extracted values to verify correct parsing and conversion
    logger.info(f"Extracted values: crim={crim}, zn={zn}, indus={indus}, chas={chas}, nox={nox}, rm={rm}, age={age}, dis={dis}, rad={rad}, tax={tax}, ptratio={ptratio}, b={b}, lstat={lstat}")

    # Prepare the CSV string payload for SageMaker, joining all features by commas.
    features = [crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat]
    payload = ','.join(map(str, features))
    logger.info(f"Payload to SageMaker: {payload}")  # Log the payload being sent to SageMaker for final verification.
    
    # Specify your SageMaker endpoint name here
    endpoint_name = "regression-linear-learner-endpoint"
    
    try:
        # Invoke the SageMaker endpoint with the constructed payload
        response = sagemaker_runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='text/csv', Body=payload)
        # Decode the prediction result from SageMaker
        result = response['Body'].read().decode('utf-8')
        logger.info(f"Received prediction: {result}")  # Log the prediction result received from SageMaker
        
        # Return a successful response with the prediction result
        return success_response({'prediction': result})
    except Exception as e:
        # Log and return an error response if there's an issue invoking the SageMaker endpoint or processing the request
        logger.error("Error processing your request", exc_info=True)
        return error_response(500, 'Error processing your request')

def success_response(body):
    # Construct a success HTTP response with CORS headers
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allow any domain to access this API
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps(body)  # Serialize the response body to JSON
    }

def error_response(status_code, error_message):
    # Construct an error HTTP response with CORS headers
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'error': error_message})  # Serialize the error message to JSON
    }
