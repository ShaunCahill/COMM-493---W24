# This AWS Lambda function interfaces with Amazon SageMaker to make predictions based on input data. 
# It receives a JSON payload via an API Gateway, parses it, sends the data to a SageMaker endpoint, 
# and returns the prediction result. It's designed to work with a linear regression model hosted on SageMaker.

import json  # Import the json library for parsing JSON data.
import boto3  # Import the boto3 library to interact with AWS services, including SageMaker.

# Initialize the SageMaker runtime client to interact with SageMaker services.
sagemaker_runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    # The entry point for the Lambda function. Processes incoming events and context.
    try:
        # Attempt to parse the JSON payload from the event object.
        body = json.loads(event['body'])
    except json.JSONDecodeError:
        # If JSON parsing fails, return an error response.
        return error_response(400, 'Invalid JSON format')
    
    # Extract features from the parsed JSON payload, providing default values if not found.
    crim = body.get('crim', '0')
    zn = body.get('zn', '0')
    indus = body.get('indus', '0')
    chas = body.get('chas', '0')
    nox = body.get('nox', '0')
    rm = body.get('rm', '0')
    age = body.get('age', '0')
    dis = body.get('dis', '0')
    rad = body.get('rad', '0')
    tax = body.get('tax', '0')
    ptratio = body.get('ptratio', '0')
    b = body.get('b', '0')
    lstat = body.get('lstat', '0')
    
    # Prepare the input data as a CSV string payload for SageMaker.
    payload = ','.join(map(str, [crim, zn, indus, chas, nox, rm, age, dis, rad, tax, ptratio, b, lstat]))
    
    # Specify the name of the SageMaker endpoint to which we want to send the data.
    endpoint_name = "regression-linear-learner-endpoint"
    
    try:
        # Invoke the SageMaker endpoint with the payload, specifying the content type.
        response = sagemaker_runtime.invoke_endpoint(EndpointName=endpoint_name, ContentType='text/csv', Body=payload)
        
        # Decode the prediction result from the response body.
        result = response['Body'].read().decode('utf-8')
        # Return a successful response with the prediction result.
        return success_response({'prediction': result})
    
    except Exception as e:
        # Log and return an error response if any exception occurs during the process.
        print(e)
        return error_response(500, 'Error processing your request')

def success_response(body):
    # Helper function to construct a success HTTP response.
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allow any domain to access this API.
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'  # Allowed HTTP methods.
        },
        'body': json.dumps(body)  # Serialize the response body to JSON.
    }

def error_response(status_code, error_message):
    # Helper function to construct an error HTTP response.
    return {
        'statusCode': status_code,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'OPTIONS,POST'
        },
        'body': json.dumps({'error': error_message})  # Serialize the error message to JSON.
    }
