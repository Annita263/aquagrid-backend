from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import ssl

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

# Create SSL context that works with Render's environment
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

# Create the connection to MongoDB with SSL fix
client = AsyncIOMotorClient(
    MONGO_URI,
    tls=True,
    tlsAllowInvalidCertificates=True
)

# Select the aquagrid database
db = client.aquagrid

# Define your collections
sensor_collection = db["sensor_readings"]
alert_collection = db["alerts"]