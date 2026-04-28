import asyncio
import httpx
import random
from datetime import datetime

# Your API URL
API_URL = "http://127.0.0.1:8000/sensors/"

# List of simulated AquaGrid devices
DEVICES = ["aquagrid-unit-01", "aquagrid-unit-02", "aquagrid-unit-03"]

def generate_reading(device_id: str):
    """Generate a realistic fake sensor reading"""
    return {
        "device_id": device_id,
        
        # Normal output is 10-20 litres, occasionally drops lower
        "water_output_litres": round(random.uniform(5.0, 20.0), 2),
        
        # WHO safe level is below 300 ppm, occasionally spikes for alerts
        "tds_ppm": round(random.uniform(30.0, 350.0), 2),
        
        # WHO safe range is 6.5 to 8.5, occasionally goes outside for alerts
        "ph_level": round(random.uniform(6.0, 9.0), 2),
        
        # Battery level between 10% and 100%
        "battery_level": round(random.uniform(10.0, 100.0), 2),
        
        # Mostly active, occasionally needs maintenance
        "status": random.choice(["active", "active", "active", "maintenance"]),
        
        "timestamp": datetime.utcnow().isoformat()
    }

async def send_reading(client: httpx.AsyncClient, device_id: str):
    """Send a single reading to the API"""
    reading = generate_reading(device_id)
    try:
        response = await client.post(API_URL, json=reading)
        if response.status_code == 200:
            print(f"✅ [{datetime.now().strftime('%H:%M:%S')}] Reading sent for {device_id} | "
                  f"Water: {reading['water_output_litres']}L | "
                  f"TDS: {reading['tds_ppm']} ppm | "
                  f"pH: {reading['ph_level']} | "
                  f"Battery: {reading['battery_level']}%")
        else:
            print(f"❌ Failed to send reading for {device_id}: {response.text}")
    except Exception as e:
        print(f"❌ Error sending reading for {device_id}: {str(e)}")

async def run_simulator():
    """Run the simulator continuously"""
    print("🌊 AquaGrid IoT Simulator Started")
    print(f"📡 Sending data to: {API_URL}")
    print(f"🔧 Simulating {len(DEVICES)} devices: {', '.join(DEVICES)}")
    print("=" * 60)
    
    async with httpx.AsyncClient() as client:
        while True:
            # Send a reading for each device
            for device_id in DEVICES:
                await send_reading(client, device_id)
            
            # Wait 10 seconds before next batch of readings
            print(f"\n⏳ Next readings in 10 seconds...\n")
            await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(run_simulator())