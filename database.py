from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Get the MongoDB connection string from .env
MONGO_URI = os.getenv("MONGO_URI")

# Create the connection to MongoDB
client = AsyncIOMotorClient(MONGO_URI)

# Select the aquagrid database
db = client.aquagrid

# Define your collections (like tables in SQL)
sensor_collection = db["sensor_readings"]  # Stores all sensor data
alert_collection = db["alerts"]            # Stores all alert history