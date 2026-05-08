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