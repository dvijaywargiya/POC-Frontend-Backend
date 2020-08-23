from azure.cosmos import exceptions, CosmosClient, PartitionKey

endpoint = "https://devesh-db.documents.azure.com:443/"
key = 'aRR0Ygc9E96R5QhHvFq6l7gEVaNxeANdC2cXel1YtRZahlmMEB6fXi6txUi0ZGBwgSttabN2FMAFiqkIv0MPNw=='

client = CosmosClient(endpoint, key)

database_name = 'Data'
database = client.create_database_if_not_exists(id=database_name)

container_name = 'Users'
container_users = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

container_name = 'UserMetrics'
container_userMetrics = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

container_name = 'Datasets'
container_datasets = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

container_name = 'Requests'
container_requests = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)

container_name = 'Jobs'
container_jobs = database.create_container_if_not_exists(
    id=container_name, 
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400
)