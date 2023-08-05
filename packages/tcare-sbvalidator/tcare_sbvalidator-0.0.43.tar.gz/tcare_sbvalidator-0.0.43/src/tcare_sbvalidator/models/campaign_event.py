from .tcare_cloud_event import TcareCloudEvent
from pydantic import BaseModel

class CampaignEventData(BaseModel):
  source: str # i.e. assist - this will be useful for analytics
  campaign: str
  case_id: str
  caregiver_id: str
  first_name: str
  last_name: str
  care_reciver_first_name: str
  car_receiver_last_name: str
  action: str # i.e. start, stop
  email: str
  phone: str
  # resources: List[Resource] # not sure if this is necessary yet, but could be helpful to provide this information to jog their memory

class CampaignEventServiceBusMessage(TcareCloudEvent):  
  data: CampaignEventData