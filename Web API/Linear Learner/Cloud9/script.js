// This function is designed to collect data from a web form, submit it to a specified API endpoint,
// and display the prediction result on the webpage.

function submitData() {
    // Gather form data into an object where keys are form field IDs and values are their respective inputs.
    const formData = {
        crim: getValueById('crim'),
        zn: getValueById('zn'),
        indus: getValueById('indus'),
        chas: getValueById('chas'),
        nox: getValueById('nox'),
        rm: getValueById('rm'),
        age: getValueById('age'),
        dis: getValueById('dis'),
        rad: getValueById('rad'),
        tax: getValueById('tax'),
        ptratio: getValueById('ptratio'),
        b: getValueById('b'),
        lstat: getValueById('lstat'),
    };

    // Specify the API endpoint URL where the form data will be submitted.
    const apiURL = 'https://nhuihvwng2.execute-api.us-east-1.amazonaws.com/prod/predict';

    // Use the fetch API to send the form data to the specified API endpoint via a POST request.
    fetch(apiURL, {
        method: 'POST', // HTTP method
        headers: {
            'Content-Type': 'application/json', // Set the content type of the request
        },
        body: JSON.stringify({body: JSON.stringify(formData)}), // Convert the form data to JSON format
    })
    .then(response => response.json()) // Parse the JSON response from the API
    .then(data => {
        // Process the API response and extract the prediction score
        const score = JSON.parse(data.prediction).predictions[0].score;
        // Update the HTML element with ID 'predictionResult' to display the prediction result
        document.getElementById('predictionResult').innerText = `Prediction Result: ${score}`;
    })
    .catch((error) => {
        // Handle any errors that occur during the fetch operation
        console.error('Error:', error);
        // Display the error message in the HTML element with ID 'predictionResult'
        document.getElementById('predictionResult').innerText = 'Error: ' + error;
    });
}

// Helper function to get the value of a form element by its ID.
function getValueById(id) {
    return document.getElementById(id).value; // Return the value of the element with the specified ID
}
