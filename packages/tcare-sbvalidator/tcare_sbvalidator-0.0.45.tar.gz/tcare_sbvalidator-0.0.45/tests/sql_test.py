import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.handlers import Sms
from src.tcare_sbvalidator.models.sms import SmsData

NAMESPACE = config['NAMESPACELOCAL']
CONNECTION_STRING = config['CONNECTION_STRING']
SENDER = config['TEST_SMS_SENDER']
RECIPIENT = config['TEST_SMS_RECIPIENT']

async def main():
    handler = Sms()
    handler.connectWithCred(NAMESPACE)
    
    sms_data = SmsData(
      # sender=SENDER,
      recipient=RECIPIENT,
      content="Helloo!",
    )
    
    await handler.publish_message(sms_data)
    
    

asyncio.run(main())