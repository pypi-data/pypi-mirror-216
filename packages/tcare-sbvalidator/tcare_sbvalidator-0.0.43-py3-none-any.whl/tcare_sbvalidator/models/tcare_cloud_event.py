from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# TCARE Cloud Events
class Options(BaseModel):
  expedite: bool

class TcareCloudEvent(BaseModel):
  specversion: str
  type: str
  id: str
  time: datetime
  datacontenttype: str
  