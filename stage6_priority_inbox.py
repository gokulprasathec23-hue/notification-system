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