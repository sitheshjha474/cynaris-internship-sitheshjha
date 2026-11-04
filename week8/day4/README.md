# CIA CSV Analyst

A web-based CSV analysis application that lets users upload datasets, ask questions about their data, and view answers and charts through a browser interface.

## Features

- Upload CSV files through the web interface.
- Load uploaded data into a Pandas DataFrame for analysis.
- Ask natural-language questions about the uploaded dataset.
- Display analysis results in the frontend.
- Visualize data using Chart.js.
- Generate chart data using Plotly-compatible structures.
- Handle file-upload and query errors with user-friendly messages.

## Tech Stack

- **Backend:** Python, FastAPI
- **Data Analysis:** Pandas
- **AI Analysis:** PandasAI with a supported LLM configuration
- **Chart Data:** Plotly-compatible JSON
- **Frontend:** HTML, CSS, JavaScript
- **Visualization:** Chart.js
- **Deployment:** Render
- **Version Control:** Git and GitHub

## Project Structure

```text
week7_day3/
├── app.py
├── requirements.txt
├── render.yaml
├── README.md
└── static/
    ├── index.html
    └── script.js
```

## Local Setup

1. Clone the repository:

   ```bash
   git clone YOUR_GITHUB_REPOSITORY_URL
   cd week7_day3
   ```

2. Create and activate a virtual environment.

   Windows PowerShell:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure any required LLM credentials using environment variables. Never commit API keys or secrets to GitHub.

5. Start the application:

   ```bash
   uvicorn app:app --reload
   ```

6. Open http://127.0.0.1:8000 in your browser.

## Deployment

- **Platform:** Render
- **Live URL:** ADD_YOUR_RENDER_URL_HERE
- **Repository:** ADD_YOUR_GITHUB_REPOSITORY_URL_HERE

## Testing

Test the application with a valid CSV file and questions such as:

1. How many rows and columns are in this dataset?
2. What are the column names?
3. What is the total sales value?
4. Which category has the highest sales?
5. Show a chart of sales by category.

Verify file-upload errors, invalid questions, chart rendering, and server logs.

## Known Limitations

- Results depend on the quality and structure of the uploaded CSV.
- AI-powered analysis requires a compatible LLM configuration and may depend on external service availability.
- Large files may require additional memory and processing time.
- Uploaded data may be temporary and session-specific rather than permanently stored.
- Supported chart types and question complexity depend on the current implementation.
- The deployment should not be used for sensitive data unless appropriate security and privacy controls are in place.

## Future Improvements

- Add user authentication and stronger upload validation.
- Improve support for large datasets.
- Add more chart types and downloadable reports.
- Add automated backend and frontend tests