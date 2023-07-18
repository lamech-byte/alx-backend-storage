#!/usr/bin/env python3
""" Insert a new document in a collection based on kwargs """

from pymongo.collection import Collection


def insert_school(mongo_collection: Collection, **kwargs) -> str:
    """
    Insert a new document in a MongoDB collection based on kwargs.

    Args:
        mongo_collection (pymongo.collection.Collection): The pymongo collection object.
        **kwargs: Keyword arguments representing the document to be inserted.

    Returns:
        str: The _id of the newly inserted document.
    """
    new_school_id = mongo_collection.insert_one(kwargs).inserted_id
    return str(new_school_id)
