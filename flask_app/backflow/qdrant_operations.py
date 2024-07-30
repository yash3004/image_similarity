from datasets import load_dataset_builder, load_dataset
from sentence_transformers import SentenceTransformer

from . import q_client
import logging
import image_processor

import os

_logger = logging.getLogger('qdrant_operations')


def add_image_qdrant(path: str):
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


