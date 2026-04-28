from fastapi import FastAPI
from routes import sensors, alerts

app = FastAPI(
    title="AquaGrid API",
    description="Backend API for AquaGrid - Solar powered atmospheric water generation system",
    version="1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

@app.get("/")
@app.head("/")
def home():
    return {
        "message": "Welcome to the AquaGrid API 🌊",
        "description": "Solar powered atmospheric water generation system",
        "version": "1.0",
        "endpoints": {
            "sensors": "/sensors",
            "alerts": "/alerts",
            "docs": "/docs"
        }
    }