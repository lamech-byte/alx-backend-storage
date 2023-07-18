#!/usr/bin/env python3
"""
Provides statistics about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def count_logs(collection):
    """
    Count the number of logs in the collection.

    Args:
        collection: The pymongo collection object.

    Returns:
        int: The number of documents in the collection.
    """
    return collection.count_documents({})


def count_by_method(collection, method):
    """
    Count the number of logs with a specific method in the collection.

    Args:
        collection: The pymongo collection object.
        method (str): The method to search for.

    Returns:
        int: The number of documents with the specified method.
    """
    return collection.count_documents({"method": method})


def count_status_check(collection, method, path):
    """
    Count the number of logs with a specific method and path in the collection.

    Args:
        collection: The pymongo collection object.
        method (str): The method to search for.
        path (str): The path to search for.

    Returns:
        int: The number of documents with the specified method and path.
    """
    return collection.count_documents({"method": method, "path": path})


def log_stats():
    """
    Provides statistics about Nginx logs stored in MongoDB.
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    total_logs = count_logs(collection)
    print(f"{total_logs} logs")

    print("Methods:")
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = count_by_method(collection, method)
        print(f"\tmethod {method}: {count}")

    status_check_count = count_status_check(collection, "GET", "/status")
    print(f"{status_check_count} status check")


if __name__ == "__main__":
    log_stats()
