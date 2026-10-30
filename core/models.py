from enum import Enum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class SeverityLevel(str, Enum):
    P1_CRITICAL = "P1_CRITICAL"
    P2_HIGH = "P2_HIGH"
    P3_MEDIUM = "P3_MEDIUM"
    P4_LOW = "P4_LOW"


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
    unit_id: str
    tenant_name: str
    description: str
    has_image: bool = False
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
    confidence_score: float
    summary_title: str
    root_cause_hypothesis: str
    safety_guidance: SafetyGuidance
    cost_estimate: CostEstimate
    sla_hours: int
    contractor_match: ContractorMatch
    reasoning_trace: List[str]
    audit_verdict: str
