from fastapi import FastAPI

from app.routers.appointment import router as appointment_router
from app.routers.doctor import router as doctor_router
from app.routers.patient import router as patient_router

app = FastAPI(
    title="Hospital Appointment Management API",
    description="API for managing patients, doctors, and appointments.",
    version="1.0.0",
)

app.include_router(patient_router)
app.include_router(doctor_router)
app.include_router(appointment_router)


@app.get("/")
def root():
    return {
        "message": "Hospital Appointment Management API is running"
    }