import os
from PIL import Image, ImageDraw

assets_dir = r"C:\Users\HP\cynbit-ai-cognicare\assets"
os.makedirs(assets_dir, exist_ok=True)

samples = [
    {
        "filename": "burst_pipe_leak.png",
        "bg_color": (30, 41, 59),
        "accent": (56, 189, 248),
        "title": "URGENT: Burst Copper Pipe Under Sink",
        "details": ["Location: Kitchen Cabinet B-12", "Flow Rate: ~4 Liters/min active spray", "Hazard: Water pooling near baseboards", "P1 Severity Indicator: High Risk"]
    },
    {
        "filename": "electrical_sparking_outlet.png",
        "bg_color": (40, 20, 20),
        "accent": (239, 68, 68),
        "title": "HAZARD: Scorched 220V Wall Outlet",
        "details": ["Location: Master Bedroom East Wall", "Condition: Visible soot, buzzing hum", "Hazard: Immediate Arc-Flash & Fire Risk", "P1 Severity Indicator: Critical Emergency"]
    },
    {
        "filename": "ac_compressor_failure.png",
        "bg_color": (30, 45, 40),
        "accent": (245, 158, 11),
        "title": "HVAC: Error Code E4 - Low Refrigerant",
        "details": ["Location: Rooftop Condenser Unit 4A", "Symptoms: Warm airflow, icing on coils", "Hazard: Compressor lockup risk", "P2 Severity Indicator: High Urgency"]
    },
    {
        "filename": "minor_faucet_drip.png",
        "bg_color": (25, 30, 45),
        "accent": (96, 165, 250),
        "title": "MAINTENANCE: Aerator Washer Degradation",
        "details": ["Location: Guest Bathroom Vanity", "Flow: 1 drip every 3 seconds", "Hazard: Minor water waste, no flooding", "P4 Severity Indicator: Routine Maintenance"]
    }
]

for s in samples:
    img = Image.new("RGB", (640, 480), color=s["bg_color"])
    draw = ImageDraw.Draw(img)
    
    draw.rectangle([15, 15, 625, 465], outline=s["accent"], width=3)
    draw.rectangle([25, 25, 615, 90], fill=(20, 25, 35), outline=s["accent"], width=1)
    
    draw.text((40, 45), s["title"], fill=s["accent"])
    draw.text((450, 65), "TENANTEASE CAM 1080P", fill=(148, 163, 184))
    
    draw.rectangle([60, 130, 360, 420], outline=(220, 38, 38) if "HAZARD" in s["title"] or "URGENT" in s["title"] else s["accent"], width=2)
    draw.text((70, 140), "DETECTED DEFECT REGION (AI BBOX)", fill=(248, 250, 252))
    
    draw.rectangle([390, 130, 610, 420], fill=(15, 23, 42), outline=(71, 85, 105), width=1)
    draw.text((410, 150), "TELEMETRY METRICS:", fill=(226, 232, 240))
    y = 190
    for detail in s["details"]:
        draw.text((410, y), f"• {detail}", fill=(203, 213, 225))
        y += 40
        
    draw.text((410, 380), "STATUS: PENDING AI TRIAGE", fill=s["accent"])
    
    path = os.path.join(assets_dir, s["filename"])
    img.save(path)
