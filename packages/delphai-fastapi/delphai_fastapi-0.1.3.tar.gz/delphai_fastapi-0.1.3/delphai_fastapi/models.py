from typing import Optional, List

from fastapi_camelcase import CamelModel
from pydantic import Field
from datetime import datetime

from companies.models import Company


class HTTPExceptionModel(CamelModel):
    detail: str


class Location(CamelModel):
    country: Optional[str] = Field(
        description="Company address (country)", example="Germany"
    )
    city: Optional[str] = Field(description="Company address (city)", example="Berlin")
    continent: Optional[str] = Field(
        description="Company address (continent)", example="Europe"
    )
    state: Optional[str] = Field(
        description="Company address (state/land)", example="Berlin"
    )
    latitude: Optional[float] = Field(example=52.5167)
    longitude: Optional[float] = Field(example=13.3833)
    zip_code: Optional[str] = Field(
        description="Company address (ZIP code)", example="10999"
    )

class Project(CamelModel):
    total: int = Field(..., description="Total number of companies in this project", example=35)
    name:  str = Field(..., description="Name of the project", example="Healthcare | Startups")
    created: datetime = Field(..., description="When the project was created")
    last_modified: datetime = Field(..., description="When the project was last edited or updated")
    available: int = Field(..., description="Number of companies in this project that are accessible in the dashboard", example=29)


class Source(CamelModel): 
    name: str = Field(description="Name of the source")
    credibility_score: float = Field(description="Credibility score of source in percentage", example=0.60)