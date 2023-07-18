#!/usr/bin/env python3
""" List all documents in a collection """

from pymongo.collection import Collection
from typing import List


def list_all(mongo_collection: Collection) -> List[dict]:
    """
    List all documents in a MongoDB collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
        The pymongo collection object.

    Returns:
        list: A list containing all the documents in the collection.
    """
    documents = list(mongo_collection.find({}))
    return documents
