#!/usr/bin/env python3

"""change school topucs"""


def update_topics(mongo_collection, name, topics):
    # Update the topics of the school document based on the given name
    result = mongo_collection.update_one({"name": name},
                                         {"$set": {"topics": topics}})

    # Return True if the document was successfully updated, False otherwise
    return result.modified_count > 0

# Example usage:


if __name__ == "__main__":
    from pymongo import MongoClient
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    update_topics(school_collection, "Holberton school",
                  ["Sys admin", "AI", "Algorithm"])

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
              school.get('name'), school.get('topics', "")))

    update_topics(school_collection, "Holberton school", ["iOS"])

    schools = list_all(school_collection)
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
              school.get('name'), school.get('topics', "")))
