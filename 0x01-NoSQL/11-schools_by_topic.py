#!/usr/bin/env python3

"""
Module Name: 11-schools_by_topic
Description: Contains a function to
retrieve schools based on a specific topic.
"""

from pymongo import MongoClient


def schools_by_topic(mongo_collection, topic):
    """
    Retrieve the list of schools that have a specific topic

    Args:
    - mongo_collection: pymongo collection object
    representing the collection of schools
    - topic: string representing the topic to search

    Returns:
    List of schools that have the specified topic.
    """
    schools = mongo_collection.find({"topics": topic})
    return list(schools)


if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    school_collection = client.my_db.school

    j_schools = [
        { 'name': "Holberton school", 'topics': ["Algo", "C", "Python", "React"]},
        { 'name': "UCSF", 'topics': ["Algo", "MongoDB"]},
        { 'name': "UCLA", 'topics': ["C", "Python"]},
        { 'name': "UCSD", 'topics': ["Cassandra"]},
        { 'name': "Stanford", 'topics': ["C", "React", "Javascript"]}
    ]
    for j_school in j_schools:
        insert_school(school_collection, **j_school)

    schools = schools_by_topic(school_collection, "Python")
    for school in schools:
        print("[{}] {} {}".format(school.get('_id'),
              school.get('name'), school.get('topics', "")))
