import extensions
import os
import qdrant_client

app_config = extensions.resolve_configuration()


def get_client():
    qdrant_config = app_config.get('qdrant')
    q_client = qdrant_client.QdrantClient(host=qdrant_config.get('host'), port=qdrant_config.get('port'),
                                          api_key=qdrant_config.get('api_key'))
    return q_client


def create_collection(collection_name: str):
    client: qdrant_client.QdrantClient = get_client()
    new_collection = client.create_collection(collection_name=collection_name)
    return new_collection


