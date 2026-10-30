"""
Data schemas and models for TenantEase CogniCare.
"""
from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SeverityLevel(str, Enum):
    P1_CRITICAL = "P1_CRITICAL"  # Immediate hazard (flooding, electrical fire, gas) - SLA: < 2 hrs
    P2_HIGH = "P2_HIGH"          # Major disruption (heating down in winter, main AC in heatwave) - SLA: < 6 hrs
    P3_MEDIUM = "P3_MEDIUM"      # Functional inconvenience (dishwater broken, slow drain) - SLA: < 24 hrs
    P4_LOW = "P4_LOW"            # Cosmetic / routine (paint chip, cabinet hinge loose) - SLA: < 72 hrs


class DefectCategory(str, Enum):
    PLUMBING = "Plumbing"
    ELECTRICAL = "Electrical"
    HVAC = "HVAC / Climate Control"
    APPLIANCE = "Appliance"
    STRUCTURAL = "Structural & Roofing"
    SAFETY_SECURITY = "Safety & Security"
    OTHER = "General Maintenance"


class ContractorSpecialty(str, Enum):
    LICENSED_PLUMBER = "Licensed Master Plumber"
    LICENSED_ELECTRICIAN = "Certified Master Electrician"
    HVAC_TECHNICIAN = "EPA-Certified HVAC Technician"
    APPLIANCE_SPECIALIST = "Appliance Repair Specialist"
    GENERAL_HANDYMAN = "Licensed General Handyman"
    EMERGENCY_RESTORATION = "24/7 Water & Fire Remediation"


class TriageRequest(BaseModel):
    unit_id: str = Field(..., description="Property unit identifier e.g., Unit-402")
    tenant_name: str = Field(..., description="Tenant full name")
    description: str = Field(..., description="Tenant text or audio transcription of issue")
    has_image: bool = Field(default=False, description="Whether an image attachment is provided")
    image_metadata: Optional[Dict[str, Any]] = None
    urgency_claimed_by_tenant: Optional[str] = "Normal"


class SafetyGuidance(BaseModel):
    hazard_detected: bool
    hazard_type: Optional[str] = None
    immediate_action_steps: List[str] = Field(default_factory=list)
    warning_box: Optional[str] = None


class CostEstimate(BaseModel):
    min_cost_inr: int
    max_cost_inr: int
    avg_labor_hours: float
    parts_likely_needed: List[str]


class ContractorMatch(BaseModel):
    recommended_contractor: str
    specialty: ContractorSpecialty
    eta_hours: float
    estimated_rate_per_hour_inr: int
    matched_reason: str


class TriageResult(BaseModel):
    ticket_id: str
    timestamp: str
    unit_id: str
    tenant_name: str
    category: DefectCategory
    severity: SeverityLevel
    confidence_score: float = Field(ge=0.0, le=1.0)
    summary_title: str
    root_cause_hypothesis: str
    safety_guidance: SafetyGuidance
    cost_estimate: CostEstimate
    sla_hours: int
    contractor_match: ContractorMatch
    reasoning_trace: List[str]
    audit_verdict: str
