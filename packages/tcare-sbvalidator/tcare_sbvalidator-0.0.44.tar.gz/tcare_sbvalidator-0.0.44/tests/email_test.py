import asyncio, sys
from dotenv import dotenv_values
config = dotenv_values(".env")

sys.path.append("..")
from src.tcare_sbvalidator.handlers import Email
from src.tcare_sbvalidator.models.email import EmailData


NAMESPACE = config['NAMESPACELOCAL']
CONNECTION_STRING = config['CONNECTION_STRING']
SENDER = config['TEST_EMAIL_SENDER']
RECIPIENT = config['TEST_EMAIL_RECIPIENT']

async def main():
    handler = Email()
    handler.connectWithCred(NAMESPACE)
    
    email_data = EmailData(
      sender=SENDER,
      recipient=RECIPIENT,
      email_subject="test_subject",
      content="Helloo!",
    )
    
    await handler.publish_message(email_data)

asyncio.run(main())