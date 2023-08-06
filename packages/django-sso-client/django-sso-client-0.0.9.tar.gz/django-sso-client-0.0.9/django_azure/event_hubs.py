from django.conf import settings
from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.aio._eventprocessor.partition_context import PartitionContext
from azure.eventhub.extensions.checkpointstoreblobaio import (
    BlobCheckpointStore,
)
import json


EVENT_HUB_NAME = settings.EVENT_HUB_NAME
EVENT_HUB_CONNECTION_STR = settings.EVENT_HUB_CONNECTION_STR
BLOB_STORAGE_CONNECTION_STRING = settings.BLOB_STORAGE_CONNECTION_STRING
BLOB_CONTAINER_NAME = settings.BLOB_CONTAINER_NAME

async def producer(data
                   ,eventhub_name = EVENT_HUB_NAME
                   ,eventhub_conn_str=EVENT_HUB_CONNECTION_STR):
    """
    Função que retorna a soma de dois números.

    Args:
        data (any): O primeiro número.
        eventhub_name(str): O segundo número.
        eventhub_conn_str (str) : terceiro elemento

    Returns:
        None
    """

    producer = EventHubProducerClient.from_connection_string(
        conn_str=eventhub_conn_str,
        eventhub_name=eventhub_name
    )

    async with producer:
        event_data_batch = await producer.create_batch()

        event = EventData(json.dumps(data))
        event.body_as_json(encoding='UTF-8')
        event_data_batch.add(event)
       
        await producer.send_batch(event_data_batch)

'''
async def on_event(partition_context:PartitionContext
                   , event:EventData):
   
    print(
        'Received the event: "{}" from the partition with ID: "{}"'.format(
            event.body_as_json(encoding="UTF-8"), partition_context.partition_id
        )
    )

    await partition_context.update_checkpoint(event)
'''

async def consumer(eventhub_name = EVENT_HUB_NAME
              ,eventhub_conn_str=EVENT_HUB_CONNECTION_STR
              ,blob_conn_str=BLOB_STORAGE_CONNECTION_STRING
              ,blob_name=BLOB_CONTAINER_NAME
              ,consumer_group='$Default'
              ,on_event=None):
    
    checkpoint_store = BlobCheckpointStore.from_connection_string(
        blob_conn_str, blob_name
    )

    client = EventHubConsumerClient.from_connection_string(
        eventhub_conn_str,
        consumer_group=consumer_group,
        eventhub_name=eventhub_name,
        retry_total=5,
        checkpoint_store=checkpoint_store
    )

    async with client:
       await client.receive(on_event=on_event)
        
