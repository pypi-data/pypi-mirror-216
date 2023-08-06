from azure.data.tables import TableServiceClient
from azure.core.exceptions import ResourceExistsError
from azure.core.credentials import AzureNamedKeyCredential
from azure.data.tables import TableTransactionError
from azure.core.exceptions import ResourceNotFoundError
from django.conf import settings
from django_utils.logger_app import get_logger


class AzureTableStorage:
    def __init__(self):
        self.logger = get_logger('AzureTableStorage')
        endpoint = f'https://{settings.AZURE_STORAGE_ACCOUNT}.table.core.windows.net'

        if settings.USE_AZURITE:
            endpoint = settings.AZURITE_CONNECTION_STRING

        credential = AzureNamedKeyCredential(name=settings.AZURE_STORAGE_ACCOUNT,key=settings.AZURE_ACCOUNT_KEY)
        self.table_service = TableServiceClient(endpoint, credential=credential)
        
        try:
            self.table_service.create_table(settings.TABLE_STORAGE)
        except ResourceExistsError:
            self.logger.info('Table existing in the database.')
        
        self.table_client = self.table_service.get_table_client(settings.TABLE_STORAGE)


    def get_entity_by_row_key(self, partition_key,row_key):
        try:
            return self.table_client.get_entity(partition_key, row_key)
        except ResourceNotFoundError:
            return None

    def query_entities(self, **kwargs):
        try:
            entities = self.table_client.query_entities(**kwargs)
            return entities
        except TableTransactionError as error:
            self.logger.error(f'Error when trying to search entity: {error}')
            return None
    def insert_entity(self, entity):
        try:
            return self.table_client.create_entity(entity=entity)
        except TableTransactionError as error:
            self.logger.error(f'Error when trying to insert entity: {error}')            

    def insert_or_replace_entity(self, entity):
        try:
            self.table_client.upsert_entity(mode='replace', entity=entity)
        except TableTransactionError as error:
            self.logger.error(f'Error when trying to update entity: {error}')            

    def update_entity(self, entity):
        try:
            self.table_client.update_entity(mode='merge', entity=entity)
        except TableTransactionError as error:
            self.logger.error(f'Error when trying to update entity: {error}')            

    def delete_entity(self, partition_key, row_key):
        try:
            self.table_client.delete_entity(partition_key, row_key)
        except TableTransactionError as error:
            self.logger.error(f'Error when trying to delete entity: {error}')            
            
class FilterBuilder:
    def __init__(self, partition_key):
        self.partition_key = partition_key
        self.filters = []

    def add_filter(self, field, operator, value):
        if value is not None:
            if isinstance(value, str):
                value = f"'{value}'"
            self.filters.append(f"{field} {operator} {value}")
        return self

    def build(self):
        filter_str = " and ".join(self.filters)
        return f"PartitionKey eq '{self.partition_key}' and {filter_str}" if filter_str else f"PartitionKey eq '{self.partition_key}'"