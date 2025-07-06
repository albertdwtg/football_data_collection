"""Module to define data models"""

from pydantic import BaseModel
from typing import Optional

class Metadata(BaseModel):
    """
    Metadata model for data export
    """
    method: str
    url: str
    request_uuid: str
    file_name: str
    ingestion_time: str
    query_params: Optional[dict] = None
    body: Optional[dict] = None

class DataExport(BaseModel):
    """ 
    Data model for data export
    """
    file_name: str
    data: dict
    metadata: Metadata