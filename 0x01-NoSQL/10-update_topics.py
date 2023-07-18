#!/usr/bin/env python3
""" Change all topics of a school document based on the name """

from pymongo.collection import Collection
from typing import List


def update_topics(mongo_collection, name, topics):
    """
    Change all topics of a school document based on the name.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The pymongo collection object.
        name (str): The school name to update.
        topics (List[str]): The list of topics approached in the school.
    """
    mongo_collection.update_many({ "name": name }, { "$set": { "topics": topics } })
