#!/usr/bin/env python3
""" Return the list of schools having a specific topic """

from pymongo.collection import Collection
from typing import List


def schools_by_topic(mongo_collection: Collection, topic: str) -> List[dict]:
    """
    Return the list of schools having a specific topic.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The pymongo collection object.
        topic (str): The topic to search for.

    Returns:
        List[dict]: A list of schools that have the specified topic.
    """
    return list(mongo_collection.find({"topics": topic}))
