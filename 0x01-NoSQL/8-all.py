def list_all(mongo_collection):
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
