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
   - All the codes are written in the `eduhub_queries.py` file

5. **Import Sample Data**

   - Use `data/sample_data.json` to populate the database with initial data.

## Database Schema

### Collections

`users` **Collection**

Represents all user accounts (students, instructors, admins).


| Field        | Type    | Description                         |
| ------------ | ------- | ----------------------------------- |
| `userId`     | String  | Unique user identifier              |
| `email`      | String  | User's email address (indexed)      |
| `firstName`  | String  | First name                          |
| `lastName`   | String  | Last name                           |
| `role`       | String  | One of: `"student"`, `"instructor"` |
| `dateJoined` | Date    | When the user joined                |
| `isActive`   | Boolean | Active status (soft deletes)        |
| `profile`    | Object  | User bio and skillset               |

`courses`  **Collection**

Stores all available courses on EduHub.

| Field          | Type    | Description                          |
| -------------- | ------- | ------------------------------------ |
| `courseId`     | String  | Unique identifier                    |
| `title`        | String  | Course name                          |
| `description`  | String  | Overview of course content           |
| `category`     | String  | Course category (e.g., "Data", etc.) |
| `instructorId` | String  | Linked user (instructor)             |
| `createdAt`    | Date    | Course creation timestamp            |
| `updatedAt`    | Date    | Last updated timestamp               |
| `tags`         | Array   | Keywords for search                  |
| `price`        | Number  | Price of the course in USD           |
| `isPublished`  | Boolean | Whether it's publicly available      |


`enrollments` **Collection**

Tracks which students are enrolled in which courses.

| Field            | Type   | Description                   |
| ---------------- | ------ | ----------------------------- |
| `enrollmentId`   | String | Unique enrollment ID          |
| `studentId`      | String | Refers to `users.userId`      |
| `courseId`       | String | Refers to `courses.courseId`  |
| `enrollmentDate` | Date   | When the enrollment occurred  |
| `lastAccessed`   | Date   | Last time course was accessed |
| `progress`       | Number | Completion %                  |


`lessons` **Collection**

Defines course lessons and their content.

| Field      | Type   | Description                     |
| ---------- | ------ | ------------------------------- |
| `lessonId` | String | Unique identifier               |
| `courseId` | String | Linked course                   |
| `title`    | String | Lesson title                    |
| `content`  | String | HTML or Markdown-formatted body |
| `duration` | Number | Length in minutes               |


`assignments` **Collection**

Assignments tied to specific lessons or courses.

| Field          | Type   | Description                |
| -------------- | ------ | -------------------------- |
| `assignmentId` | String | Unique assignment ID       |
| `courseId`     | String | Linked course              |
| `title`        | String | Assignment title           |
| `instructions` | String | Detailed assignment prompt |
| `dueDate`      | Date   | Deadline                   |


`submissions` **Collection**

Stores student submissions for assignments.

| Field           | Type    | Description                          |
| --------------- | ------- | ------------------------------------ |
| `submissionId`  | String  | Unique ID                            |
| `assignmentId`  | String  | Refers to `assignments.assignmentId` |
| `studentId`     | String  | Refers to `users.userId`             |
| `submittedDate` | Date    | When the student submitted           |
| `grade`         | Number  | Score given                          |
| `isGraded`      | Boolean | Whether the submission is graded     |


### Relationships

- `instructorId` (courses) → `users._id`.
- `studentId` (enrollments, submissions) → `users._id`.
- `courseId` (enrollments, lessons, assignments) → `courses._id`.
- `assignmentId` (submissions) → `assignments._id`.

## Usage

- Run the Jupyter Notebook to execute CRUD operations, aggregations, and performance tests.
- Use `src/eduhub_queries.py` as a reference for standalone Python scripts.
- Modify `sample_data.json` to add or update data as needed.

## 📥 Data Loader: `load_data_to_collections(file_path)`

This function loads data from a JSON file into MongoDB collections while ensuring that all date fields are properly converted from string format to `datetime` objects.


### ✅ Purpose

- Import data from a JSON source into MongoDB collections (`users`, `courses`, `enrollments`, `lessons`, `assignments`, `submissions`)
- Automatically convert ISO 8601 date strings (e.g., `"2024-01-01T00:00:00Z"`) to Python `datetime` objects before insertion
- Ensure data integrity and avoid schema validation errors


### ⚙️ How It Works

1. **Load the JSON file** using Python’s `json` module.
2. **Define date fields** that need conversion for each collection.
3. **Iterate through each relevant collection**:
   - Check if it exists in the JSON.
   - Convert date fields to `datetime`.
   - Insert documents into the corresponding MongoDB collection using `insert_many()`.


### 🗂️ Collections Processed

- `users` → converts `dateJoined`
- `courses` → converts `createdAt`, `updatedAt`
- `enrollments` → converts `enrollmentDate`, `lastAccessed`
- `assignments` → converts `dueDate`
- `submissions` → converts `submittedDate`
- `lessons` → loaded directly (no date conversion)

---

### 🧪 Example Usage

```python
load_data_to_collections('file_path')
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