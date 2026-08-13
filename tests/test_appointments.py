def create_patient(client):
    response = client.post(
        "/patients",
        json={
            "name": "Rahul Kumar",
            "email": "rahul@test.com",
            "phone": "9876543210",
        },
    )

    return response.json()["id"]


def create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr. Priya Sharma",
            "specialization": "Cardiology",
        },
    )

    return response.json()["id"]


def test_create_appointment(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["patient_id"] == patient_id
    assert data["doctor_id"] == doctor_id


def test_get_appointments(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    response = client.get("/appointments")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_appointment_by_id(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    create_response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    appointment_id = create_response.json()["id"]

    response = client.get(
        f"/appointments/{appointment_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == appointment_id


def test_get_appointment_not_found(client):
    response = client.get("/appointments/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Appointment not found"


def test_overlapping_appointment_rejected(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    first_response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    assert first_response.status_code == 201

    overlapping_response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:30:00",
            "appointment_end": "2026-08-14T11:30:00",
        },
    )

    assert overlapping_response.status_code == 400
    assert (
        overlapping_response.json()["detail"]
        == "Doctor already has an appointment during this time"
    )


def test_back_to_back_appointment_allowed(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T11:00:00",
            "appointment_end": "2026-08-14T12:00:00",
        },
    )

    assert response.status_code == 201


def test_patient_not_found_for_appointment(client):
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": 999,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Patient not found"


def test_doctor_not_found_for_appointment(client):
    patient_id = create_patient(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": 999,
            "appointment_start": "2026-08-14T10:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Doctor not found"


def test_invalid_appointment_time(client):
    patient_id = create_patient(client)
    doctor_id = create_doctor(client)

    response = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "appointment_start": "2026-08-14T12:00:00",
            "appointment_end": "2026-08-14T11:00:00",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Appointment start time must be before appointment end time"
    )