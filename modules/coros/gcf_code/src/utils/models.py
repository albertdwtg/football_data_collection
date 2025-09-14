"""Module to define data models"""

from pydantic import BaseModel, validator, Extra
from typing import Optional

DATE_FORMAT_LENGTH = 8

class Metadata(BaseModel):
    """
    Metadata model for data export
    """
    method: str
    url: str
    request_uuid: str
    file_name: str
    ingestion_time: str
    query_params: Optional[dict] = "Empty"
    body: Optional[dict] = "Empty"

    class Config:
        """Config for metadata model"""
        extra = Extra.forbid

class DataExport(BaseModel):
    """ 
    Data model for data export
    """
    file_name: str
    data: dict
    metadata: Metadata

class InputRequest(BaseModel):
    """
    Input request model
    """
    account: str
    from_date: int
    to_date: int

    # ruff: noqa: N805
    @validator("from_date", "to_date")
    def validate_date_format(cls, v: int) -> None:
        """Check if date is in YYYYMMDD format

        Args:
            v (int): Date to validate in YYYYMMDD format

        Raises:
            ValueError: If date is not in YYYYMMDD format
        """
        if len(str(v)) != DATE_FORMAT_LENGTH:
            raise ValueError("Date must be in fomat YYYYMMDD.")

    # ruff: noqa: N805
    @validator("account")
    def validate_email_format(cls, v: str) -> None:
        """Check if email is valid

        Args:
            v (str): email to validate

        Raises:
            ValueError: if email is not valid
        """
        if "@" not in v:
            raise ValueError('Email must contain "@" character.')
        if "." not in v:
            raise ValueError('Email must contain "." character.')
    
    class Config:
        """ Config for input request model """
        extra = Extra.forbid