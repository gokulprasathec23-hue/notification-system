# Stage 1
# Notification System Overview
This system allows users to receive and manage notifications.
# Core Actions
Create notification
Fetch notifications
Mark notification as read
Delete notification
Real-time notifications
# REST API Endpoints
# GET /api/notifications
# POST /api/notifications
# PATCH /api/notifications/{id}/read
# DELETE /api/notifications/{id}
# Notification JSON Schema
json
{
  "id": "string",
  "title": "string",
  "message": "string",
  "isRead": false
}
# Stage 2 
# Data Base Choice
MongoDB is selected for the notification system because it supports high-volume data, flexible schema design, and fast read/write operations.
# Schema of the DB Choosen
{ "_id": "ObjectId",
 "userId": "string", 
 "title": "string", 
 "message": "string", 
 "type": "string", 
 "isRead": false,
"createdAt": "date"
}
# Problem arises when the data volume increses ?
When data volume increases significantly in MongoDB, it impacts performance, storage, and infrastructure requirements.
# How to over come it ?
MongoDB is built for scale. Its distributed architecture combines replica sets, sharding, and intelligent query routing to handle high traffic and large datasets without requiring you to endlessly upgrade a single server.
 # MongoDB query according to stage 1 end points.
POST /api/notifications → insertOne()
GET /api/notifications → find()
PATCH /api/notifications/{id}/read → updateOne()
DELETE /api/notifications/{id} → deleteOne()
# Stage 3
# is the query accurate 
SELECT * FROM notifications
WHERE studentID = 1042 AND isRead = false
ORDER BY createdAt ASC;

The query is correct but performs slowly because the notifications table contains millions of records. Without proper indexing, the database performs a full table scan and sorting operation.
# why this is slow ?
Beasuce it sort from first to till the required found so that query may be slow.
# Changes to be done 
Add a composite index:
CREATE INDEX idx_student_read_created
ON notifications(studentID, isRead, createdAt);

# Is Adding Indexes on Every Column Effective?
Adding indexes on every column is not effective because:
Incre,ases storage usage,Slows INSERT, UPDATE, DELETE operations Increases index maintenance overhead,Many indexes may never be used Indexes should only be added on frequently filtered, searched, and sorted columns.
# Query to Find Students Who Got Placement Notifications in Last 7 Days
SELECT DISTINCT studentID
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= NOW() - INTERVAL 7 DAY;

# Stage 4
# Suggested Solutions
# 1. Pagination
Fetch notifications in smaller batches instead of loading all notifications.
# Performance Improvement
Reduces database load, Faster API response,Lower memory usage,Reduces repeated database queries ,Faster notification retrieval, Reduces unnecessary database requests,Improves page load speed
# Tradeoff
Requires multiple API calls for more data,Additional cache management,Possible stale data issues,Notifications are not loaded immediately

# Stage 5
# Shortcomings of Current Implementation
 Sequential processing is slow for 50,000 students
 Email API failure stops reliable delivery
 No retry mechanism
 High database load
 No fault tolerance
 Poor scalability
 No asynchronous processing
# Problem with Email Failure
If `send_email()` fails midway for 200 students:
Some students receive notifications
Some students do not receive notifications
Data becomes inconsistent
Manual recovery becomes difficult
# Recommended Redesign
Use message queues for asynchronous processing
Save notification to DB first
Process email sending separately
Add retry mechanism for failed emails
Use worker services for parallel processing
Use batch processing for scalability
# Why DB Save and Email Should Not Happen Together
Saving to DB and sending emails should be separated because:
Email APIs can fail or become slow
DB operations should remain reliable
Failure in email should not rollback notification storage
Asynchronous processing improves scalability
# Revised Pseudocode
function notify_all(student_ids, message):

    for student_id in student_ids:

        save_to_db(student_id, message)

        add_to_queue({
            "student_id": student_id,
            "message": message
        })
worker_process():

    while queue_not_empty():

        job = get_next_job()

        try:
            send_email(job.student_id, job.message)

            push_to_app(job.student_id, job.message)

        except:
            retry_job(job)
# Stage 6
# The given code to fetch the details from the given api link 
import requests
from datetime import datetime

API_URL = "http://4.224.186.213/evaluation-service/notifications"

weights = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

response = requests.get(API_URL)
notifications = response.json()

current_time = datetime.now()

priority_notifications = []

for notification in notifications:

    notification_type = notification.get("notificationType", "Event")

    weight = weights.get(notification_type, 1)

    created_at = notification.get("createdAt")

    try:
        created_time = datetime.fromisoformat(created_at)
        recency_score = 1 / ((current_time - created_time).seconds + 1)
    except:
        recency_score = 0

    priority_score = weight + recency_score

    notification["priorityScore"] = priority_score

    priority_notifications.append(notification)

priority_notifications.sort(
    key=lambda x: x["priorityScore"],
    reverse=True
)

top_10 = priority_notifications[:10]

print("\nTop 10 Priority Notifications:\n")

for index, notification in enumerate(top_10, start=1):

    print(
        f"{index}. "
        f"{notification.get('notificationType')} - "
        f"{notification.get('message')}"
    )
# Stage 7
![alt text](image-1.png)