from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from PIL import Image
import io

from core.models import TriageRequest, TriageResult
from core.agent import CogniCareAgent
from core.benchmarks import get_benchmark_dataframe

app = FastAPI(
    title="TenantEase CogniCare API",
    version="2.4.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = CogniCareAgent()

@app.get("/")
def read_root():
    return {
        "service": "TenantEase CogniCare API",
        "status": "operational",
        "version": "2.4.0",
        "docs_url": "/docs"
    }

@app.post("/api/v1/triage", response_model=TriageResult)
async def triage_ticket(
    unit_id: str = Form(...),
    tenant_name: str = Form(...),
    description: str = Form(...),
    urgency_claimed: Optional[str] = Form("Normal"),
    image_file: Optional[UploadFile] = File(None)
):
    pil_image = None
    if image_file:
        try:
            content = await image_file.read()
            pil_image = Image.open(io.BytesIO(content)).convert("RGB")
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Invalid image format: {e}")

    req = TriageRequest(
        unit_id=unit_id,
        tenant_name=tenant_name,
        description=description,
        has_image=bool(pil_image),
        urgency_claimed_by_tenant=urgency_claimed
    )

    return agent.triage(req, pil_image)

@app.get("/api/v1/benchmarks")
def read_benchmarks():
    df = get_benchmark_dataframe()
    return df.to_dict(orient="records")

@app.get("/api/v1/analytics")
def read_analytics():
    return {
        "active_units_monitored": 1420,
        "monthly_tickets_processed": 384,
        "average_first_response_time_seconds": 1.4,
        "p1_emergency_sla_compliance_rate": "99.8%",
        "maintenance_cost_reduction_percent": "34.2%",
        "contractor_first_time_fix_rate": "94.6%",
        "tenant_satisfaction_csat": "4.92 / 5.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
