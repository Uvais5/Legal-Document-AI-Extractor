from pydantic import BaseModel, Field
from typing import List

class LegalDocument(BaseModel):
    document_title: str = Field(..., description="The title of the document")
    definitions: str = Field(..., description="Summary of key definitions found in the act")
    obligations: str = Field(..., description="Summary of obligations mentioned in the act")
    responsibilities: str = Field(..., description="Summary of responsibilities mentioned in the act")
    eligibility: str = Field(..., description="Summary of eligibility criteria")
    payments: str = Field(..., description="Summary of payments and entitlements")
    penalties: str = Field(..., description="Summary of penalties and enforcement elements")
    record_keeping: str = Field(..., description="Summary of record keeping requirements")
    purpose: str = Field(..., description="A specific statement of the Act's purpose")
    executive_summary: str = Field(..., description="5-10 bullet points summarizing the act in Markdown format (use hyphens for bullets, NO HTML)")
