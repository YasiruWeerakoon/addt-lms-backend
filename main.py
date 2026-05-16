from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.student import router as student_router  # <--- IMPORT THIS

app = FastAPI()

# --- CORS (Allow Frontend to talk to Backend) ---
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Routes ---
app.include_router(student_router, tags=["Students"]) # <--- ADD THIS LINE

@app.get("/")
def read_root():
    return {"message": "ADDT LMS Backend is Alive! 🚀"}