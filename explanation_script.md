# Project Presentation Script: Legal Document AI Extractor

## 1. Introduction & Problem Statement
"Hello everyone. The goal of this project was to build an AI-powered agent capable of analyzing complex legal documents—specifically the 'Credit Act 2025'—and extracting structured, actionable data. Manual review of such documents is time-consuming and prone to error, so we automated this using a Large Language Model (LLM)."

## 2. The Solution: Streamlit App
"I built a web application using **Streamlit**, which provides a simple and interactive interface. Let me walk you through it:"

*   **Upload**: "First, the user uploads a PDF document here."
*   **Configuration**: "We securely input the Google Gemini API key in the sidebar. This key authenticates us to use Google's powerful AI models."
*   **Processing**: "When I click 'Analyze Document', the app reads the PDF text and sends it to the AI for processing."
*   **Results**: "The results are presented in organized tabs:
    *   **Summary**: A high-level executive summary with key metrics.
    *   **Definitions**: A glossary of terms found in the act.
    *   **Sections**: A breakdown of legislative sections.
    *   **Entitlements**: Specific payments and conditions extracted from the text.
    *   **JSON Export**: Finally, we can download the raw structured data for use in other systems."

## 3. Technical Approach

### Architecture
"The system follows a modular 3-tier architecture:"
1.  **Frontend (`app.py`)**: Handles user interaction and display.
2.  **Logic Layer (`extractor.py`)**:
    *   Uses `pypdf` to extract raw text from the uploaded file.
    *   Prepares the prompt and schema for the AI.
    *   Cleans the data schema to ensure compatibility with the API.
3.  **Data Layer (`models.py`)**:
    *   We use **Pydantic** to define strict data models. This forces the AI to return data in a specific JSON structure, not just free text.
    *   This ensures we always get fields like 'Eligibility Criteria', 'Payment Amounts', and 'Obligations' reliably.

### AI Integration (Gemini)
"We switched from OpenAI to **Google Gemini (Flash model)** for this project.
*   **Why Gemini Flash?**: It offers a massive context window (1M+ tokens), allowing us to process entire legal acts in one go without splitting them up. It's also faster and more cost-effective.
*   **Structured Output**: We use Gemini's 'JSON Mode' with our Pydantic schema to guarantee the output is valid JSON, ready for database insertion."

### Challenges & Solutions
*   **Schema Compatibility**: "One challenge was that Gemini's API is strict about JSON schemas. It doesn't like 'default' values or 'optional' types. I wrote a custom schema cleaner in `extractor.py` to sanitize our data models before sending them to the API, ensuring smooth communication."

## 4. Conclusion
"In summary, this tool transforms unstructured legal text into structured, queryable data, significantly reducing the time required for legal compliance and review."
