# Import Useful Libraries
from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from datetime import datetime, timedelta
import pandas as pd
from bson import json_util
import json
import time
from pymongo.errors import OperationFailure, DuplicateKeyError
from pprint import pprint

# Establish connection
client = MongoClient('mongodb://localhost:27017/')
db = client['eduhub_db']

def create_collections_with_validation():
   
    # List of all collections with their validation schemas
    collections = {
        "users": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ["userId", "email", "firstName", "lastName", "role", "dateJoined", "isActive"],
                "properties": {
                    "userId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "email": {
                        "bsonType": "string",
                        "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                        "description": "must be a valid email and is required"
                    },
                    "firstName": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "lastName": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "role": {
                        "enum": ["student", "instructor"],
                        "description": "must be either 'student' or 'instructor' and is required"
                    },
                    "dateJoined": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "profile": {
                        "bsonType": "object",
                        "properties": {
                            "bio": {"bsonType": "string"},
                            "avatar": {"bsonType": "string"},
                            "skills": {
                                "bsonType": "array",
                                "items": {"bsonType": "string"}
                            }
                        }
                    },
                    "isActive": {
                        "bsonType": "bool",
                        "description": "must be a boolean"
                    }
                }
            }
        },

        "courses": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['courseId', 'title', 'description', 'instructorId', 'category', 
                     'level', 'duration', 'price', 'createdAt', 'isPublished'],
                "properties": {
                    "courseId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "title": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "description": {"bsonType": "string"},
                    "instructorId": {
                        "bsonType": "string",
                        "description": "must reference a user and is required"
                    },
                    "category": {"bsonType": "string"},
                    "level": {
                        "enum": ["beginner", "intermediate", "advanced"],
                        "description": "must be one of the defined levels"
                    },
                    "duration": {
                        "bsonType": "number",
                        "minimum": 0,
                        "description": "must be a positive number"
                    },
                    "price": {
                        "bsonType": "number",
                        "minimum": 0,
                        "description": "must be a positive number"
                    },
                    "tags": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    },
                    "createdAt": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "updatedAt": {"bsonType": "date"},
                    "isPublished": {"bsonType": "bool"}
                }
            }
        },

        "enrollments": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['enrollmentId', 'studentId', 'courseId', 'enrollmentDate', 
                    'completionStatus', 'lastAccessed'],
                "properties": {
                    "enrollmentId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "studentId": {
                        "bsonType": "string",
                        "description": "must reference a user and is required"
                    },
                    "courseId": {
                        "bsonType": "string",
                        "description": "must reference a course and is required"
                    },
                    "enrollmentDate": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "completionStatus": {
                        "bsonType": "number",
                        "minimum": 0,
                        "maximum": 100,
                        "description": "must be a percentage between 0 and 100"
                    },
                    "lastAccessed": {"bsonType": "date"}
                }
            }
        },
        
        "lessons": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['lessonId', 'courseId', 'title', 'content', 'sequence', 'duration'],
                "properties": {
                    "lessonId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "courseId": {
                        "bsonType": "string",
                        "description": "must reference a course and is required"
                    },
                    "title": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "content": {"bsonType": "string"},
                    "sequence": {
                        "bsonType": "number",
                        "minimum": 1,
                        "description": "must be a positive integer and is required"
                    },
                    "duration": {
                        "bsonType": "number",
                        "minimum": 0,
                        "description": "must be a positive number"
                    },
                    "resources": {
                        "bsonType": "array",
                        "items": {"bsonType": "string"}
                    }
                }
            }
        },

        "assignments": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['assignmentId', 'courseId', 'title', 'description', 'dueDate', 'maxPoints', 'instructions'],
                "properties": {
                    "assignmentId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "courseId": {
                        "bsonType": "string",
                        "description": "must reference a course and is required"
                    },
                    "title": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "description": {"bsonType": "string"},
                    "dueDate": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "maxPoints": {
                        "bsonType": "number",
                        "minimum": 0,
                        "description": "must be a positive number"
                    },
                    "instructions": {"bsonType": "string"}
                }
            }
        },

        "submissions": {
            "$jsonSchema": {
                "bsonType": "object",
                "required": ['submissionId', 'assignmentId', 'studentId', 'submittedDate', 'content', 'isGraded'],
                "properties": {
                    "submissionId": {
                        "bsonType": "string",
                        "description": "must be a string and is required"
                    },
                    "assignmentId": {
                        "bsonType": "string",
                        "description": "must reference an assignment and is required"
                    },
                    "studentId": {
                        "bsonType": "string",
                        "description": "must reference a user and is required"
                    },
                    "submittedDate": {
                        "bsonType": "date",
                        "description": "must be a date and is required"
                    },
                    "content": {"bsonType": "string"},
                    "grade": {
                        "bsonType": "number",
                        "minimum": 0,
                        "description": "must be a positive number"
                    },
                    "feedback": {"bsonType": "string"},
                    "isGraded": {"bsonType": "bool"}
                }
            }
        },
    }

    # Get list of existing collections
    existing_collections = db.list_collection_names()
    
    # Create each collection if it doesn't exist
    for collection_name, validator in collections.items():
        if collection_name not in existing_collections:
            db.create_collection(collection_name, validator=validator)
            print(f"Collection '{collection_name}' created with validation rules.")
        else:
            print(f"Collection '{collection_name}' already exists. Skipping creation.")

# Execute the function to create collections
# create_collections_with_validation()

# Document Schema Example
def list_document_schema_example():
        # Create sample documents from the sample_data.json file
    with open("C:/Users/USER/Desktop/mongodb-eduhub-project/data/sample_data.json") as f:
        sample_data = json.load(f)

    users_sample_document = sample_data.get("users", [])
    courses_sample_document = sample_data.get("courses", [])
    enrollments_sample_document = sample_data.get("enrollments", [])
    lessons_sample_document = sample_data.get("lessons", [])
    assignments_sample_document = sample_data.get("assignments", [])
    submissions_sample_document = sample_data.get("submissions", [])

    # Print the first elements of each sample data
    print(f"Users Sample Document: {json.dumps(users_sample_document[0], indent=4)}")
    print("  ")
    print(f"Courses Sample Document: {json.dumps(courses_sample_document[0], indent=4)}")
    print("  ")
    print(f"Enrollments Sample Document: {json.dumps(enrollments_sample_document[0], indent=4)}")
    print("  ")
    print(f"Lessons Sample Document: {json.dumps(lessons_sample_document[0], indent=4)}")
    print("  ")
    print(f"Assignments Sample Document: {json.dumps(assignments_sample_document[0], indent=4)}")
    print("  ")
    print(f"Submissions Sample Document: {json.dumps(submissions_sample_document[0], indent=4)}")


def load_data_to_collections(json_file_path):
    
    # Load JSON data
    with open(json_file_path) as file:
        data = json.load(file)
    
    # Date fields for each collection
    date_fields = {
        'users': ['dateJoined'],
        'courses': ['createdAt', 'updatedAt'],
        'enrollments': ['enrollmentDate', 'lastAccessed'],
        'assignments': ['dueDate'],
        'submissions': ['submittedDate']
    }
    
    # Convert date strings to datetime objects
    def convert_dates(document, fields):
        for field in fields:
            if field in document and document[field]:
                document[field] = datetime.strptime(document[field], "%Y-%m-%dT%H:%M:%SZ")
        return document
    
    # Load data into each collection
    for collection_name in ['users', 'courses', 'enrollments', 'lessons', 'assignments', 'submissions']:
        if collection_name in data:
            collection = db[collection_name]
            
            # Convert dates for documents in this collection
            documents = data[collection_name]
            if collection_name in date_fields:
                documents = [convert_dates(doc, date_fields[collection_name]) for doc in documents]
            
            # Insert documents
            if documents:  # Only insert if there are documents
                result = collection.insert_many(documents)
                print(f"Inserted {len(result.inserted_ids)} documents into {collection_name} collection")
    
    print("Data loading completed!")

# Usage example:
# load_data_to_collections('C:/Users/USER/Desktop/mongodb-eduhub-project/data/sample_data.json')


def add_new_student(db):
    """
    Adds a new student user to the database.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        None
    """
    new_student = {
        "userId": "user021",
        "email": "new.student@example.com",
        "firstName": "New",
        "lastName": "Student",
        "role": "student",
        "dateJoined": datetime.now(),
        "profile": {
            "bio": "New computer science student",
            "skills": ["Python", "SQL"]
        },
        "isActive": True
    }

    student_result = db.users.insert_one(new_student)
    print(f"1. Added new student (ID: {student_result.inserted_id}):")
    print(f"   - Name: {new_student['firstName']} {new_student['lastName']}")
    print(f"   - Email: {new_student['email']}\n")

def create_new_course(db):
    """
    Creates a new course in the database.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        None
    """
    new_course = {
        "courseId": "course009",
        "title": "Advanced Data Analysis",
        "description": "Master data analysis techniques with Python and Pandas",
        "instructorId": "user012",  # Nneka Onyemaobi (ML specialist)
        "category": "Data Science",
        "level": "advanced",
        "duration": 35,
        "price": 229.99,
        "tags": ["data analysis", "python", "pandas"],
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
        "isPublished": True
    }

    course_result = db.courses.insert_one(new_course)
    print(f"2. Created new course (ID: {course_result.inserted_id}):")
    print(f"   - Title: {new_course['title']}")
    print(f"   - Instructor ID: {new_course['instructorId']}")
    print(f"   - Price: ${new_course['price']}\n")

def enroll_student_in_course(db):
    """
    Enrolls a student in a course by creating an enrollment record.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        None
    """
    new_enrollment = {
        "enrollmentId": "enroll017",
        "studentId": "user021",  # Our new student
        "courseId": "course009",  # Our new course
        "enrollmentDate": datetime.now(),
        "completionStatus": 0,
        "lastAccessed": datetime.now()
    }

    enrollment_result = db.enrollments.insert_one(new_enrollment)
    print(f"3. Created new enrollment (ID: {enrollment_result.inserted_id}):")
    print(f"   - Student: {new_enrollment['studentId']}")
    print(f"   - Course: {new_enrollment['courseId']}")
    print(f"   - Status: {new_enrollment['completionStatus']}% complete\n")

def add_lesson_to_course(db):
    """
    Adds a new lesson to an existing course in the database.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        None
    """
    new_lesson = {
        "lessonId": "lesson026",
        "courseId": "course009",  # Our new course
        "title": "Pandas Advanced Features",
        "content": "Master multi-indexing, groupby operations, and performance optimization",
        "sequence": 1,
        "duration": 90,
        "resources": ["https://example.com/pandas-advanced"]
    }

    lesson_result = db.lessons.insert_one(new_lesson)
    print(f"4. Added new lesson (ID: {lesson_result.inserted_id}):")
    print(f"   - Course: {new_lesson['courseId']}")
    print(f"   - Title: {new_lesson['title']}")
    print(f"   - Duration: {new_lesson['duration']} minutes")

def verify_database_counts(db):
    """
    Verifies and prints the total counts of documents in each collection.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        None
    """
    print("\n=== Verification ===")
    print(f"Total users: {db.users.count_documents({})}")
    print(f"Total courses: {db.courses.count_documents({})}")
    print(f"Total enrollments: {db.enrollments.count_documents({})}")
    print(f"Total lessons: {db.lessons.count_documents({})}")

# Example usage:
# add_new_student(db)
# create_new_course(db)
# enroll_student_in_course(db)
# add_lesson_to_course(db)
# verify_database_counts(db)


def find_active_students(db):
    """
    Finds and displays all active student users in the system.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        list: All active student documents with selected fields
    """
    active_students = list(db.users.find({
        "role": "student",
        "isActive": True
    }, {"userId": 1, "firstName": 1, "lastName": 1, "email": 1}))

    print("1. Active Students (Total:", len(active_students), "):")
    for student in active_students[:3]:  # Display first 3 for brevity
        print(f"   - {student['firstName']} {student['lastName']} ({student['email']})")
    print("   ...\n")
    
    return active_students

def get_course_with_instructor(db, course_id="course001"):
    """
    Retrieves detailed course information including instructor details using aggregation.
    
    Args:
        db: MongoDB database connection object
        course_id: The ID of the course to look up (defaults to Python course)
        
    Returns:
        dict: Course document with embedded instructor information
    """
    course_with_instructor = list(db.courses.aggregate([
        {
            "$match": {"courseId": course_id}
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "instructorId",
                "foreignField": "userId",
                "as": "instructor"
            }
        },
        {
            "$unwind": "$instructor"
        },
        {
            "$project": {
                "title": 1,
                "description": 1,
                "level": 1,
                "instructorName": {"$concat": ["$instructor.firstName", " ", "$instructor.lastName"]},
                "instructorBio": "$instructor.profile.bio"
            }
        }
    ]))

    print("2. Course with Instructor Details:")
    if course_with_instructor:
        pprint(course_with_instructor[0])
    else:
        print("   No course found with ID:", course_id)
    print("\n")
    
    return course_with_instructor[0] if course_with_instructor else None

def get_courses_by_category(db, category="Data Science"):
    """
    Finds all courses in a specified category.
    
    Args:
        db: MongoDB database connection object
        category: The course category to filter by
        
    Returns:
        list: All courses in the specified category
    """
    courses = list(db.courses.find(
        {"category": category},
        {"title": 1, "level": 1, "price": 1}
    ))

    print(f"3. {category} Courses (Total:", len(courses), "):")
    for course in courses:
        print(f"   - {course['title']} ({course['level']}, ${course['price']})")
    print("\n")
    
    return courses

def get_students_in_course(db, course_id="course001"):
    """
    Retrieves all students enrolled in a specific course with their progress.
    
    Args:
        db: MongoDB database connection object
        course_id: The ID of the course to query
        
    Returns:
        list: Enrollment records with student information
    """
    students = list(db.enrollments.aggregate([
        {
            "$match": {"courseId": course_id}
        },
        {
            "$lookup": {
                "from": "users",
                "localField": "studentId",
                "foreignField": "userId",
                "as": "student"
            }
        },
        {
            "$unwind": "$student"
        },
        {
            "$project": {
                "studentName": {"$concat": ["$student.firstName", " ", "$student.lastName"]},
                "email": "$student.email",
                "completionStatus": 1
            }
        }
    ]))

    print(f"4. Students Enrolled in Course {course_id} (Total:", len(students), "):")
    for student in students[:3]:  # Display first 3
        print(f"   - {student['studentName']} ({student['email']}), Progress: {student['completionStatus']}%")
    print("   ...\n")
    
    return students

def search_courses_by_title(db, search_term="data"):
    """
    Performs a case-insensitive partial match search on course titles.
    
    Args:
        db: MongoDB database connection object
        search_term: The string to search for in course titles
        
    Returns:
        list: Courses matching the search term
    """
    matched_courses = list(db.courses.find(
        {"title": {"$regex": search_term, "$options": "i"}},
        {"title": 1, "category": 1}
    ))

    print(f"5. Courses matching '{search_term}' (Total:", len(matched_courses), "):")
    for course in matched_courses:
        print(f"   - {course['title']} ({course['category']})")
    
    return matched_courses

def print_verification_counts(db):
    """
    Prints verification counts for important collections and queries.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        None
    """
    print("\n=== Verification Counts ===")
    print("Total active students:", db.users.count_documents({"role": "student", "isActive": True}))
    print("Total Data Science courses:", db.courses.count_documents({"category": "Data Science"}))
    print("Total enrollments in Python course:", db.enrollments.count_documents({"courseId": "course001"}))

# Example usage:
# find_active_students(db)
# get_course_with_instructor(db)
# get_courses_by_category(db)
# get_students_in_course(db)
# search_courses_by_title(db)
# print_verification_counts(db)



def update_user_profile(db, user_id="user001", updates=None):
    """
    Updates a user's profile information with the specified changes.
    
    Args:
        db: MongoDB database connection object
        user_id: ID of the user to update (default: "user001")
        updates: Dictionary of fields to update (will be merged with default updates)
        
    Returns:
        tuple: (update_result, updated_user_document)
    """
    # Default updates (can be overridden or extended by passing updates parameter)
    default_updates = {
        "profile.bio": "Computer science graduate specializing in AI",
        "profile.skills": ["Python", "Java", "Machine Learning"],
        "lastName": "Adesanya-Jones"  # Married name change
    }
    
    # Merge with any provided updates
    final_updates = {**default_updates, **(updates or {})}
    
    # Perform the update
    update_result = db.users.update_one(
        {"userId": user_id},
        {"$set": final_updates}
    )

    # Verification
    updated_user = db.users.find_one({"userId": user_id})
    print("1. Updated User Profile:")
    print(f"   - Name: {updated_user['firstName']} {updated_user['lastName']}")
    print(f"   - New Bio: {updated_user['profile']['bio']}")
    print(f"   - Skills: {', '.join(updated_user['profile']['skills'])}")
    print(f"   - Documents modified: {update_result.modified_count}\n")
    
    return update_result, updated_user

def publish_course(db, course_id="course008"):
    """
    Marks a course as published and updates the timestamp.
    
    Args:
        db: MongoDB database connection object
        course_id: ID of the course to publish (default: "course008")
        
    Returns:
        tuple: (update_result, updated_course_document)
    """
    update_result = db.courses.update_one(
        {"courseId": course_id},
        {
            "$set": {
                "isPublished": True,
                "updatedAt": datetime.utcnow()
            }
        }
    )

    # Verification
    updated_course = db.courses.find_one({"courseId": course_id})
    print("2. Course Publishing Status:")
    print(f"   - Course: {updated_course['title']}")
    print(f"   - Published: {updated_course['isPublished']}")
    print(f"   - Last Updated: {updated_course['updatedAt']}")
    print(f"   - Documents modified: {update_result.modified_count}\n")
    
    return update_result, updated_course

def update_assignment_grade(db, submission_id="sub002", student_id="user001", grade=95, feedback=None):
    """
    Updates an assignment submission with a new grade and feedback.
    
    Args:
        db: MongoDB database connection object
        submission_id: ID of the submission (default: "sub002")
        student_id: ID of the student (default: "user001")
        grade: New grade to assign (default: 95)
        feedback: Feedback comments (defaults to preset message)
        
    Returns:
        tuple: (update_result, updated_submission_document)
    """
    if feedback is None:
        feedback = "Excellent work! Fixed all edge cases."

    update_result = db.submissions.update_one(
        {
            "submissionId": submission_id,
            "studentId": student_id
        },
        {
            "$set": {
                "grade": grade,
                "feedback": feedback,
                "isGraded": True
            }
        }
    )

    # Verification
    updated_submission = db.submissions.find_one({"submissionId": submission_id})
    print("3. Updated Assignment Grade:")
    print(f"   - Student: {updated_submission['studentId']}")
    print(f"   - New Grade: {updated_submission['grade']}/100")
    print(f"   - Feedback: {updated_submission['feedback']}")
    print(f"   - Documents modified: {update_result.modified_count}\n")
    
    return update_result, updated_submission

def add_course_tags(db, course_id="course005", new_tags=None):
    """
    Adds tags to an existing course without creating duplicates.
    
    Args:
        db: MongoDB database connection object
        course_id: ID of the course to update (default: "course005")
        new_tags: List of tags to add (defaults to ["deep learning", "neural networks"])
        
    Returns:
        tuple: (update_result, updated_course_document)
    """
    if new_tags is None:
        new_tags = ["deep learning", "neural networks"]

    update_result = db.courses.update_one(
        {"courseId": course_id},
        {
            "$addToSet": {  # Prevents duplicate tags
                "tags": {"$each": new_tags}
            },
            "$set": {
                "updatedAt": datetime.utcnow()
            }
        }
    )

    # Verification
    updated_course = db.courses.find_one({"courseId": course_id})
    print("4. Added Course Tags:")
    print(f"   - Course: {updated_course['title']}")
    print(f"   - Updated Tags: {', '.join(updated_course['tags'])}")
    print(f"   - Last Updated: {updated_course['updatedAt']}")
    print(f"   - Documents modified: {update_result.modified_count}")
    
    return update_result, updated_course

def verify_updates(db, *update_results):
    """
    Prints verification counts for all update operations performed.
    
    Args:
        db: MongoDB database connection object
        update_results: Variable number of update result objects
        
    Returns:
        None
    """
    print("\n=== Final Verification ===")
    for i, result in enumerate(update_results, 1):
        print(f"Operation {i} documents modified:", result.modified_count)

# Example usage:
# user_result, updated_user = update_user_profile(db)
# course_result, updated_course = publish_course(db)
# grade_result, updated_submission = update_assignment_grade(db)
# tags_result, updated_course = add_course_tags(db)
# verify_updates(db, user_result, course_result, grade_result, tags_result)


def soft_delete_user(db, user_id="user020"):
    """
    Performs a soft delete on a user by setting isActive to False.
    Maintains the user record while deactivating their account.
    
    Args:
        db: MongoDB database connection object
        user_id: ID of the user to soft delete (default: "user020")
        
    Returns:
        tuple: (update_result, deleted_user_document)
    """
    # Perform the soft delete update
    update_result = db.users.update_one(
        {"userId": user_id},
        {"$set": {"isActive": False}}
    )

    # Verification
    deleted_user = db.users.find_one({"userId": user_id})
    print("1. Soft Deleted User:")
    print(f"   - Name: {deleted_user['firstName']} {deleted_user['lastName']}")
    print(f"   - isActive Status: {deleted_user['isActive']}")
    print(f"   - Documents modified: {update_result.modified_count}")
    print(f"   - Active users count: {db.users.count_documents({'isActive': True, 'role': 'student'})}\n")
    
    return update_result, deleted_user

def delete_enrollment(db, enrollment_id="enroll016"):
    """
    Permanently deletes an enrollment record from the database.
    
    Args:
        db: MongoDB database connection object
        enrollment_id: ID of the enrollment to delete (default: "enroll016")
        
    Returns:
        tuple: (delete_result, remaining_enrollments_count)
    """
    # First get course ID for verification
    enrollment = db.enrollments.find_one({"enrollmentId": enrollment_id})
    course_id = enrollment["courseId"] if enrollment else None
    
    # Perform the deletion
    delete_result = db.enrollments.delete_one(
        {"enrollmentId": enrollment_id}
    )

    # Verification
    print("2. Deleted Enrollment:")
    print(f"   - Enrollment ID: {enrollment_id}")
    print(f"   - Documents deleted: {delete_result.deleted_count}")
    print(f"   - Remaining enrollments: {db.enrollments.count_documents({})}")
    
    if course_id:
        print(f"   - Course {course_id} enrollments: {db.enrollments.count_documents({'courseId': course_id})}")
    print()
    
    return delete_result, db.enrollments.count_documents({})

def remove_lesson(db, lesson_id="lesson025", course_id="course001"):
    """
    Removes a lesson from a course in the database.
    
    Args:
        db: MongoDB database connection object
        lesson_id: ID of the lesson to remove (default: "lesson025")
        course_id: ID of the course to remove from (default: "course001")
        
    Returns:
        tuple: (delete_result, remaining_lessons_count)
    """
    # Perform the deletion
    delete_result = db.lessons.delete_one(
        {
            "lessonId": lesson_id,
            "courseId": course_id
        }
    )

    # Verification
    print("3. Removed Lesson:")
    print(f"   - Lesson ID: {lesson_id}")
    print(f"   - Documents deleted: {delete_result.deleted_count}")
    print(f"   - Remaining lessons: {db.lessons.count_documents({})}")
    print(f"   - Lessons in course {course_id}: {db.lessons.count_documents({'courseId': course_id})}")
    
    return delete_result, db.lessons.count_documents({})

def verify_deletions(db, user_id="user020", enrollment_id="enroll016", lesson_id="lesson025"):
    """
    Performs comprehensive verification of deletion operations.
    
    Args:
        db: MongoDB database connection object
        user_id: ID of soft-deleted user to verify
        enrollment_id: ID of deleted enrollment to verify
        lesson_id: ID of removed lesson to verify
        
    Returns:
        dict: Verification results
    """
    verification_results = {
        "active_students": db.users.count_documents({'role': 'student', 'isActive': True}),
        "total_enrollments": db.enrollments.count_documents({}),
        "total_lessons": db.lessons.count_documents({}),
        "user_status": db.users.find_one({"userId": user_id}, {"isActive": 1}),
        "enrollment_exists": bool(db.enrollments.find_one({"enrollmentId": enrollment_id})),
        "lesson_exists": bool(db.lessons.find_one({"lessonId": lesson_id}))
    }

    print("\n=== Final Verification ===")
    print(f"Active students count: {verification_results['active_students']}")
    print(f"Total enrollments: {verification_results['total_enrollments']}")
    print(f"Total lessons: {verification_results['total_lessons']}")

    print("\n=== Detailed Verification ===")
    print(f"User {user_id} status:", verification_results['user_status'])
    print(f"Enrollment {enrollment_id} exists:", verification_results['enrollment_exists'])
    print(f"Lesson {lesson_id} exists:", verification_results['lesson_exists'])
    
    return verification_results

# Example usage:
# soft_delete_result, deleted_user = soft_delete_user(db)
# enrollment_delete_result, enrollments_count = delete_enrollment(db)
# lesson_delete_result, lessons_count = remove_lesson(db)
# verification = verify_deletions(db)



def find_courses_by_price_range(db, min_price=50, max_price=200):
    """
    Finds courses within a specified price range and sorts them by price.
    
    Args:
        db: MongoDB database connection object
        min_price: Minimum course price (default: 50)
        max_price: Maximum course price (default: 200)
        
    Returns:
        list: Courses matching the price range criteria
    """
    courses = list(db.courses.find(
        {
            "price": {
                "$gte": min_price,
                "$lte": max_price
            }
        },
        {
            "title": 1,
            "price": 1,
            "category": 1,
            "_id": 0
        }
    ).sort("price", 1))  # Sort by price ascending

    print(f"1. Courses between ${min_price}-${max_price} (Count:", len(courses), "):")
    for course in courses:
        print(f"   - {course['title']}: ${course['price']} ({course['category']})")
    print()
    
    return courses

def find_recent_students(db, months=6):
    """
    Finds students who joined within the specified number of months.
    
    Args:
        db: MongoDB database connection object
        months: Number of months to look back (default: 6)
        
    Returns:
        list: Recent student documents
    """
    cutoff_date = datetime.now() - timedelta(days=months*30)
    students = list(db.users.find(
        {
            "dateJoined": {"$gte": cutoff_date},
            "role": "student"
        },
        {
            "firstName": 1,
            "lastName": 1,
            "dateJoined": 1,
            "_id": 0
        }
    ).sort("dateJoined", -1))  # Newest first

    print(f"2. Students joined in last {months} months (Count:", len(students), "):")
    for student in students[:3]:  # Show first 3 for brevity
        join_date = student['dateJoined'].strftime("%Y-%m-%d")
        print(f"   - {student['firstName']} {student['lastName']} (Joined: {join_date})")
    print("   ...\n")
    
    return students

def find_courses_by_tags(db, tags=None):
    """
    Finds courses that have any of the specified tags.
    
    Args:
        db: MongoDB database connection object
        tags: List of tags to search for (default: ["python", "machine learning"])
        
    Returns:
        list: Courses matching at least one of the tags
    """
    if tags is None:
        tags = ["python", "machine learning"]
    
    courses = list(db.courses.find(
        {
            "tags": {"$in": tags}
        },
        {
            "title": 1,
            "tags": 1,
            "_id": 0
        }
    ))

    print(f"3. Courses with tags {tags} (Count:", len(courses), "):")
    for course in courses:
        matched_tags = [tag for tag in course['tags'] if tag in tags]
        print(f"   - {course['title']} (Tags: {', '.join(matched_tags)})")
    print()
    
    return courses

def find_upcoming_assignments(db, days=7):
    """
    Finds assignments with due dates within the specified number of days.
    
    Args:
        db: MongoDB database connection object
        days: Number of days to look ahead (default: 7)
        
    Returns:
        list: Upcoming assignment documents
    """
    today = datetime.now()
    end_date = today + timedelta(days=days)
    
    assignments = list(db.assignments.find(
        {
            "dueDate": {
                "$gte": today,
                "$lte": end_date
            }
        },
        {
            "title": 1,
            "courseId": 1,
            "dueDate": 1,
            "_id": 0
        }
    ).sort("dueDate", 1))  # Earliest first

    print(f"4. Assignments due in next {days} days (Count:", len(assignments), "):")
    for assignment in assignments:
        due_date = assignment['dueDate'].strftime("%Y-%m-%d")
        course = db.courses.find_one(
            {"courseId": assignment['courseId']},
            {"title": 1}
        )
        course_title = course['title'] if course else "Unknown Course"
        print(f"   - {assignment['title']} (Due: {due_date})")
        print(f"     Course: {course_title}")
    print()
    
    return assignments

def verify_query_results(db, price_courses=None, recent_students=None, 
                       tagged_courses=None, upcoming_assignments=None):
    """
    Verifies and prints counts of query results and sample documents.
    
    Args:
        db: MongoDB database connection object
        price_courses: Result from find_courses_by_price_range()
        recent_students: Result from find_recent_students()
        tagged_courses: Result from find_courses_by_tags()
        upcoming_assignments: Result from find_upcoming_assignments()
        
    Returns:
        dict: Verification results
    """
    verification = {
        "price_range_count": len(price_courses) if price_courses else 0,
        "recent_students_count": len(recent_students) if recent_students else 0,
        "tagged_courses_count": len(tagged_courses) if tagged_courses else 0,
        "upcoming_assignments_count": len(upcoming_assignments) if upcoming_assignments else 0,
        "price_sample": price_courses[0] if price_courses and len(price_courses) > 0 else None,
        "student_sample": recent_students[0] if recent_students and len(recent_students) > 0 else None,
        "tagged_sample": tagged_courses[0] if tagged_courses and len(tagged_courses) > 0 else None,
        "assignment_sample": upcoming_assignments[0] if upcoming_assignments and len(upcoming_assignments) > 0 else None
    }

    print("=== Verification Counts ===")
    print("Courses $50-$200:", verification['price_range_count'])
    print("Recent students:", verification['recent_students_count'])
    print("Tagged courses:", verification['tagged_courses_count'])
    print("Upcoming assignments:", verification['upcoming_assignments_count'])

    print("\n=== Sample Document Verification ===")
    print("Sample course in price range:", verification['price_sample'])
    print("Most recent student:", verification['student_sample'])
    print("Sample tagged course:", verification['tagged_sample'])
    print("Next due assignment:", verification['assignment_sample'])
    
    return verification

# Example usage:
# price_courses = find_courses_by_price_range(db)
# recent_students = find_recent_students(db)
# tagged_courses = find_courses_by_tags(db)
# upcoming_assignments = find_upcoming_assignments(db)
# verification = verify_query_results(db, price_courses, recent_students, 
#                                   tagged_courses, upcoming_assignments)



def course_enrollment_stat():
    
    # 1. Course Enrollment Statistics Pipeline
    enrollment_stats = db.enrollments.aggregate([
        # Join with courses collection
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "course"
            }
        },
        {"$unwind": "$course"},
        
        # Join with submissions for ratings (assuming rating is in submissions)
        {
            "$lookup": {
                "from": "submissions",
                "localField": "studentId",
                "foreignField": "studentId",
                "as": "submissions"
            }
        },
        
        # Group by course and calculate metrics
        {
            "$group": {
                "_id": {
                    "courseId": "$courseId",
                    "title": "$course.title",
                    "category": "$course.category"
                },
                "totalEnrollments": {"$sum": 1},
                "averageGrade": {"$avg": "$submissions.grade"},
                "completionRate": {"$avg": "$completionStatus"}
            }
        },
        
        # Project for cleaner output
        {
            "$project": {
                "courseTitle": "$_id.title",
                "category": "$_id.category",
                "totalEnrollments": 1,
                "averageGrade": {"$round": ["$averageGrade", 2]},
                "averageCompletion": {"$round": ["$completionRate", 2]},
                "_id": 0
            }
        },
        
        # Sort by enrollments (descending)
        {"$sort": {"totalEnrollments": -1}}
    ])

    # Convert to list for display
    stats_list = list(enrollment_stats)

    print("1. Course Enrollment Statistics:")
    print("=" * 50)
    pprint(stats_list)

    # Display as a table using pandas
    print("\nFormatted Results:")
    print("=" * 100)
    df = pd.DataFrame(stats_list)
    print(df.to_string(index=False))

    # Verification metrics
    total_courses = db.courses.count_documents({})
    print("\n=== Verification ===")
    print(f"Total courses in system: {total_courses}")
    print(f"Courses with enrollment data: {len(stats_list)}")
    print(f"Sample course stats:")
    pprint(stats_list[0] if stats_list else "No results")

    # Additional verification queries
    most_popular = max(stats_list, key=lambda x: x['totalEnrollments']) if stats_list else None
    print("\nMost Popular Course:")
    print(f" - Title: {most_popular['courseTitle'] if most_popular else 'N/A'}")
    print(f" - Enrollments: {most_popular['totalEnrollments'] if most_popular else 'N/A'}")
    print(f" - Avg Grade: {most_popular['averageGrade'] if most_popular else 'N/A'}")

    # Compare with raw counts
    print("\nRaw Enrollment Counts per Course:")
    raw_counts = db.enrollments.aggregate([
        {"$group": {"_id": "$courseId", "count": {"$sum": 1}}}
    ])
    for course in raw_counts:
        c = db.courses.find_one({"courseId": course["_id"]}, {"title": 1})
        print(f" - {c['title'] if c else 'Unknown'}: {course['count']}")

def student_performance_analysis():
    
    student_performance = db.enrollments.aggregate([
        # Join with users collection
        {
            "$lookup": {
                "from": "users",
                "localField": "studentId",
                "foreignField": "userId",
                "as": "student"
            }
        },
        {"$unwind": "$student"},
        
        # Join with submissions (preserving enrollments without submissions)
        {
            "$lookup": {
                "from": "submissions",
                "localField": "studentId",
                "foreignField": "studentId",
                "as": "submissions"
            }
        },
        
        # Add field to check if student has submissions
        {
            "$addFields": {
                "hasSubmissions": {"$gt": [{"$size": "$submissions"}, 0]}
            }
        },
        
        # Calculate average grade per enrollment (handling empty arrays)
        {
            "$addFields": {
                "enrollmentAvgGrade": {
                    "$cond": [
                        {"$eq": [{"$size": "$submissions"}, 0]},
                        None,
                        {"$avg": "$submissions.grade"}
                    ]
                }
            }
        },
        
        # Group by student
        {
            "$group": {
                "_id": {
                    "studentId": "$studentId",
                    "name": {"$concat": ["$student.firstName", " ", "$student.lastName"]}
                },
                "coursesEnrolled": {"$sum": 1},
                "coursesWithSubmissions": {"$sum": {"$cond": ["$hasSubmissions", 1, 0]}},
                "averageGrade": {"$avg": "$enrollmentAvgGrade"},
                "averageCompletion": {"$avg": "$completionStatus"},
                "submissionCount": {"$sum": {"$size": "$submissions"}}
            }
        },
        
        # Format output
        {
            "$project": {
                "studentName": "$_id.name",
                "coursesEnrolled": 1,
                "coursesWithSubmissions": 1,
                "averageGrade": {
                    "$ifNull": [
                        {"$round": ["$averageGrade", 2]},
                        None
                    ]
                },
                "averageCompletion": {"$round": ["$averageCompletion", 2]},
                "submissionCount": 1,
                "_id": 0
            }
        },
        
        # Sort by average grade (descending), putting nulls last
        {
            "$sort": {
                "averageGrade": -1,
                "submissionCount": -1
            }
        }
    ])

    # Convert to list and display
    performance_data = list(student_performance)

    print("Student Performance Analysis:")
    print("=" * 60)
    pprint(performance_data)

    # Display as table
    print("\nTop Performing Students:")
    print("=" * 120)
    df = pd.DataFrame(performance_data)
    print(df.to_string(index=False))

    # 2. Completion Rate by Course
    completion_by_course = db.enrollments.aggregate([
        # Join with courses
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "course"
            }
        },
        {"$unwind": "$course"},
        
        # Group by course
        {
            "$group": {
                "_id": {
                    "courseId": "$courseId",
                    "title": "$course.title"
                },
                "averageCompletion": {"$avg": "$completionStatus"},
                "totalStudents": {"$sum": 1}
            }
        },
        
        # Format output
        {
            "$project": {
                "courseTitle": "$_id.title",
                "averageCompletion": {"$round": ["$averageCompletion", 2]},
                "totalStudents": 1,
                "_id": 0
            }
        },
        
        # Sort by completion rate
        {"$sort": {"averageCompletion": -1}}
    ])

    print("\nCourse Completion Rates:")
    print("=" * 60)
    for course in completion_by_course:
        print(f"{course['courseTitle']}: {course['averageCompletion']}% ({course['totalStudents']} students)")

    # Verification
    print("\n=== Verification ===")
    top_student = performance_data[0] if performance_data else None
    print(f"Top student: {top_student['studentName'] if top_student else 'N/A'}")
    print(f"Avg grade: {top_student['averageGrade'] if top_student else 'N/A'}")
    print(f"Enrollments analyzed: {len(performance_data)}")

    # Verify with raw data
    sample_student = db.users.find_one({"userId": "user001"})
    student_grades = list(db.submissions.find({"studentId": "user001"}, {"grade": 1}))
    avg_grade = sum(g['grade'] for g in student_grades) / len(student_grades) if student_grades else 0

    print("\nSample Student Verification:")
    print(f"Name: {sample_student['firstName']} {sample_student['lastName']}")
    print(f"Calculated avg grade: {round(avg_grade, 2)}")
    print(f"Submissions: {len(student_grades)}")


def instructor_analysis():
    
    # Instructor Analytics Pipeline
    instructor_analytics = db.courses.aggregate([
        # Join with instructors
        {
            "$lookup": {
                "from": "users",
                "localField": "instructorId",
                "foreignField": "userId",
                "as": "instructor"
            }
        },
        {"$unwind": "$instructor"},
        
        # Join with enrollments
        {
            "$lookup": {
                "from": "enrollments",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "enrollments"
            }
        },
        
        # Join with submissions for ratings
        {
            "$lookup": {
                "from": "submissions",
                "localField": "enrollments.studentId",
                "foreignField": "studentId",
                "as": "submissions"
            }
        },
        
        # Calculate metrics per instructor-course combination
        {
            "$project": {
                "instructorId": 1,
                "instructorName": {"$concat": ["$instructor.firstName", " ", "$instructor.lastName"]},
                "courseTitle": "$title",
                "studentCount": {"$size": "$enrollments"},
                "courseRevenue": {"$multiply": ["$price", {"$size": "$enrollments"}]},
                "avgGrade": {"$avg": "$submissions.grade"}
            }
        },
        
        # Group by instructor
        {
            "$group": {
                "_id": "$instructorId",
                "instructorName": {"$first": "$instructorName"},
                "totalStudents": {"$sum": "$studentCount"},
                "totalRevenue": {"$sum": "$courseRevenue"},
                "coursesTaught": {"$sum": 1},
                "avgCourseRating": {"$avg": "$avgGrade"}
            }
        },
        
        # Format output
        {
            "$project": {
                "instructorName": 1,
                "totalStudents": 1,
                "totalRevenue": {"$round": ["$totalRevenue", 2]},
                "coursesTaught": 1,
                "avgCourseRating": {
                    "$ifNull": [
                        {"$round": ["$avgCourseRating", 2]},
                        "No ratings yet"
                    ]
                },
                "_id": 0
            }
        },
        
        # Sort by total students (descending)
        {"$sort": {"totalStudents": -1}}
    ])


    # Convert to list and display
    analytics_data = list(instructor_analytics)

    print("Instructor Analytics:")
    print("=" * 60)
    pprint(analytics_data)

    # Display as table
    print("\nFormatted Results:")
    print("=" * 60)
    df = pd.DataFrame(analytics_data)
    print(df.to_string(index=False))

    # Verification
    print("\n=== Verification ===")

    # Verify Chinwe Okonkwo (user002) - teaches Python and Django courses
    chinwe_courses = list(db.courses.find({"instructorId": "user002"}, {"courseId": 1, "title": 1, "price": 1}))
    chinwe_enrollments = db.enrollments.count_documents({"courseId": {"$in": [c["courseId"] for c in chinwe_courses]}})
    chinwe_revenue = sum(c["price"] * db.enrollments.count_documents({"courseId": c["courseId"]}) for c in chinwe_courses)

    print(f"\nManual calculation for Chinwe Okonkwo:")
    print(f"Courses taught: {[c['title'] for c in chinwe_courses]}")
    print(f"Total students: {chinwe_enrollments}")
    print(f"Calculated revenue: ${chinwe_revenue:.2f}")

    # Check against aggregation results
    chinwe_agg = next((i for i in analytics_data if i["instructorName"] == "Chinwe Okonkwo"), None)
    print(f"\nAggregation results:")
    print(f"Total students: {chinwe_agg['totalStudents'] if chinwe_agg else 'N/A'}")
    print(f"Total revenue: ${chinwe_agg['totalRevenue'] if chinwe_agg else 'N/A'}")




def analyze_learning_trends(db):
    """
    Analyzes and reports on key learning trends including:
    - Monthly enrollment patterns
    - Popular course categories
    - Student engagement metrics
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        dict: Dictionary containing all analytics results
    """
    results = {}
    
    # 1. Monthly Enrollment Trends
    monthly_enrollments = list(db.enrollments.aggregate([
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$enrollmentDate"},
                    "month": {"$month": "$enrollmentDate"}
                },
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]))
    results['monthly_trends'] = monthly_enrollments
    
    # 2. Most Popular Course Categories
    popular_categories = list(db.enrollments.aggregate([
        {
            "$lookup": {
                "from": "courses",
                "localField": "courseId",
                "foreignField": "courseId",
                "as": "course"
            }
        },
        {"$unwind": "$course"},
        {
            "$group": {
                "_id": "$course.category",
                "enrollmentCount": {"$sum": 1}
            }
        },
        {"$sort": {"enrollmentCount": -1}}
    ]))
    results['popular_categories'] = popular_categories
    
    # 3. Student Engagement Metrics
    total_enrollments = db.enrollments.count_documents({})
    active_enrollments = db.enrollments.count_documents({"completionStatus": {"$gt": 0}})
    submission_count = db.submissions.count_documents({})
    
    engagement_metrics = {
        'total_enrollments': total_enrollments,
        'active_enrollments': active_enrollments,
        'active_percentage': round(active_enrollments/total_enrollments*100, 2),
        'submission_count': submission_count,
        'avg_submissions_per_enrollment': round(submission_count/total_enrollments, 2)
    }
    results['engagement_metrics'] = engagement_metrics
    
    # Verification data
    sample_course = db.courses.find_one({"category": "Programming"})
    verification = {
        'sample_course': sample_course['title'] if sample_course else None,
        'sample_course_enrollments': db.enrollments.count_documents(
            {"courseId": sample_course["courseId"]}
        ) if sample_course else None
    }
    results['verification'] = verification
    
    return results

def print_learning_trends(results):
    """
    Prints the learning trends analysis in a formatted way
    
    Args:
        results: Dictionary returned from analyze_learning_trends()
    """
    # 1. Monthly Enrollment Trends
    print("\n1. Monthly Enrollment Trends:")
    for month in results['monthly_trends']:
        print(f"{month['_id']['month']}/{month['_id']['year']}: {month['count']} enrollments")
    
    # 2. Most Popular Course Categories
    print("\n2. Most Popular Course Categories:")
    for category in results['popular_categories']:
        print(f"{category['_id']}: {category['enrollmentCount']} enrollments")
    
    # 3. Student Engagement Metrics
    print("\n3. Student Engagement Metrics:")
    metrics = results['engagement_metrics']
    print(f"Total enrollments: {metrics['total_enrollments']}")
    print(f"Active enrollments: {metrics['active_enrollments']} ({metrics['active_percentage']}%)")
    print(f"Submissions made: {metrics['submission_count']}")
    print(f"Avg submissions per enrollment: {metrics['avg_submissions_per_enrollment']}")
    
    # Verification
    print("\n=== Verification ===")
    if results['verification']['sample_course']:
        print(f"Sample course '{results['verification']['sample_course']}' has "
              f"{results['verification']['sample_course_enrollments']} enrollments")
    else:
        print("No sample course found for verification")

# Example usage:
# trends_data = analyze_learning_trends(db)
# print_learning_trends(trends_data)



def create_database_indexes(db):
    """
    Creates optimized indexes for the learning management system database.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        dict: Dictionary containing index creation results and verification
    """
    results = {
        'indexes_created': [],
        'verification': {},
        'errors': []
    }

    # 1. User email lookup index
    try:
        db.users.create_index(
            [("email", ASCENDING)], 
            unique=True, 
            name="email_lookup_idx"
        )
        results['indexes_created'].append("email_lookup_idx")
    except Exception as e:
        results['errors'].append(f"Failed to create email index: {str(e)}")

    # 2. Course search by title and category index
    try:
        db.courses.create_index(
            [("title", TEXT), ("category", ASCENDING)],
            name="course_search_idx"
        )
        results['indexes_created'].append("course_search_idx")
    except Exception as e:
        results['errors'].append(f"Failed to create course search index: {str(e)}")

    # 3. Assignment queries by due date index
    try:
        db.assignments.create_index(
            [("dueDate", ASCENDING)],
            name="due_date_idx"
        )
        results['indexes_created'].append("due_date_idx")
    except Exception as e:
        results['errors'].append(f"Failed to create due date index: {str(e)}")

    # 4. Enrollment queries by student and course index
    try:
        db.enrollments.create_index(
            [("studentId", ASCENDING), ("courseId", ASCENDING)],
            name="student_course_idx"
        )
        results['indexes_created'].append("student_course_idx")
    except Exception as e:
        results['errors'].append(f"Failed to create enrollment index: {str(e)}")

    # Verify all indexes
    collections = {
        'users': 'email_lookup_idx',
        'courses': 'course_search_idx',
        'assignments': 'due_date_idx',
        'enrollments': 'student_course_idx'
    }

    for collection_name, index_name in collections.items():
        results['verification'][index_name] = verify_index(
            db[collection_name], 
            index_name
        )

    return results

def verify_index(collection, index_name):
    """
    Verifies if an index exists in the specified collection.
    
    Args:
        collection: MongoDB collection object
        index_name: Name of the index to verify
        
    Returns:
        bool: True if index exists, False otherwise
    """
    try:
        indexes = collection.index_information()
        return index_name in indexes
    except Exception as e:
        print(f"Error verifying index {index_name}: {str(e)}")
        return False
    

def print_index_results(results):
    """
    Prints the index creation results in a formatted way.
    
    Args:
        results: Dictionary returned from create_database_indexes()
    """
    print("\n=== Index Creation Results ===")
    print(f"Successfully created {len(results['indexes_created'])} indexes:")
    for index in results['indexes_created']:
        print(f" - {index}")
    
    if results['errors']:
        print("\nErrors encountered:")
        for error in results['errors']:
            print(f" - {error}")
    
    print("\n=== Index Verification ===")
    for index_name, exists in results['verification'].items():
        status = "EXISTS" if exists else "MISSING"
        print(f"{index_name}: {status}")

def drop_all_indexes(db):
    """
    Drops all custom indexes from the database collections.
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        dict: Dictionary of dropped indexes by collection
    """
    dropped = {}
    collections = ['users', 'courses', 'assignments', 'enrollments']
    
    for collection_name in collections:
        collection = db[collection_name]
        current_indexes = collection.index_information()
        
        # Skip the default _id_ index
        indexes_to_drop = [
            name for name in current_indexes.keys() 
            if name != '_id_'
        ]
        
        if indexes_to_drop:
            collection.drop_indexes()
            dropped[collection_name] = indexes_to_drop
    
    return dropped

# Example usage:
# index_results = create_database_indexes(db)
# print_index_results(index_results)

# To reset indexes:
# dropped_indexes = drop_all_indexes(db)
# print("Dropped indexes:", dropped_indexes)



def create_index_safely(collection, index_spec, index_name):
    """
    Safely creates an index if it doesn't exist, or returns existing matching index.
    
    Args:
        collection: MongoDB collection object
        index_spec: List of tuples specifying index fields and directions
        index_name: Name for the new index
        
    Returns:
        str: Name of the index being used
    """
    existing_indexes = collection.index_information()
    
    # Check if equivalent index exists
    for name, spec in existing_indexes.items():
        if spec['key'] == index_spec:
            print(f"Using existing index {name} with same specification")
            return name
    
    # If not, create new index
    try:
        collection.create_index(index_spec, name=index_name)
        print(f"Created new index: {index_name}")
        return index_name
    except OperationFailure as e:
        if e.code == 85:  # IndexOptionsConflict
            existing_name = next(name for name, spec in existing_indexes.items() 
                            if spec['key'] == index_spec)
            print(f"Using existing index {existing_name} (conflict with {index_name})")
            return existing_name
        raise

def test_query_performance(db):
    """
    Tests and optimizes query performance by:
    1. Testing queries before optimization
    2. Creating optimized indexes
    3. Testing queries after optimization
    4. Calculating performance improvements
    
    Args:
        db: MongoDB database connection object
        
    Returns:
        dict: Dictionary containing performance results and index information
    """
    results = {
        'original_times': [],
        'optimized_times': [],
        'improvements': [],
        'index_info': {}
    }

    # Define test queries
    def query_courses_by_category():
        return db.courses.find({"category": "Programming"})

    def query_active_students():
        return db.users.find({"role": "student", "isActive": True})

    def query_upcoming_assignments():
        return db.assignments.find({"dueDate": {"$gt": datetime.now()}}).sort("dueDate", 1)

    # Test queries before optimization
    print("="*20 + " BEFORE OPTIMIZATION " + "="*20)
    results['original_times'].append(execute_and_analyze_query(db, query_courses_by_category, "Courses by category"))
    results['original_times'].append(execute_and_analyze_query(db, query_active_students, "Active students"))
    results['original_times'].append(execute_and_analyze_query(db, query_upcoming_assignments, "Upcoming assignments"))

    # Create optimized indexes
    print("\n" + "="*20 + " CREATING INDEXES " + "="*20)
    category_index = create_index_safely(
        db.courses,
        [("category", 1)],
        "category_optimized"
    )

    student_status_index = create_index_safely(
        db.users,
        [("role", 1), ("isActive", 1)],
        "active_students_optimized"
    )

    due_date_index = create_index_safely(
        db.assignments,
        [("dueDate", 1)],
        "due_date_optimized"
    )

    # Define optimized queries using hints
    def optimized_category_query():
        return db.courses.find({"category": "Programming"}).hint(category_index)

    def optimized_active_students():
        return db.users.find({"role": "student", "isActive": True}).hint(student_status_index)

    def optimized_assignments():
        return db.assignments.find({"dueDate": {"$gt": datetime.now()}}).sort("dueDate", 1).hint(due_date_index)

    # Test optimized queries
    print("\n" + "="*20 + " AFTER OPTIMIZATION " + "="*20)
    results['optimized_times'].append(execute_and_analyze_query(db, optimized_category_query, "Courses by category (optimized)"))
    results['optimized_times'].append(execute_and_analyze_query(db, optimized_active_students, "Active students (optimized)"))
    results['optimized_times'].append(execute_and_analyze_query(db, optimized_assignments, "Upcoming assignments (optimized)"))

    # Calculate improvements
    results['improvements'] = [
        results['original_times'][0]/results['optimized_times'][0],
        results['original_times'][1]/results['optimized_times'][1],
        results['original_times'][2]/results['optimized_times'][2]
    ]

    # Get index information
    results['index_info'] = {
        'courses': db.courses.index_information(),
        'users': db.users.index_information(),
        'assignments': db.assignments.index_information()
    }

    return results

def execute_and_analyze_query(db, query_func, query_name):
    """
    Executes and analyzes a query's performance
    
    Args:
        db: MongoDB database connection object
        query_func: Function that returns a MongoDB cursor
        query_name: Name of the query for reporting
        
    Returns:
        float: Execution time in seconds
    """
    # Run query and time it
    start_time = time.time()
    results = list(query_func())
    end_time = time.time()
    
    # Get execution stats
    explain = query_func().explain()
    execution_stats = explain.get('executionStats', explain)
    
    # Determine if index was used
    index_used = 'None'
    if 'indexName' in execution_stats:
        index_used = execution_stats['indexName']
    elif execution_stats.get('executionStages', {}).get('stage') == 'IXSCAN':
        index_used = execution_stats['executionStages'].get('indexName', 'Unknown')
    
    # Print results
    print(f"\n{query_name.upper()} RESULTS")
    print("-" * 40)
    print(f"Execution time: {(end_time - start_time)*1000:.2f} ms")
    print(f"Documents examined: {execution_stats.get('totalDocsExamined', 'N/A')}")
    print(f"Results returned: {len(results)}")
    print(f"Index used: {index_used}")
    
    return end_time - start_time

def print_performance_results(results):
    """
    Prints the performance test results in a formatted way
    
    Args:
        results: Dictionary returned from test_query_performance()
    """
    print("\n" + "="*20 + " PERFORMANCE IMPROVEMENT " + "="*20)
    print("\nSpeed Improvement Factors:")
    print(f"1. Category query: {results['improvements'][0]:.1f}x faster")
    print(f"2. Active students: {results['improvements'][1]:.1f}x faster")
    print(f"3. Assignments: {results['improvements'][2]:.1f}x faster")

    print("\n" + "="*20 + " INDEX INFORMATION " + "="*20)
    print("\nCourses indexes:")
    pprint(results['index_info']['courses'])

    print("\nUsers indexes:")
    pprint(results['index_info']['users'])

    print("\nAssignments indexes:")
    pprint(results['index_info']['assignments'])

# Example usage:
# performance_results = test_query_performance(db)
# print_performance_results(performance_results)



def handle_errors():
    print("=== ERROR HANDLING DEMONSTRATION ===")
    
    # 1. Handle duplicate key errors
    print("\n1. Duplicate Key Error Handling:")
    try:
        # Try inserting a user with duplicate email
        db.users.insert_one({
            "userId": "user999",
            "email": "adebola.adesanya@gmail.com",  # Existing email
            "firstName": "Test",
            "lastName": "User",
            "role": "student",
            "dateJoined": datetime.now(),
            "isActive": True
        })
    except DuplicateKeyError as e:
        print(f"Caught DuplicateKeyError: {e.details['errmsg']}")
        print("Action: Rejected duplicate email address")
    
    # 2. Handle invalid data type insertions
    print("\n2. Invalid Data Type Handling:")
    try:
        # Try inserting invalid data (string instead of number for price)
        db.courses.insert_one({
            "courseId": "course999",
            "title": "Invalid Course",
            "price": "free",  # Should be number
            "instructorId": "user001",
            "createdAt": datetime.now()
        })
    except OperationFailure as e:
        print(f"Caught OperationFailure: {e.details['errmsg']}")
        print("Action: Rejected invalid price data type")
    
    # 3. Handle missing required fields
    print("\n3. Missing Required Fields Handling:")
    try:
        # Try inserting user without required email field
        db.users.insert_one({
            "userId": "user999",
            "firstName": "Test",
            "lastName": "User",
            "role": "student",
            "dateJoined": datetime.now(),
            "isActive": True
        })
    except OperationFailure as e:
        print(f"Caught OperationFailure: {e.details['errmsg']}")
        print("Action: Rejected document missing required email field")
    
    # 4. Bonus: Document validation error (schema mismatch)
    print("\n4. Schema Validation Handling:")
    try:
        # Try inserting invalid role
        db.users.insert_one({
            "userId": "user999",
            "email": "test.user@example.com",
            "firstName": "Test",
            "lastName": "User",
            "role": "admin",  # Not in enum (student/instructor)
            "dateJoined": datetime.now(),
            "isActive": True
        })
    except OperationFailure as e:
        print(f"Caught OperationFailure: {e.details['errmsg']}")
        print("Action: Rejected invalid role value")

# Usage
# handle_errors()