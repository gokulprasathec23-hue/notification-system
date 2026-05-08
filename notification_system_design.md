# Stage 1
## Notification System Overview
This system allows users to receive and manage notifications.
## Core Actions
- Create notification
- Fetch notifications
- Mark notification as read
- Delete notification
- Real-time notifications
## REST API Endpoints
### GET /api/notifications
### POST /api/notifications
### PATCH /api/notifications/{id}/read
### DELETE /api/notifications/{id}
## Notification JSON Schema
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