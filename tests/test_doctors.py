def test_create_doctor(client):
    response = client.post(
        "/doctors",
        json={
            "name": "Dr. Priya Sharma",
            "specialization": "Cardiology",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["id"] == 1
    assert data["name"] == "Dr. Priya Sharma"
    assert data["specialization"] == "Cardiology"


def test_get_doctors(client):
    client.post(
        "/doctors",
        json={
            "name": "Dr. Priya Sharma",
            "specialization": "Cardiology",
        },
    )

    response = client.get("/doctors")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["name"] == "Dr. Priya Sharma"


def test_get_doctor_by_id(client):
    create_response = client.post(
        "/doctors",
        json={
            "name": "Dr. Priya Sharma",
            "specialization": "Cardiology",
        },
    )

    doctor_id = create_response.json()["id"]

    response = client.get(f"/doctors/{doctor_id}")

    assert response.status_code == 200
    assert response.json()["id"] == doctor_id


def test_get_doctor_not_found(client):
    response = client.get("/doctors/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Doctor not found"