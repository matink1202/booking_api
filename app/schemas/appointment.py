from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field

from app.models.appointment import AppointmentStatus


class AppointmentCreateSchema(BaseModel):
    
    provider_id: UUID4 = Field(..., description="provider id")
    service_id: UUID4 = Field(..., description="service id")
    start_time: datetime = Field(..., description="start of the session time")
    
    
class AppointmentStatusUpdateSchema(BaseModel):
    
    status: AppointmentStatus = Field(..., description="appointment's status")
    
    
class AppointmentOutSchema(BaseModel):
    
    id: UUID4 = Field(description="appointment's id")
    customer_id: UUID4 = Field(description="customer's id")
    provider_id: UUID4 = Field(description="provider's id")
    service_id: UUID4 = Field(description="service's id")
    
    start_time: datetime = Field(description="start of the session time")
    end_time: datetime = Field(description="end of the session time")
    created_at: datetime = Field(description="time of creation of booking")
    
    status: AppointmentStatus = Field(..., description="appointment's status")
    
    model_config = ConfigDict(from_attributes=True)