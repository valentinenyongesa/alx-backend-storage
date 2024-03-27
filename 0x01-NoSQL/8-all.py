#!/usr/bin/env python3

"""List all documents in Python"""


def list_all(mongo_collection):
    # Retrieve all documents from the collection
    documents = list(mongo_collection.find())

    # Return an empty list if no documents are found
    return documents if documents else []

# Example usage:


if __name__ == "__main__":
    from pymongo import MongoClient

    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {}".format(school.get('_id'), school.get('name')))
