document.getElementById("predictionForm").onsubmit = function(event) {
    event.preventDefault();

    var countryCode = document.getElementById("countryCode").value;
    var salesData = document.getElementById("salesData").value.split(',').map(Number);
    var startDate = document.getElementById("startDate").value;

    var payload = {
        country_code: parseInt(countryCode),
        sales_data: salesData,
        start_date: startDate
    };

    fetch("https://m3ge077ly9.execute-api.us-east-1.amazonaws.com/prod/predictions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        if (!response.ok) {
            return response.text().then(text => {
                throw new Error(`Network response was not ok: ${response.status} ${response.statusText}\nResponse Body: ${text}`);
            });
        }
        return response.json();
    })
    .then(data => {
        // Display the predicted sales
        document.getElementById("result").innerHTML = "Predicted Sales: " + JSON.stringify(data);

        // Create a chart with the predicted sales data
        var ctx = document.getElementById('myChart').getContext('2d');
        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length: data.predicted_means.length}, (_, i) => i + 1),
                datasets: [{
                    label: 'Predicted Sales',
                    data: data.predicted_means,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `Error: ${error.message}`;
    });
};
