import pypdf
import google.generativeai as genai
from models import LegalDocument
import json

def extract_text_from_pdf(file) -> str:
    """Extracts text from a PDF file object."""
    try:
        reader = pypdf.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF: {str(e)}")

def analyze_document(text: str, api_key: str) -> LegalDocument:
    """
    Analyzes the provided text using Google's Gemini API to extract structured legal data.
    """
    try:
        genai.configure(api_key=api_key.strip())
        
        # Helper to remove 'default' and resolve '$defs'
        def clean_schema(schema, defs=None):
            if defs is None:
                defs = schema.get("$defs", {})
            
            if isinstance(schema, dict):
                if "$ref" in schema:
                    ref_key = schema["$ref"].split("/")[-1]
                    return clean_schema(defs[ref_key], defs)
                
                cleaned = {}
                for k, v in schema.items():
                    # Remove keys not supported by Gemini's strict schema
                    if k == "$defs" or k == "default" or k == "anyOf":
                        continue
                    # Only remove 'title' if it's a metadata string, not if it's a field definition (dict)
                    if k == "title" and isinstance(v, str):
                        continue
                        
                    cleaned[k] = clean_schema(v, defs)
                return cleaned
            elif isinstance(schema, list):
                return [clean_schema(i, defs) for i in schema]
            return schema

        # Get schema and clean it
        schema = LegalDocument.model_json_schema()
        cleaned_schema = clean_schema(schema)

        # Using gemini-flash-latest as it is available in the user's region/key
        model = genai.GenerativeModel(
            'gemini-flash-latest',
            generation_config={
                "response_mime_type": "application/json",
                "response_schema": cleaned_schema
            }
        )
        
        prompt = f"""
        You are an expert legal analyst AI. Your task is to analyze the provided legal document text 
        and extract structured information according to the schema.
        
        Focus on:
        1. Definitions: Extract key terms and their definitions.
        2. Legislative Sections: Identify main sections, their titles, and summaries.
        3. Eligibility Criteria: Extract specific criteria for eligibility.
        4. Payment/Entitlements: Identify what payments or entitlements are described and their conditions.
        5. Record Keeping: Extract any requirements for keeping records or reporting.
        6. Executive Summary: Generate 5-10 bullet points summarizing the entire Act, specifically covering:
           - Purpose
           - Key definitions
           - Eligibility
           - Obligations
           - Enforcement elements
        
        Be precise and extract information exactly as stated in the text.
        
        Document Text:
        {text[:100000]} 
        """
        # Truncate to avoid token limits if extremely large, though Gemini 1.5 has huge context.
        
        response = model.generate_content(prompt)
        
        # Parse the JSON response directly into the Pydantic model
        return LegalDocument.model_validate_json(response.text)
        
    except Exception as e:
        raise Exception(f"Error during Gemini analysis: {str(e)}")
