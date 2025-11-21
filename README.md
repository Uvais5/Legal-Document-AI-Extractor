# Legal Document AI Extractor

An AI-powered agent that extracts structured data from complex legal documents (PDFs) using Google's Gemini API. Built with Streamlit and Pydantic.

## 🚀 Features

- **PDF Text Extraction**: Upload any legal PDF document.
- **AI Analysis**: Uses **Google Gemini Flash** to analyze the text.
- **Structured Data**: Extracts key information into strict JSON format:
    - Definitions
    - Legislative Sections
    - Eligibility Criteria
    - Payment Entitlements
    - Record Keeping Requirements
- **Executive Summary**: Generates a 5-10 bullet point summary of the Act.
- **Interactive UI**: View results in organized tabs (Summary, Definitions, etc.).
- **JSON Export**: Download the full extracted data as a JSON file.

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **AI Model**: Google Gemini (gemini-flash-latest)
- **Data Validation**: Pydantic
- **PDF Processing**: pypdf

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-folder>
    ```

2.  **Create a virtual environment** (optional but recommended):
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration

You need a **Google Gemini API Key** to run this project.

1.  Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  You can enter the key directly in the app's sidebar.
3.  **Optional**: Create a `.env` file to store it automatically:
    ```bash
    # .env
    GEMINI_API_KEY=your_api_key_here
    ```

## 🏃‍♂️ Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

1.  Enter your API Key in the sidebar (if not in `.env`).
2.  Upload a Legal PDF.
3.  Click **Analyze Document**.
4.  Explore the tabs and download the JSON report.

## 🧪 Testing

To run the unit tests for data models and extraction logic:

```bash
python test_extraction.py
```
