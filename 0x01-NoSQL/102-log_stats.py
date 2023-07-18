#!/usr/bin/env python3
""" Provides some stats about Nginx logs stored in MongoDB """

from pymongo import MongoClient
from pymongo.collection import Collection


def count_documents(mongo_collection, query={}):
    """ Count the number of documents in a collection that
    match the given query.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The pymongo collection object.
        query (dict):
            The query filter to count documents (default is an
            empty dictionary).

    Returns:
        int: The number of documents that match the given query.
    """
    return mongo_collection.count_documents(query)


def count_method(mongo_collection, method):
    """ Count the number of documents with a specific method
    in the collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The pymongo collection object.
        method (str):
            The method to filter the documents.

    Returns:
        int: The number of documents that have the specified method.
    """
    return mongo_collection.count_documents({"method": method})


def print_stats(mongo_collection):
    """ Print various statistics about Nginx logs in the collection.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The pymongo collection object.
    """
    total_logs = count_documents(mongo_collection)
    print(f"{total_logs} logs")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = count_method(mongo_collection, method)
        print(f"method {method}: {count}")

    status_check = count_documents(
        mongo_collection, {"method": "GET", "path": "/status"})
    print(f"{status_check} status check")

    ip_pipeline = [{"$group": {"_id": "$ip", "count": {"$sum": 1}}},
                   {"$sort": {"count": -1}},
                   {"$limit": 10}]
    top_ips = list(mongo_collection.aggregate(ip_pipeline))
    print("IPs:")
    for ip in top_ips:
        print(f"    {ip['_id']}: {ip['count']}")


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs.nginx

    print_stats(logs_collection)
