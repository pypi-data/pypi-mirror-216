import asyncio
# from src.tcare_sbvalidator import sb_validator
from tcare_sbvalidator.handlers import Sms

from dotenv import dotenv_values
config = dotenv_values(".env")

NAMESPACE = config['NAMESPACELOCAL']
CONNECTION_STRING = config['CONNECTION_STRING']
SMSTOPIC = config['SMSTOPIC']

async def main():
    handler = Sms()

    json = handler.build_json(
        id="123",
        recipient="+15713024423",
        sender="+18722782273",
        content="Helloo!"
    )

    await handler.publish_message(NAMESPACE, SMSTOPIC, json)

asyncio.run(main())