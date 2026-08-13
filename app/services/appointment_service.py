from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.doctor import Doctor
from app.models.patient import Patient
from app.schemas.appointment import AppointmentCreate


def create_appointment(
    db: Session,
    appointment_data: AppointmentCreate,
) -> Appointment:

    # Check that patient exists
    patient = (
        db.query(Patient)
        .filter(Patient.id == appointment_data.patient_id)
        .first()
    )

    if patient is None:
        raise ValueError("Patient not found")

    # Check that doctor exists
    doctor = (
        db.query(Doctor)
        .filter(Doctor.id == appointment_data.doctor_id)
        .first()
    )

    if doctor is None:
        raise ValueError("Doctor not found")

    # Validate appointment time
    if appointment_data.appointment_start >= appointment_data.appointment_end:
        raise ValueError(
            "Appointment start time must be before appointment end time"
        )

    # Check for overlapping appointment
    overlapping_appointment = (
        db.query(Appointment)
        .filter(
            Appointment.doctor_id == appointment_data.doctor_id,
            Appointment.appointment_start
            < appointment_data.appointment_end,
            Appointment.appointment_end
            > appointment_data.appointment_start,
        )
        .first()
    )

    if overlapping_appointment is not None:
        raise ValueError(
            "Doctor already has an appointment during this time"
        )

    # Create appointment
    new_appointment = Appointment(
        patient_id=appointment_data.patient_id,
        doctor_id=appointment_data.doctor_id,
        appointment_start=appointment_data.appointment_start,
        appointment_end=appointment_data.appointment_end,
    )

    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)

    return new_appointment