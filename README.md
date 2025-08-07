# GCC Quick Process

A Streamlit application for processing Google Career Certificates (GCC) usage reports with specific filtering capabilities for AI Essentials certificates.

## Features

### AI Essentials Certificate Filtering
The application automatically filters and counts AI Essentials certificates based on the following criteria:
- **Course**: "Google AI Essentials"
- **Enrollment Time**: >= January 01, 2025
- **Completed**: "Yes"

### Output Format
The application displays: `Total {num} AI Essentials certificate(s)`

## Usage

### Running the Application

1. **Setup Environment** (using uv as per project requirements):
   ```bash
   cd /Users/sonnt/gcc-quick-process
   uv venv .venv && source .venv/bin/activate
   uv pip install streamlit pandas
   ```

2. **Run Streamlit App**:
   ```bash
   uv run streamlit run main.py
   ```

3. **Upload CSV File**:
   - Select "Process GCC Usage Report" from the sidebar
   - Upload your CSV file with usage report data
   - View the filtered results and download processed data

### Testing

Run the test script to verify functionality with sample data:
```bash
uv run python test_sample.py
```

## CSV File Format

Expected columns in the usage report CSV:
- `Name` - Student name
- `Email` - Student email
- `Course` - Course name (filter target: "Google AI Essentials")
- `Enrollment Time` - ISO format timestamp (filter: >= 2025-01-01)
- `Completed` - Completion status (filter target: "Yes")
- `Completion Time` - Completion timestamp
- Other columns as per standard GCC usage report format

## Sample Data

The application has been tested with sample data including:
- Regular courses (non-AI Essentials)
- AI Essentials courses with various enrollment dates
- Both completed and incomplete certificates

## Technical Details

- Built with Streamlit for web interface
- Uses pandas for data processing
- Handles timezone-aware datetime comparisons
- Supports UTF-8 CSV files with comma separation
- Provides data preview, filtering results, and download capabilities