import streamlit as st
import os
from extractor import extract_text_from_pdf, analyze_document
import json

st.set_page_config(page_title="Legal Doc Extractor", layout="wide")

st.title("📄 Legal Document AI Extractor (Gemini Powered)")
st.markdown("Upload a legal document (PDF) to extract structured information like definitions, eligibility, and entitlements.")

# Sidebar for API Key
with st.sidebar:
    st.header("Configuration")
    st.markdown("[Get your Google Gemini API Key](https://aistudio.google.com/app/apikey)")
    api_key = st.text_input("Google Gemini API Key", type="password", help="Enter your Google Gemini API Key here.")
    if not api_key:
        # Check environment variable
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        
    if api_key:
        api_key = api_key.strip() # Remove any leading/trailing whitespace/newlines
        st.success("API Key found!")
    else:
        st.warning("Please enter your Gemini API Key to proceed.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None and api_key:
    if st.button("Analyze Document"):
        with st.spinner("Extracting text and analyzing with Gemini AI..."):
            try:
                # 1. Extract Text
                text = extract_text_from_pdf(uploaded_file)
                st.info(f"Extracted {len(text)} characters from the PDF.")
                
                # 2. Analyze with LLM
                result = analyze_document(text, api_key)
                
                # 3. Display Results
                st.success("Analysis Complete!")
                
                st.subheader(f"Document: {result.document_title}")
                
            
                
                if result.executive_summary:
                    st.markdown(result.executive_summary)
                else:
                    st.error("Summary could not be generated.")
                    
                st.divider()
                
                # Create tabs with specific names requested by user
                tab_purp, tab_defs, tab_elig, tab_oblig, tab_enf = st.tabs([
                    "Purpose", "Key definitions", "Eligibility", "Obligations", "Enforcement elements"
                ])
                
                with tab_purp:
                    st.markdown("### Purpose")
                    if hasattr(result, 'purpose') and result.purpose:
                        st.markdown(result.purpose)
                    elif result.executive_summary:
                         # Fallback if purpose isn't extracted separately yet (for old cached results if any, though we re-run)
                         st.markdown(result.executive_summary)
                    else:
                        st.write("No purpose information available.")
                        
                with tab_defs:
                    st.markdown(result.definitions)
                    
                with tab_elig:
                    st.markdown("### Eligibility Criteria")
                    st.markdown(result.eligibility)
                    st.divider()
                    st.markdown("### Payments & Entitlements")
                    st.markdown(result.payments)
                    
                with tab_oblig:
                    st.markdown("### Obligations")
                    st.markdown(result.obligations)
                    st.divider()
                    st.markdown("### Responsibilities")
                    st.markdown(result.responsibilities)
                    
                with tab_enf:
                    st.markdown("### Penalties")
                    st.markdown(result.penalties)
                    st.divider()
                    st.markdown("### Record Keeping")
                    st.markdown(result.record_keeping)

                st.subheader("Raw JSON Output")
                
                # Create a dictionary for the JSON output that matches the requested format exactly
                # (excluding executive_summary which is for Task 2 display)
                json_output = result.model_dump(mode='json', exclude={'executive_summary', 'document_title'})
                
                st.json(json_output)
                
                # Download Button
                json_str = json.dumps(json_output, indent=2)
                st.download_button(
                    label="Download JSON Report",
                    data=json_str,
                    file_name="legal_extraction.json",
                    mime="application/json"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif not api_key:
    st.info("Please provide a Google Gemini API Key to start.")
