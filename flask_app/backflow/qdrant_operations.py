import qdrant_client
from datasets import load_dataset_builder, load_dataset
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import uuid
from qdrant_client.http.models import PointStruct
from triton.language import pointer_type

from image_processor import pil_image_to_base64
from . import q_client
import logging
import image_processor
import os

_logger = logging.getLogger('qdrant_operations')


def get_embeddings(path: str):
    new_path = f"{path}_new"
    os.mkdir(path=new_path)
    try:
        image_processor.convert_bulk(path, new_path)
    except OSError as err:
        _logger.error(f"error while converting image occurred {err}")

    data = load_dataset(new_path, split="train")
    images = data['image']
    model = SentenceTransformer('clip-Vit-B-32')
    image_embeddings = model.encode([image for image in images])
    return image_embeddings, images


def save_to_collection(img_path: str, collection_name: str, client: qdrant_client.QdrantClient):
    image_embeddings, images = get_embeddings(img_path)
    points = []
    for embedding, image in tqdm(zip(image_embeddings, images)):
        payload = {"base64_image": pil_image_to_base64(image)}
        embeddings = embedding.toList()
        point_id = str(uuid.uuid4())
        points.append(PointStruct(id=point_id, payload=payload, vector={"image": embeddings}))

    batch_size = 100
    for i in tqdm(range(0, len(points), batch_size)):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=collection_name,
            wait=True,
            points=batch
        )
