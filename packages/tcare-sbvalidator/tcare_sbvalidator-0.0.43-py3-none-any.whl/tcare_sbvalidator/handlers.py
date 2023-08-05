from .base_handler import BaseHandler
from .models.sms import SmsServiceBusMessage
from .models.email import EmailServiceBusMessage
from .models.campaign_event import CampaignEventServiceBusMessage

class Sms(BaseHandler):
    messageSchema = SmsServiceBusMessage
    topic = "send-sms"
    
class Email(BaseHandler):
    messageSchema = EmailServiceBusMessage
    topic = "send-email"
    
class CampaignEvent(BaseHandler):
    messageSchema = CampaignEventServiceBusMessage
    topic = "campaign-event"