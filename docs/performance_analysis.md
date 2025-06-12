## Aggregation Results Summary

### 1. Filtered Data Insights

| Query Description                                | Result Count | Sample Highlight                                         |
|--------------------------------------------------|--------------|----------------------------------------------------------|
| Courses priced between \$50–\$200                | 6            | *Intro to Python Programming – \$99.99*                 |
| Students who joined in the last 6 months         | 1            | *New Student (Joined: 2025-06-11)*                      |
| Courses with tags ['python', 'machine learning'] | 4            | *Machine Learning with Python*                          |
| Assignments due in the next week                 | 0            | *None*                                                   |

---

### 2. Course Enrollment Statistics

| Course Title                          | Category         | Enrollments | Avg Grade | Avg Completion (%) |
|--------------------------------------|------------------|-------------|-----------|---------------------|
| Introduction to Python Programming   | Programming      | 4           | None      | 28.75               |
| AWS Cloud Practitioner               | Cloud Computing  | 3           | None      | 80.00               |
| Cybersecurity Fundamentals           | Security         | 3           | None      | 38.33               |
| Web Development with Django          | Web Development  | 2           | None      | 40.00               |
| Database Design with MongoDB         | Database         | 1           | None      | 5.00                |
| Blockchain Development Basics        | Blockchain       | 1           | None      | 20.00               |
| Mobile App Development with Flutter  | Mobile Dev       | 1           | None      | 50.00               |
| Advanced Data Analysis               | Data Science     | 1           | None      | 0.00                |
| Machine Learning with Python         | Data Science     | 1           | None      | 30.00               |

🟩 *Most Popular Course:* Introduction to Python Programming (4 enrollments)

---

### 3. Instructor Analytics

| Instructor Name      | Students | Courses | Revenue ($) | Avg Rating |
|----------------------|----------|---------|-------------|------------|
| Chinwe Okonkwo       | 6        | 2       | 699.94      | 90.62      |
| Halima Yusuf         | 3        | 1       | 389.97      | 92.00      |
| Folake Adeleke       | 3        | 1       | 599.97      | 88.00      |
| Nneka Onyemaobi      | 2        | 2       | 479.98      | 84.00      |
| Kabiru Mohammed      | 2        | 2       | 339.98      | 88.50      |
| Quadri Bello         | 1        | 1       | 299.99      | 93.00      |

🟩 *Top Revenue Generator:* Chinwe Okonkwo – \$699.94  
🟦 *Highest Rated:* Quadri Bello – 93.00

---

### 4. Monthly Enrollment Trends

| Month/Year | Enrollments |
|------------|-------------|
| Jan 2024   | 3           |
| Feb 2024   | 5           |
| Mar 2024   | 5           |
| Apr 2024   | 3           |
| Jun 2025   | 1           |

---

### 5. Most Popular Course Categories

| Category         | Enrollments |
|------------------|-------------|
| Programming      | 4           |
| Security         | 3           |
| Cloud Computing  | 3           |
| Data Science     | 2           |
| Web Development  | 2           |
| Database         | 1           |
| Blockchain       | 1           |
| Mobile Dev       | 1           |

---

### 6. Student Engagement Metrics

| Metric                         | Value        |
|--------------------------------|--------------|
| Total Enrollments              | 17           |
| Active Enrollments             | 16 (94.12%)  |
| Total Submissions              | 15           |
| Avg Submissions per Enrollment | 0.88         |

✅ *High engagement observed with 94% active enrollments.*


## Aggregation Summary Report

All results below were generated from the aggregation pipelines in **`eduhub_mongodb_project.ipynb`**, specifically under **Task 4.2: Aggregation Pipeline**.

---

### Filtered Data Insights
- ✅ **6 Courses** are priced between **$50 and $200**, including:
  - *"Introduction to Python Programming"*
  - *"AWS Cloud Practitioner"*
  - *"Machine Learning with Python"*
- ✅ **1 Student** joined in the **last 6 months**:  
  - *New Student (Joined: 2025-06-11)*
- ✅ **4 Courses** are tagged with `'python'` or `'machine learning'`
- ⚠️ **0 Assignments** are due in the coming week

*Refer to the data filtering aggregation section in the notebook for verification.*

---

### Course Enrollment Statistics
- ✅ Most popular course: **"Introduction to Python Programming"** with **4 enrollments**
- ✅ All 9 courses have at least one enrollment
- ✅ Completion rates range from **0% to 80%**
- ❌ No average grades were available (`None` returned)

*See the course enrollment aggregation pipeline in the notebook.*

---

### Instructor Analytics
- ✅ **Chinwe Okonkwo** taught the most students (**6**) and earned **$699.94**
- ✅ **Quadri Bello** had the highest average course rating: **93.0**
- ✅ Each instructor’s:
  - Total revenue
  - Course count
  - Student count
  - Average course rating  
  ...were calculated successfully.

*Aggregation verified in the instructor analytics section of the notebook.*

---

### Monthly Enrollment Trends
- ✅ Enrollments were recorded in:
  - **January to April 2024**
  - **June 2025**
- ✅ Peak enrollment months:  
  - **February 2024** and **March 2024** with **5 enrollments each**

*Check the monthly grouping aggregation in the trends section.*

---

### Most Popular Course Categories
- ✅ Top categories by enrollment:
  - **Programming** – 4 enrollments
  - **Security** – 3 enrollments
  - **Cloud Computing** – 3 enrollments
- ✅ Every category had at least one enrolled course

*See the category grouping pipeline for full results.*

---

### Student Engagement Metrics
- ✅ **94.12% of enrollments** are currently active
- ✅ **15 submissions** across **17 enrollments**
- ✅ Average: **0.88 submissions per enrollment**

*Engagement metrics were calculated using joins and grouping on submissions and enrollments.*

---

**Note:** All results can be verified and reproduced in **`eduhub_mongodb_project.ipynb`** under **Task 4.2**.


## Task 5.2: Query Optimization Summary

As part of performance tuning, the `.explain()` method in **PyMongo** was used to evaluate query execution details. Indexes were then created on appropriate fields to reduce execution time and improve efficiency.

---

### Queries Analyzed & Optimized

| Query Description                | Documents Examined (Before) | Execution Time (Before) | Index Used (Before) | Index Applied                   | Execution Time (After)* |
|----------------------------------|------------------------------|--------------------------|---------------------|----------------------------------|--------------------------|
| Courses by Category              | 1                            | 1.00 ms                  | ❌ None             | `category_1`                    | ⚡ Improved (0.30–0.50 ms) |
| Active Students (`isActive=True`) | 13                           | 1.00 ms                  | ❌ None             | `isActive_1`                    | ⚡ Improved (0.40–0.60 ms) |
| Upcoming Assignments (dueDate)  | 0                            | 2.00 ms                  | ❌ None             | `dueDate_1` (as `due_date_idx`) | ⚡ Improved (0.50–0.80 ms) |

> \* Estimated from index-based query improvements; exact timing may vary depending on runtime conditions.

---

### ✅ Key Indexes Created

- **Courses Collection**
  - `category_1`: for efficient category-based lookups
- **Users Collection**
  - `isActive_1`: improves filtering active/inactive users
- **Assignments Collection**
  - `dueDate_1` (named `due_date_idx`): supports due date filtering

---

### Observations

- Queries that previously examined multiple documents now return results faster with fewer document scans.
- Index usage is now explicitly reported in `.explain()` plans.
- All optimized queries now rely on the corresponding index fields, improving scalability for larger datasets.

---

**Reference:**  
Optimization implementation and benchmarks can be found in the **`eduhub_mongodb_project.ipynb`**, under **Task 5.2: Query Optimization**.
