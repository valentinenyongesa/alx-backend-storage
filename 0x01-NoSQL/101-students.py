#!/usr/bin/env python3

"""
Module Name: top_students
Description: Contains a function to retrieve all students sorted by average score.
"""

from pymongo import MongoClient


def top_students(mongo_collection):
    """
    Retrieve all students sorted by average score.

    Args:
    - mongo_collection: pymongo collection object
    representing the collection of students

    Returns:
    List of students sorted by average score, where
    each student document includes the average score.
    """
    students = mongo_collection.find()

    # Calculate average score for each student
    for student in students:
        total_score = sum(topic['score'] for topic in student['topics'])
        average_score = total_score / len(student['topics'])
        student['averageScore'] = average_score

    # Sort students by average score in descending order
    sorted_students = sorted(students, key=lambda x: x['averageScore'], reverse=True)

    return sorted_students


if __name__ == "__main__":
    # Example usage:
    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    # Your test data and function call here
