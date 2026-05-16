import motor.motor_asyncio
from bson.objectid import ObjectId

# 1. Connection String (Replace with your actual MongoDB URL later)
# For now, we use localhost. If you use MongoDB Atlas, paste that URL here.
MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# 2. Create the Database named 'addt_lms'
database = client.addt_lms

# 3. Collections (Tables)
student_collection = database.get_collection("students")
instructor_collection = database.get_collection("instructors")
admin_collection = database.get_collection("admins")
course_collection = database.get_collection("courses")

# --- Helper: Fix MongoDB ID ---
# MongoDB uses "_id" (ObjectId), but frontend wants "id" (string).
def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "role": "student",
    }