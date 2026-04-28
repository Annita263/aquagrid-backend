from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class SensorReading(BaseModel):
    device_id: str                  # Which AquaGrid unit sent this e.g "aquagrid-unit-01"
    water_output_litres: float      # How much water was produced
    tds_ppm: float                  # Water quality (Total Dissolved Solids) - WHO safe level is below 300
    ph_level: float                 # pH of the water - WHO safe range is 6.5 to 8.5
    battery_level: float            # Solar battery percentage
    status: str                     # "active" or "maintenance"
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)

class AlertLog(BaseModel):
    device_id: str                  # Which unit triggered the alert
    alert_type: str                 # e.g "Low Water Quality" or "Low Battery"
    message: str                    # The actual SMS message that was sent
    timestamp: Optional[datetime] = Field(default_factory=datetime.utcnow)