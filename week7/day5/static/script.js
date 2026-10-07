let sessionId = null;
let currentChart = null;

// -----------------------------
// UPLOAD CSV
// -----------------------------
async function uploadCSV() {
    const fileInput = document.getElementById("csvFile");
    const status = document.getElementById("status");

    if (!fileInput || !fileInput.files || !fileInput.files.length) {
        status.innerText = "Please select a CSV file.";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append("file", file);

    status.innerText = "Uploading...";

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            sessionId = data.session_id;
            status.innerText = `Uploaded: ${data.filename} | Rows: ${data.rows}`;
        } else {
            status.innerText = "Error: " + data.error;
        }
    } catch (error) {
        status.innerText = "Upload failed: " + error;
    }
}

// -----------------------------
// ASK CIA
// -----------------------------
async function askCIA() {
    const question = document.getElementById("question").value;
    const answer = document.getElementById("answer");

    if (!sessionId) {
        answer.innerText = "Please upload a CSV first.";
        return;
    }

    if (!question.trim()) {
        answer.innerText = "Please enter a question.";
        return;
    }

    answer.innerText = "Analyzing with PandasAI...";

    const formData = new FormData();
    formData.append("session_id", sessionId);
    formData.append("question", question);

    try {
        const response = await fetch("/cia/sql-analyst", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!data.success) {
            answer.innerText = "Error: " + data.error;
            return;
        }

        answer.innerText = data.answer;

        if (data.chart) {
            renderChart(data.chart);
        }
    } catch (error) {
        answer.innerText = "Request failed: " + error;
    }
}

// -----------------------------
// RENDER CHART.JS
// -----------------------------
function renderChart(plotlyJSON) {
    if (!plotlyJSON) {
        return;
    }

    let chartData;

    try {
        chartData = JSON.parse(plotlyJSON);
    } catch (error) {
        console.error("Invalid chart JSON", error);
        return;
    }

    const canvas = document.getElementById("myChart");
    if (!canvas) {
        return;
    }

    if (currentChart) {
        currentChart.destroy();
    }

    const trace = chartData?.data?.[0];
    if (!trace) {
        return;
    }

    const labels = trace.x || [];
    const values = trace.y || [];

    currentChart = new Chart(canvas, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: trace.name || "Data",
                data: values
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: chartData.layout?.title?.text || "Chart"
                }
            }
        }
    });
}

