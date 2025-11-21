from pydantic import BaseModel, Field
from typing import List

class Definition(BaseModel):
    term: str = Field(..., description="The term being defined")
    definition: str = Field(..., description="The definition of the term")

class LegislativeSection(BaseModel):
    section_number: str = Field(..., description="The section number (e.g., '1.2')")
    title: str = Field(..., description="The title of the section")
    content_summary: str = Field(..., description="A brief summary of the section's content")

class EligibilityCriteria(BaseModel):
    criteria: str = Field(..., description="A specific eligibility criterion")
    category: str = Field("", description="Category of eligibility (e.g., 'Age', 'Income'). Empty string if not applicable.")

class PaymentEntitlement(BaseModel):
    entitlement_name: str = Field(..., description="Name of the entitlement or payment")
    description: str = Field(..., description="Description of what is provided")
    conditions: str = Field("", description="Conditions required to receive this entitlement. Empty string if none.")

class RecordKeepingRequirement(BaseModel):
    requirement: str = Field(..., description="The specific record-keeping requirement")
    duration: str = Field("", description="How long records must be kept. Empty string if not specified.")

class LegalDocument(BaseModel):
    document_title: str = Field(..., description="The title of the document")
    definitions: List[Definition] = Field(default_factory=list, description="List of defined terms")
    sections: List[LegislativeSection] = Field(default_factory=list, description="Key legislative sections")
    eligibility: List[EligibilityCriteria] = Field(default_factory=list, description="Eligibility criteria found in the document")
    entitlements: List[PaymentEntitlement] = Field(default_factory=list, description="Payments or entitlements details")
    record_keeping: List[RecordKeepingRequirement] = Field(default_factory=list, description="Record keeping and reporting requirements")
    executive_summary: List[str] = Field(default_factory=list, description="5-10 bullet points summarizing the act (Purpose, Definitions, Eligibility, Obligations, Enforcement)")
