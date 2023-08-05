import asyncio, sys, random
from dotenv import dotenv_values
config = dotenv_values(".env")

from random_word import RandomWords
r = RandomWords()

def ra():
  return r.get_random_word()

def random_with_N_digits(n):
  range_start = 10**(n-1)
  range_end = (10**n)-1
  return random.randint(range_start, range_end)

sys.path.append("..")
from src.tcare_sbvalidator.handlers import CampaignEvent
from src.tcare_sbvalidator.models.campaign_event import CampaignEventData


NAMESPACE = config['NAMESPACELOCAL']
SMS_RECIPIENT = config['TEST_SMS_RECIPIENT']
EMAIL_RECIPIENT = config['TEST_EMAIL_RECIPIENT']

async def main():
    handler = CampaignEvent()
    handler.connectWithCred(NAMESPACE)
    
    campaign_event_data = CampaignEventData(
      source="assist",
      campaign="elevance-1",
      case_id="1",
      caregiver_id="1",
      first_name=ra(),
      last_name=ra(),
      action="start",
      email=f"{ra()}@{ra()}.com",
      phone=f"+{random_with_N_digits(11)}"
      # email=EMAIL_RECIPIENT,
      # phone=SMS_RECIPIENT,
    )
    
    await handler.publish_message(campaign_event_data)

asyncio.run(main())