# Technical Documentation

## Architecture

User
  |
  v
Streamlit Interface
  |
  v
CSV Upload
  |
  v
Pandas DataFrame
  |
  +----> Data Profiling
  |
  +----> Data Quality Checks
  |
  +----> Plotly Visualizations
  |
  +----> Question Analysis Engine
  |          |
  |          +----> Pandas Calculations
  |          |
  |          +----> Optional Ollama
  |
  +----> Automated Insights
  |
  v
CSV Export

## Main Components

### Streamlit Interface
Provides the browser-based user interface, file uploader, charts, metrics, and question input.

### Pandas
Loads CSV files and performs statistical calculations, grouping, missing-value checks, and duplicate detection.

### NumPy
Supports numeric-column identification and numerical analysis.

### Plotly
Creates interactive visualizations.

### Question Analysis Engine
Interprets common question patterns and performs deterministic calculations using Pandas.

### Ollama Integration
Optionally sends a dataset sample and user question to a locally running Ollama model.

## Data Flow
1. User uploads a CSV file.
2. The application reads the file into a DataFrame.
3. Dataset statistics and data-quality information are calculated.
4. The user selects visualizations or enters a question.
5. The application generates charts or analytical responses.
6. The user can download the dataset.

## Error Handling
The application handles CSV reading errors and optional Ollama connection failures. If Ollama is unavailable, the built-in analysis engine is used as a fallback.

## Security Considerations
- Run the prototype locally.
- Do not upload confidential or personally identifiable information without appropriate safeguards.
- Do not expose the local Ollama service or application publicly without security controls.
- Validate uploaded files and analytical outputs before production use.