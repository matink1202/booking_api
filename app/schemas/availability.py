from datetime import time

from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator


class AvailabilityCreateSchema(BaseModel):
    
    day_of_week: int = Field(..., ge=0, le=6, description="week days(monday=0, sunday=6)")
    start_time: time = Field(..., description="start time")
    end_time: time = Field(..., description="end time")
    
    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError("end_time must be after start_time")
        return self
    

class AvailabilityOutSchema(BaseModel):
    
    id: UUID4 = Field(description="availability id")
    provider_id: UUID4 = Field(description="provider's id")
    day_of_week: int = Field(ge=0, le=6, description="week days(monday=0, sunday=6)")
    start_time: time = Field(description="start time")
    end_time: time = Field(description="end time")
    

    model_config = ConfigDict(from_attributes=True)