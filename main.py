from fastapi import FastAPI
from routes import sensors, alerts

# Create the FastAPI app
app = FastAPI(
    title="AquaGrid API",
    description="Backend API for AquaGrid - Solar powered atmospheric water generation system",
    version="1.0"
)

# Register routes
app.include_router(sensors.router, prefix="/sensors", tags=["Sensors"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])

# Home route
@app.get("/")
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