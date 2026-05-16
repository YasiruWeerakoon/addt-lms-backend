from fastapi import APIRouter, Body, HTTPException
from database import student_collection
from models import StudentSignupSchema, UserLoginSchema
from hashing import Hash
from auth.jwt_handler import signJWT
from fastapi import Header, Depends
from auth.jwt_handler import decodeJWT
from bson.objectid import ObjectId

router = APIRouter()

@router.post("/student/register")
async def register_student(student: StudentSignupSchema = Body(...)):
    # 1. Check if email already exists
    existing_student = await student_collection.find_one({"email": student.email})
    if existing_student:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 2. Hash the password
    hashed_password = Hash.bcrypt(student.password)

    # 3. Prepare data for MongoDB
    new_student = {
        "fullname": student.fullname,
        "email": student.email,
        "password": hashed_password,
        "role": "student",  # Force role to always be 'student' for public signup
        "is_active": True
    }

    # 4. Insert into Database
    result = await student_collection.insert_one(new_student)
    
    return {
        "message": "Student registered successfully",
        "id": str(result.inserted_id)
    }

@router.post("/student/login")
async def login_student(user: UserLoginSchema = Body(...)):
    # 1. Find the user by email
    student = await student_collection.find_one({"email": user.email})
    
    # 2. Check if user exists & password matches
    if not student or not Hash.verify(user.password, student["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 3. Generate Token
    return signJWT(user_id=str(student["_id"]), role="student")

# --- Helper to get user from token ---
async def get_current_student(authorization: str = Header(...)):
    token = authorization.split(" ")[1] # Remove "Bearer " prefix
    payload = decodeJWT(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
        
    student = await student_collection.find_one({"_id": ObjectId(payload["user_id"])})
    return student

@router.get("/student/me")
async def get_student_profile(student: dict = Depends(get_current_student)):
    return {
        "fullname": student["fullname"],
        "email": student["email"],
        "role": student["role"]
    }