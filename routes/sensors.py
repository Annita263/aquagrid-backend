from fastapi import APIRouter
from database import sensor_collection
from models import SensorReading
from datetime import datetime

router = APIRouter()

# POST - Save a new sensor reading from the IoT device
@router.post("/")
async def add_sensor_reading(reading: SensorReading):
    reading_dict = reading.dict()
    result = await sensor_collection.insert_one(reading_dict)
    return {"message": "Reading saved successfully", "id": str(result.inserted_id)}

# GET - Retrieve all sensor readings
@router.get("/")
async def get_all_readings():
    readings = []
    async for reading in sensor_collection.find():
        reading["_id"] = str(reading["_id"])
        readings.append(reading)
    return readings

# GET - Get only the latest sensor reading
@router.get("/latest")
async def get_latest_reading():
    reading = await sensor_collection.find_one(sort=[("timestamp", -1)])
    if reading:
        reading["_id"] = str(reading["_id"])
        return reading
    return {"message": "No readings found"}

# GET - Get readings for a specific device
@router.get("/device/{device_id}")
async def get_device_readings(device_id: str):
    readings = []
    async for reading in sensor_collection.find({"device_id": device_id}):
        reading["_id"] = str(reading["_id"])
        readings.append(reading)
    if readings:
        return readings
    return {"message": f"No readings found for device {device_id}"}

# GET - Get water quality status
@router.get("/status/water-quality")
async def get_water_quality_status():
    reading = await sensor_collection.find_one(sort=[("timestamp", -1)])
    if not reading:
        return {"message": "No readings found"}
    
    tds = reading["tds_ppm"]
    ph = reading["ph_level"]
    
    # Check against WHO standards
    tds_safe = tds < 300
    ph_safe = 6.5 <= ph <= 8.5
    
    return {
        "device_id": reading["device_id"],
        "tds_ppm": tds,
        "ph_level": ph,
        "tds_status": "Safe ✅" if tds_safe else "Unsafe ❌",
        "ph_status": "Safe ✅" if ph_safe else "Unsafe ❌",
        "overall_status": "Safe for drinking ✅" if tds_safe and ph_safe else "Not safe for drinking ❌",
        "timestamp": reading["timestamp"]
    }