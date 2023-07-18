#!/usr/bin/env python3
"""Returns all students sorted by average score."""


from pymongo.collection import Collection


def calculate_average_score(topics):
    """Calculate the average score of a student based on their topics.

    Args:
        topics (list): The list of topics with scores.

    Returns:
        float: The average score of the student.
    """
    total_score = sum(topic.get('score', 0) for topic in topics)
    return total_score / len(topics) if len(topics) > 0 else 0


def top_students(mongo_collection: Collection):
    """Returns all students sorted by average score.

    Args:
        mongo_collection (pymongo.collection.Collection):
            The pymongo collection object containing student records.

    Returns:
        list: A list of students sorted by average score in descending order.
    """
    students = mongo_collection.find({})
    return sorted(students, key=lambda student: calculate_average_score(student['topics']), reverse=True)


# The code below is for testing the function. Comment it out when running as a script.

if __name__ == "__main__":
    from pymongo import MongoClient
    list_all = __import__('8-all').list_all
    insert_school = __import__('9-insert_school').insert_school

    client = MongoClient('mongodb://127.0.0.1:27017')
    students_collection = client.my_db.students

    j_students = [
        {'name': "John", 'topics': [{'title': "Algo", 'score': 10.3}, {'title': "C", 'score': 6.2},
                                    {'title': "Python", 'score': 12.1}]},
        {'name': "Bob", 'topics': [{'title': "Algo", 'score': 5.4}, {'title': "C", 'score': 4.9},
                                   {'title': "Python", 'score': 7.9}]},
        {'name': "Sonia", 'topics': [{'title': "Algo", 'score': 14.8}, {'title': "C", 'score': 8.8},
                                     {'title': "Python", 'score': 15.7}]},
        {'name': "Amy", 'topics': [{'title': "Algo", 'score': 9.1}, {'title': "C", 'score': 14.2},
                                   {'title': "Python", 'score': 4.8}]},
        {'name': "Julia", 'topics': [{'title': "Algo", 'score': 10.5}, {'title': "C", 'score': 10.2},
                                     {'title': "Python", 'score': 10.1}]}
    ]
    for j_student in j_students:
        insert_school(students_collection, **j_student)

    students = list_all(students_collection)
    for student in students:
        print("[{}] {} - {}".format(student.get('_id'), student.get('name'), student.get('topics')))

    top_students = top_students(students_collection)
    for student in top_students:
        print("[{}] {} => {}".format(student.get('_id'), student.get('name'), student.get('averageScore')))
