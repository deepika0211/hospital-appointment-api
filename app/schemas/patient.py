from pydantic import BaseModel, ConfigDict, EmailStr


class PatientCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str


class PatientResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str

    model_config = ConfigDict(from_attributes=True)