#!/usr/bin/env python3

"""
Module Name: 12-log_stats
Description: Provides some stats about Nginx logs stored in MongoDB.
"""

from pymongo import MongoClient


def log_stats():
    """
    Retrieve statistics about Nginx logs stored in MongoDB.

    Prints:
    - Number of documents in the collection
    - Number of documents with each HTTP method
    - Number of documents with method=GET and path=/status
    """
    # Connect to MongoDB
    client = MongoClient('mongodb://127.0.0.1:27017')
    db = client.logs
    collection = db.nginx

    # Count total number of documents
    total_logs = collection.count_documents({})

    print("{} logs".format(total_logs))

    # Count number of documents with each HTTP method
    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in http_methods:
        count = collection.count_documents({"method": method})
        print("    method {}: {}".format(method, count))

    # Count number of documents with method=GET and path=/status
    status_check_count = collection.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status_check_count))


if __name__ == "__main__":
    log_stats()
