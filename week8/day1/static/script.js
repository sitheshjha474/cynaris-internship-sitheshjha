// ==================================================
// GLOBAL VARIABLES
// ==================================================

let sessionId = null;
let resultChart = null;


// ==================================================
// UPLOAD CSV
// ==================================================

async function uploadCSV() {

    const fileInput = document.getElementById("csvFile");
    const status = document.getElementById("uploadStatus");
    const fileInfo = document.getElementById("fileInfo");

    if (!fileInput.files.length) {

        showStatus(
            status,
            "Please select a CSV file first.",
            false
        );

        return;
    }

    const file = fileInput.files[0];

    const formData = new FormData();

    formData.append("file", file);

    status.style.display = "none";

    try {

        const response = await fetch(
            "/upload",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!data.success) {

            showStatus(
                status,
                data.error || "Upload failed.",
                false
            );

            return;
        }

        sessionId = data.session_id;

        showStatus(
            status,
            "CSV uploaded successfully.",
            true
        );

        fileInfo.classList.remove("hidden");

        fileInfo.innerHTML = `
            <strong>File:</strong> ${data.filename}<br>
            <strong>Rows:</strong> ${data.rows.toLocaleString()}<br>
            <strong>Columns:</strong> ${data.columns.length}<br>
            <strong>Column Names:</strong> ${data.columns.join(", ")}
        `;

        enableButtons();

    } catch (error) {

        showStatus(
            status,
            "Upload error: " + error.message,
            false
        );
    }
}


// ==================================================
// ASK QUESTION
// ==================================================

async function askQuestion() {

    if (!sessionId) {

        alert("Please upload a CSV file first.");

        return;
    }

    const questionInput =
        document.getElementById("question");

    const question =
        questionInput.value.trim();

    if (!question) {

        alert("Please enter a question.");

        return;
    }

    const button =
        document.getElementById("askButton");

    const loading =
        document.getElementById("queryLoading");

    const answerSection =
        document.getElementById("answerSection");

    const answer =
        document.getElementById("answer");

    button.disabled = true;

    loading.style.display = "block";

    answerSection.classList.add("hidden");

    try {

        const formData = new FormData();

        formData.append(
            "session_id",
            sessionId
        );

        formData.append(
            "question",
            question
        );

        const response = await fetch(
            "/cia/sql-analyst",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!data.success) {

            answer.innerText =
                "Error: " +
                (data.error || "Unable to process question.");

            answerSection.classList.remove("hidden");

            hideChart();

            return;
        }

        answer.innerText =
            data.answer;

        answerSection.classList.remove("hidden");

        // Show chart if available
        if (data.chart) {

            renderChart(data.chart);

        } else {

            hideChart();
        }

    } catch (error) {

        answer.innerText =
            "Error: " + error.message;

        answerSection.classList.remove("hidden");

        hideChart();

    } finally {

        button.disabled = false;

        loading.style.display = "none";
    }
}


// ==================================================
// ENTER KEY FOR QUESTION
// ==================================================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        const question =
            document.getElementById("question");

        question.addEventListener(
            "keypress",
            function (event) {

                if (event.key === "Enter") {

                    askQuestion();
                }
            }
        );

        disableButtons();
    }
);


// ==================================================
// RENDER CHART
// ==================================================

function renderChart(chartJson) {

    const chartSection =
        document.getElementById("chartSection");

    const canvas =
        document.getElementById("resultChart");

    if (resultChart) {

        resultChart.destroy();

        resultChart = null;
    }

    const chartData =
        typeof chartJson === "string"
            ? JSON.parse(chartJson)
            : chartJson;

    const labels =
        getChartLabels(chartData);

    const values =
        getChartValues(chartData);

    const title =
        getChartTitle(chartData);

    if (!labels.length || !values.length) {

        hideChart();

        return;
    }

    resultChart =
        new Chart(
            canvas,
            {
                type: "bar",

                data: {
                    labels: labels,

                    datasets: [
                        {
                            label: title,

                            data: values,

                            borderWidth: 1
                        }
                    ]
                },

                options: {
                    responsive: true,

                    maintainAspectRatio: false,

                    plugins: {
                        title: {
                            display: true,
                            text: title
                        },

                        legend: {
                            display: false
                        }
                    },

                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            }
        );

    chartSection.classList.remove("hidden");
}


// ==================================================
// GET CHART LABELS
// ==================================================

function getChartLabels(chartData) {

    if (
        chartData
        && chartData.data
        && chartData.data.length > 0
    ) {

        const firstTrace =
            chartData.data[0];

        if (firstTrace.x) {

            return firstTrace.x;
        }
    }

    return [];
}


// ==================================================
// GET CHART VALUES
// ==================================================

function getChartValues(chartData) {

    if (
        chartData
        && chartData.data
        && chartData.data.length > 0
    ) {

        const firstTrace =
            chartData.data[0];

        if (firstTrace.y) {

            return firstTrace.y;
        }
    }

    return [];
}


// ==================================================
// GET CHART TITLE
// ==================================================

function getChartTitle(chartData) {

    if (
        chartData
        && chartData.layout
        && chartData.layout.title
    ) {

        if (
            typeof chartData.layout.title === "string"
        ) {

            return chartData.layout.title;
        }

        if (
            chartData.layout.title.text
        ) {

            return chartData.layout.title.text;
        }
    }

    return "Data Analysis Chart";
}


// ==================================================
// HIDE CHART
// ==================================================

function hideChart() {

    const chartSection =
        document.getElementById("chartSection");

    chartSection.classList.add("hidden");

    if (resultChart) {

        resultChart.destroy();

        resultChart = null;
    }
}


// ==================================================
// GENERATE AI SUMMARY
// ==================================================

async function generateSummary() {

    if (!sessionId) {

        alert("Please upload a CSV file first.");

        return;
    }

    const button =
        document.getElementById("summaryButton");

    const loading =
        document.getElementById("summaryLoading");

    const insightsSection =
        document.getElementById("insightsSection");

    const summarySection =
        document.getElementById("summarySection");

    const insightsDiv =
        document.getElementById("insights");

    const summaryDiv =
        document.getElementById("summary");

    button.disabled = true;

    loading.style.display = "block";

    insightsSection.classList.add("hidden");

    summarySection.classList.add("hidden");

    try {

        const formData = new FormData();

        formData.append(
            "session_id",
            sessionId
        );

        const response = await fetch(
            "/ai-summary",
            {
                method: "POST",
                body: formData
            }
        );

        const data = await response.json();

        if (!data.success) {

            alert(
                data.error ||
                "Unable to generate AI summary."
            );

            return;
        }

        // ------------------------------------------
        // DISPLAY FIVE INSIGHTS
        // ------------------------------------------

        insightsDiv.innerHTML = "";

        data.insights.forEach(
            function (insight, index) {

                const div =
                    document.createElement("div");

                div.className = "insight";

                div.innerHTML =
                    `<strong>Insight ${index + 1}:</strong> ${escapeHTML(insight)}`;

                insightsDiv.appendChild(div);
            }
        );

        insightsSection.classList.remove("hidden");


        // ------------------------------------------
        // DISPLAY SUMMARY
        // ------------------------------------------

        summaryDiv.innerText =
            data.summary;

        summarySection.classList.remove("hidden");

    } catch (error) {

        alert(
            "Summary error: " +
            error.message
        );

    } finally {

        button.disabled = false;

        loading.style.display = "none";
    }
}


// ==================================================
// DOWNLOAD POWERPOINT
// ==================================================

async function downloadPPT() {

    if (!sessionId) {

        alert("Please upload a CSV file first.");

        return;
    }

    const button =
        document.getElementById("pptButton");

    const loading =
        document.getElementById("pptLoading");

    button.disabled = true;

    loading.style.display = "block";

    try {

        const formData = new FormData();

        formData.append(
            "session_id",
            sessionId
        );

        const response = await fetch(
            "/download-ppt",
            {
                method: "POST",
                body: formData
            }
        );

        if (!response.ok) {

            let errorMessage =
                "Unable to create PowerPoint.";

            try {

                const errorData =
                    await response.json();

                errorMessage =
                    errorData.error ||
                    errorMessage;

            } catch (e) {}

            alert(errorMessage);

            return;
        }

        const blob =
            await response.blob();

        const url =
            window.URL.createObjectURL(blob);

        const link =
            document.createElement("a");

        link.href = url;

        link.download =
            "CIA_Executive_Report.pptx";

        document.body.appendChild(link);

        link.click();

        link.remove();

        window.URL.revokeObjectURL(url);

    } catch (error) {

        alert(
            "PPT download error: " +
            error.message
        );

    } finally {

        button.disabled = false;

        loading.style.display = "none";
    }
}


// ==================================================
// ENABLE BUTTONS
// ==================================================

function enableButtons() {

    document.getElementById(
        "askButton"
    ).disabled = false;

    document.getElementById(
        "summaryButton"
    ).disabled = false;

    document.getElementById(
        "pptButton"
    ).disabled = false;
}


// ==================================================
// DISABLE BUTTONS
// ==================================================

function disableButtons() {

    document.getElementById(
        "askButton"
    ).disabled = true;

    document.getElementById(
        "summaryButton"
    ).disabled = true;

    document.getElementById(
        "pptButton"
    ).disabled = true;
}


// ==================================================
// STATUS MESSAGE
// ==================================================

function showStatus(
    element,
    message,
    success
) {

    element.innerText = message;

    element.className =
        "status " +
        (
            success
                ? "success-message"
                : "error-message"
        );

    element.style.display = "block";
}


// ==================================================
// ESCAPE HTML
// ==================================================

function escapeHTML(value) {

    const div =
        document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}