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
                
                # Create tabs for different sections
                tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
                    "Summary", "Definitions", "Sections", "Eligibility", "Entitlements", "Record Keeping"
                ])
                
                with tab1:
                    st.subheader(f"Document: {result.document_title}")
                    
                    # Metrics
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Definitions", len(result.definitions))
                    col2.metric("Sections", len(result.sections))
                    col3.metric("Entitlements", len(result.entitlements))
                    
                    st.markdown("### Executive Summary")
                    if result.executive_summary:
                        for point in result.executive_summary:
                            st.markdown(f"- {point}")
                    elif result.sections:
                        # Fallback to section summaries if executive summary is missing (backward compatibility)
                        for section in result.sections:
                            st.markdown(f"- **{section.section_number} {section.title}**: {section.content_summary}")
                    else:
                        st.write("No summary available.")
                        
                    st.divider()
                    
                    st.subheader("Raw JSON Output")
                    st.json(result.model_dump(mode='json'))
                    
                    # Download Button
                    json_str = json.dumps(result.model_dump(mode='json'), indent=2)
                    st.download_button(
                        label="Download JSON Report",
                        data=json_str,
                        file_name="legal_extraction.json",
                        mime="application/json"
                    )

                with tab2:
                    st.subheader("Definitions")
                    if result.definitions:
                        for item in result.definitions:
                            st.markdown(f"**{item.term}**: {item.definition}")
                    else:
                        st.write("No definitions found.")

                with tab3:
                    st.subheader("Legislative Sections")
                    if result.sections:
                        for item in result.sections:
                            with st.expander(f"Section {item.section_number}: {item.title}"):
                                st.write(item.content_summary)
                    else:
                        st.write("No sections found.")

                with tab4:
                    st.subheader("Eligibility Criteria")
                    if result.eligibility:
                        for item in result.eligibility:
                            st.markdown(f"- **{item.category or 'General'}**: {item.criteria}")
                    else:
                        st.write("No eligibility criteria found.")

                with tab5:
                    st.subheader("Payment & Entitlements")
                    if result.entitlements:
                        for item in result.entitlements:
                            st.markdown(f"### {item.entitlement_name}")
                            st.write(item.description)
                            if item.conditions:
                                st.caption(f"Conditions: {item.conditions}")
                            st.divider()
                    else:
                        st.write("No entitlements found.")

                with tab6:
                    st.subheader("Record Keeping")
                    if result.record_keeping:
                        for item in result.record_keeping:
                            st.markdown(f"- **Requirement**: {item.requirement}")
                            if item.duration:
                                st.caption(f"Duration: {item.duration}")
                    else:
                        st.write("No record keeping requirements found.")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

elif not api_key:
    st.info("Please provide a Google Gemini API Key to start.")
