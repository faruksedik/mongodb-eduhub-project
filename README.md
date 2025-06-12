# EduHub MongoDB Project

## Overview

This project, "EduHub," is a MongoDB-based database backend for an online e-learning platform designed as part of the AltSchool of Data Engineering Tinyuka 2024 Second Semester Project Exam. It demonstrates proficiency in MongoDB fundamentals, including database design, data modeling, CRUD operations, query optimization, aggregation pipelines, and performance tuning. The system supports user management, course management, enrollment tracking, assessments, analytics, and search functionality.

## Project Objectives

- Build a scalable NoSQL database system for an e-learning platform.
- Implement data integrity, validation, and efficient querying.
- Provide comprehensive documentation and interactive code examples.

## Features

- **User Management**: Registration, authentication, and profile management for students and instructors.
- **Course Management**: Creation, publishing, and organization of courses.
- **Enrollment System**: Track student enrollments and progress.
- **Assessment System**: Manage assignments, submissions, and grading.
- **Analytics and Reporting**: Generate performance metrics and statistics.
- **Search and Discovery**: Enable course search with filtering and sorting.

## Setup Instructions

### Prerequisites

- MongoDB v8.0 or higher (https://www.mongodb.com/try/download/community)
- Python 3.8+
- Required Python libraries: `pymongo`, `pandas`, `datetime`

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/faruksedik/mongodb-eduhub-project.git
   cd mongodb-eduhub-project
   ```

2. **Set Up MongoDB**

   - Install MongoDB and start the service.
   - Ensure it runs on `mongodb://localhost:27017/`.

3. **Install Dependencies**

   ```bash
   pip install pymongo pandas 
   ```

4. **Run the Jupyter Notebook**

   - Open `notebooks/eduhub_mongodb_project.ipynb` in Jupyter Notebook.
   - Execute all cells to set up the database and run queries.

5. **Import Sample Data**

   - Use `data/sample_data.json` to populate the database with initial data.

## Database Schema

### Collections

- **users**: Stores student and instructor profiles.
  - `_id` (string): Unique user ID.
  - `email` (string): Unique email address.
  - `firstName` (string): User's first name.
  - `lastName` (string): User's last name.
  - `role` (string): Enum \['student', 'instructor'\].
  - `dateJoined` (date): Registration date.
  - `profile` (object): Bio, avatar, and skills.
  - `isActive` (boolean): User status.
- **courses**: Stores course details.
  - `_id` (string): Unique course ID.
  - `title` (string): Course title.
  - `instructorId` (string): References `users._id`.
  - `category` (string): Course category.
  - `level` (string): Enum \['beginner', 'intermediate', 'advanced'\].
  - `duration` (number): Duration in hours.
  - `price` (number): Course price.
  - `tags` (array): Course tags.
  - `createdAt` (date): Creation date.
  - `updatedAt` (date): Last update date.
  - `isPublished` (boolean): Publication status.
- **enrollments**: Tracks student enrollments.
  - `_id` (string): Unique enrollment ID.
  - `studentId` (string): References `users._id`.
  - `courseId` (string): References `courses._id`.
  - `enrollmentDate` (date): Enrollment date.
  - `completionStatus` (number): Progress (0-100).
  - `lastAccessed` (date): Last access date.
- **lessons**: Stores course lessons.
  - `_id` (string): Unique lesson ID.
  - `courseId` (string): References `courses._id`.
  - `title` (string): Lesson title.
  - `content` (string): Lesson content.
  - `sequence` (number): Lesson order.
  - `duration` (number): Duration in minutes.
  - `resources` (array): Resource URLs.
- **assignments**: Stores course assignments.
  - `_id` (string): Unique assignment ID.
  - `courseId` (string): References `courses._id`.
  - `title` (string): Assignment title.
  - `description` (string): Assignment description.
  - `dueDate` (date): Submission deadline.
  - `maxPoints` (number): Maximum points.
  - `instructions` (string): Assignment instructions.
- **submissions**: Tracks assignment submissions.
  - `_id` (string): Unique submission ID.
  - `assignmentId` (string): References `assignments._id`.
  - `studentId` (string): References `users._id`.
  - `submittedDate` (date): Submission date.
  - `content` (string): Submission content.
  - `grade` (number): Assigned grade (0-100).
  - `feedback` (string): Instructor feedback.
  - `isGraded` (boolean): Grading status.

### Relationships

- `instructorId` (courses) → `users._id`.
- `studentId` (enrollments, submissions) → `users._id`.
- `courseId` (enrollments, lessons, assignments) → `courses._id`.
- `assignmentId` (submissions) → `assignments._id`.

## Usage

- Run the Jupyter Notebook to execute CRUD operations, aggregations, and performance tests.
- Use `src/eduhub_queries.py` as a reference for standalone Python scripts.
- Modify `sample_data.json` to add or update data as needed.

## Data Loading Utility – Code Explanation

This section contains utility functions to load and insert data from the `sample_data.json` file into MongoDB. Here's what each part does:

---

### `convert_date_strings_to_datetime(data, date_fields)`

- **Purpose:** Converts specified string date fields in a document to `datetime` objects.
- **Used for:** Ensuring proper date format before MongoDB insertion (MongoDB requires actual date types, not strings).

---

### `load_json_to_dict(file_path)`

- **Purpose:** Loads and parses JSON data from a specified file path.
- **Returns:** A Python dictionary containing the parsed JSON content.
- **Error Handling:**
  - Catches file not found and JSON decoding errors.

---

### `convert_dates_in_collections(data)`

- **Purpose:** Iterates over collections (like `users`, `courses`, etc.) and converts their date fields using the helper above.
- **Uses:** A predefined dictionary `date_fields` to map each collection to its date fields.

---

### `load_data_into_mongodb(data)`

- **Purpose:** Inserts all documents into their corresponding MongoDB collections using `insert_many`.

---

### `load_json_to_mongodb_collections(file_path)`

- **Purpose:** Orchestrates the full process:
  1. Loads JSON from file.
  2. Converts date strings to `datetime`.
  3. Inserts data into MongoDB.
- **Prints:** Success or failure messages for the overall operation.

---

### Usage Example

```python
file_path = 'data/sample_data.json'
load_json_to_mongodb_collections(file_path)
```

## CRUD Operations Summary

All core **Create**, **Read**, **Update**, and **Delete (CRUD)** functionalities required for the EduHub project have been fully implemented and demonstrated in the main notebook: `eduhub_mongodb_project.ipynb`.

### Task 3.1: Create Operations
- Added a new student user
- Created a new course
- Enrolled a student in a course
- Added a new lesson to an existing course

### Task 3.2: Read Operations
- Queried all active students
- Retrieved course details with instructor info
- Listed all courses in a specific category
- Found students enrolled in a given course
- Implemented case-insensitive course title search

### Task 3.3: Update Operations
- Updated user profile data
- Marked a course as published
- Modified assignment grades
- Added new tags to an existing course

### Task 3.4: Delete Operations
- Soft-deleted a user (set `isActive` to `false`)
- Deleted an enrollment document
- Removed a lesson from a course

*Refer to* `eduhub_mongodb_project.ipynb` *for code implementations and execution results.*


## Performance Optimization

- Indexes created on:
  - `users.email` for unique lookups.
  - `courses.title` and `courses.category` for search.
  - `assignments.dueDate` for deadline queries.
  - `enrollments.studentId` and `enrollments.courseId` for enrollment lookups.
- Query performance analyzed using `explain()` and optimized with timing comparisons.



## Challenges Faced and Solutions

Below are some challenges encountered during the development of the EduHub MongoDB project and how they were addressed:

---

### 1. Handling Complex Nested JSON Data
- **Challenge:** The `sample_data.json` file had nested structures and date strings that required conversion before MongoDB insertion.
- **Solution:** 
  - Wrote utility functions (`convert_date_strings_to_datetime`, `convert_dates_in_collections`) to parse ISO-formatted strings into Python `datetime` objects.
  - Handled collection-wise conversion for robust data loading.

---

### 2. Environment Setup for Notebook Execution
- **Challenge:** Ensuring all required libraries were present in the execution environment (Jupyter Notebook / VS Code).
- **Solution:**
  - Listed all dependencies (`pymongo`, `pandas`, `bson`, etc.) in the README for easy setup.

---

### 3. Maintaining Data Consistency Across Collections
- **Challenge:** Ensuring that related documents (e.g. users and enrollments, courses and lessons) maintained consistent foreign key references (e.g. `userId`, `courseId`).
- **Solution:**
  - Implemented structured creation logic to match valid `userId` and `courseId`.
  - Used unique fields and validations to prevent duplication.

---

### 4. Error Handling for Data Loading
- **Challenge:** Data loading failed silently when JSON was malformed or file paths were wrong.
- **Solution:**
  - Implemented try-except blocks for file reading, JSON parsing, and MongoDB insertion.
  - Displayed clear error messages to aid debugging.


## License

This project is licensed under the **MIT License**.  
Feel free to use, modify, and distribute this project in accordance with the terms of the license.

## Contributors

- Faruk Sedik

## Submission Details

- **Due Date**: Sunday, June 15, 2025, 11:59 PM WAT.

## Resources

MongoDB Documentation: https://docs.mongodb.com/