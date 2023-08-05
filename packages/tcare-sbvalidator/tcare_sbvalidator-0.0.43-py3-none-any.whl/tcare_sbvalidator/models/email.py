from .tcare_cloud_event import TcareCloudEvent
from pydantic import BaseModel

# SMS
class EmailData(BaseModel):
    sender: str
    recipient: str
    email_subject: str
    content: str

class EmailServiceBusMessage(TcareCloudEvent):
  data: EmailData