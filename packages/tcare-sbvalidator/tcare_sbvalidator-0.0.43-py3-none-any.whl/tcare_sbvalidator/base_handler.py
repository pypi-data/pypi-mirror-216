import json
from uuid import uuid4
from datetime import datetime
from azure.identity.aio import DefaultAzureCredential
from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage, TransportType
from azure.servicebus.exceptions import ServiceBusAuthenticationError
from .models.tcare_cloud_event import TcareCloudEvent


def cleanupCred(func):
    async def wrapper(*args, **kwargs):
        await func(*args, **kwargs)
        if args[0].cred:
            await args[0].cred.close()
    return wrapper

class BaseHandler:
    client = None
    cred = None
    messageSchema = None
    
    def validate_json(self, message):
        if not self.messageSchema:
            raise Exception("A class inheriting from BaseHandler is trying to validate without a messageSchema property.")
        parsed_json = json.loads(message)
        return self.messageSchema(**parsed_json)

    def connectWithCred(self, namespace):
        if self.client == None:
            self.cred = DefaultAzureCredential()
            self.client = ServiceBusClient(
                namespace,
                self.cred,
                transport_type=TransportType.AmqpOverWebsocket
            )

    def connectWithString(self, connection_string):
        print("attempting to connect with connection string")
        if self.client == None:
            self.client = ServiceBusClient.from_connection_string(
                connection_string,
                transport_type=TransportType.AmqpOverWebsocket
            )
    
    @cleanupCred
    async def publish_message(self, dynamic_data):
      
      model = self.messageSchema
      
      async with self.client:
        try:
          async with self.client.get_topic_sender(self.topic) as sender:
            
            sb_message = model(
              specversion="1.0.0",
              type="servicebusevent",
              id=str(uuid4()),
              time=datetime.now(),
              datacontenttype="application/json",
              data=dynamic_data,
            )
            
            if not model.validate(sb_message):
              raise Exception(f"Invalid {model.__name__} message")
            
            json_message = sb_message.json()
            msg = ServiceBusMessage(json_message)
            await sender.send_messages(msg)
            print(f"message sent with content: {json_message}")
                  
        except ServiceBusAuthenticationError as e:
          print(e)
          print(f"Make sure that {self.topic} is a valid topic.")
          
        except Exception as e:
          print(f"There was a problem publishing message: {e}")