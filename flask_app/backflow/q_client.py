import extensions
import os
from flask import config, Flask
from qdrant_client import QdrantClient, models


def get_client():
    qdrant_config = config.get('qdrant')
    q_client = QdrantClient(host=qdrant_config.get('host'), port=qdrant_config.get('port'),
                            api_key=qdrant_config.get('api_key'))
    return q_client


def create_collection(collection_name: str, client: QdrantClient):
    collection_config = models.VectorParams(size=512,
                                            distance=models.Distance.COSINE)
    new_collection = client.create_collection(collection_name=collection_name,
                                              vectors_config={'image': collection_config})

    return new_collection


def close_connection(client: QdrantClient):
    if client is not None:
        client.close()


def init_client(app: Flask, client: QdrantClient):
    app.teardown_request(close_connection(client))
