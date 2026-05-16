from pydantic import BaseModel, EmailStr, Field

# 1. Schema for Registering a Student
class StudentSignupSchema(BaseModel):
    fullname: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    is_verified: bool = False # <--- Add this! Default is False

    class Config:
        json_schema_extra = {
            "example": {
                "fullname": "Alex Student",
                "email": "alex@demo.com",
                "password": "securepassword123"
            }
        }

# 2. Schema for Login (We'll use this later)
class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str