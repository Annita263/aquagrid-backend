from fastapi import APIRouter
from database import sensor_collection, alert_collection
from models import AlertLog
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

async def simulate_sms(device_id: str, alert_type: str, message: str):
    """Simulates sending an SMS by logging it to MongoDB"""
    alert = AlertLog(
        device_id=device_id,
        alert_type=alert_type,
        message=message
    )
    await alert_collection.insert_one(alert.dict())
    print(f"📱 SMS SIMULATED [{datetime.now().strftime('%H:%M:%S')}] → {message}")
    return True

# POST - Manually trigger a test alert
@router.post("/test-sms")
async def send_test_sms(phone_number: str, message: str):
    try:
        await alert_collection.insert_one({
            "device_id": "test",
            "alert_type": "Test Alert",
            "message": message,
            "phone_number": phone_number,
            "timestamp": datetime.utcnow()
        })
        return {
            "message": "✅ SMS Simulated Successfully",
            "to": phone_number,
            "content": message,
            "note": "In production this would be sent via Africa's Talking"
        }
    except Exception as e:
        return {"message": "Failed", "error": str(e)}

# POST - Check latest reading and send alert if unsafe
@router.post("/check-and-alert")
async def check_and_alert(phone_number: str):
    # Get the latest sensor reading
    reading = await sensor_collection.find_one(sort=[("timestamp", -1)])

    if not reading:
        return {"message": "No readings found"}

    alerts_sent = []

    # Check TDS level
    if reading["tds_ppm"] >= 300:
        message = (
            f"⚠️ AquaGrid Alert: High TDS detected on "
            f"{reading['device_id']}. TDS: {reading['tds_ppm']} ppm. "
            f"Immediate maintenance required."
        )
        await simulate_sms(reading["device_id"], "High TDS", message)
        alerts_sent.append({
            "type": "High TDS",
            "message": message,
            "status": "Simulated ✅"
        })

    # Check pH level
    if not (6.5 <= reading["ph_level"] <= 8.5):
        message = (
            f"⚠️ AquaGrid Alert: Unsafe pH detected on "
            f"{reading['device_id']}. pH: {reading['ph_level']}. "
            f"Immediate maintenance required."
        )
        await simulate_sms(reading["device_id"], "Unsafe pH", message)
        alerts_sent.append({
            "type": "Unsafe pH",
            "message": message,
            "status": "Simulated ✅"
        })

    # Check battery level
    if reading["battery_level"] < 20:
        message = (
            f"⚠️ AquaGrid Alert: Low battery on "
            f"{reading['device_id']}. Battery: {reading['battery_level']}%. "
            f"Please check solar panels."
        )
        await simulate_sms(reading["device_id"], "Low Battery", message)
        alerts_sent.append({
            "type": "Low Battery",
            "message": message,
            "status": "Simulated ✅"
        })

    if not alerts_sent:
        return {"message": "All systems normal ✅ No alerts needed"}

    return {
        "alerts_triggered": len(alerts_sent),
        "alerts": alerts_sent,
        "note": "In production these would be sent as real SMS via Africa's Talking"
    }

# GET - Get all alert history
@router.get("/history")
async def get_alert_history():
    alerts = []
    async for alert in alert_collection.find():
        alert["_id"] = str(alert["_id"])
        alerts.append(alert)
    return alerts

# GET - Get alert count summary
# GET - Get alert count summary
@router.get("/summary")
async def get_alert_summary():
    try:
        total = await alert_collection.count_documents({})
        high_tds = await alert_collection.count_documents({"alert_type": "High TDS"})
        unsafe_ph = await alert_collection.count_documents({"alert_type": "Unsafe pH"})
        low_battery = await alert_collection.count_documents({"alert_type": "Low Battery"})

        return {
            "total_alerts": total,
            "high_tds_alerts": high_tds,
            "unsafe_ph_alerts": unsafe_ph,
            "low_battery_alerts": low_battery
        }
    except Exception as e:
        return {"error": str(e)}