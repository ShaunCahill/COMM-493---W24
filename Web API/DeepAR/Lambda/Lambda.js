import json
import boto3
import os

def lambda_handler(event, context):
    # Define the endpoint name (set as an environment variable)
    endpoint_name = 'online-retail-endpoint-cat'

    # Check if the event has a 'body' key (API Gateway event)
    if 'body' in event:
        body = json.loads(event['body'])
    else:
        body = event  # Direct invocation

    # Extract the country code, sales data, and start date from the input
    country_code = body['country_code']
    sales_data = body['sales_data']
    start_date = body['start_date']  # Extract the start date from the input

    # Prepare the input data for prediction
    prediction_input = {
        "instances": [{"start": start_date, "target": sales_data, "cat": [country_code]}],
        "configuration": {"num_samples": 100, "output_types": ["mean", "quantiles"], "quantiles": ["0.1", "0.9"]}
    }

    # Invoke the endpoint for prediction
    sagemaker_runtime = boto3.client('sagemaker-runtime')
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType='application/json',
        Body=json.dumps(prediction_input)
    )

    # Parse the prediction response
    predictions = json.loads(response['Body'].read().decode())
    predicted_means = predictions['predictions'][0]['mean']
    predicted_quantiles = predictions['predictions'][0]['quantiles']

# Create a response object with the predicted sales
    result = {
        'predicted_means': predicted_means,
        'predicted_lower_quantile': predicted_quantiles['0.1'],
        'predicted_upper_quantile': predicted_quantiles['0.9']
    }

    # Return the response object with CORS headers
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Allows requests from any origin
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Allow-Methods': 'POST'
        },
        'body': json.dumps(result)
    }