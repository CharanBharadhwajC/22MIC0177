# Stage 1
## REST APIs
### GET /notifications
Fetch notifications for user
### POST /notifications
Create notification
### PUT /notifications/{id}/read
Mark notification as read
### DELETE /notifications/{id}
Delete notification
## Real-time Design
Use WebSockets for real-time delivery.
---
# Stage 2
## Database Choice
PostgreSQL
## Tables
notifications
- id
- studentId
- type
- message
- isRead
- createdAt
Indexes:
- studentId
- createdAt
---
# Stage 3
## Problem
Query performs full table scan.
## Solution
Composite index:
(studentId, isRead, createdAt)
## Query
SELECT *
FROM notifications
WHERE notificationType = 'Placement'
AND createdAt >= NOW() - INTERVAL '7 days';
---
# Stage 4
## Performance Improvements
- Redis caching
- Pagination
- Lazy loading
- Background workers
- WebSockets
Tradeoff:
More infrastructure complexity.
---
# Stage 5
## Problems
- Sequential processing
- Failure inconsistency
- Slow execution
## Better Design
Use queue-based asynchronous processing.
Steps:
1. Save notification
2. Push to queue
3. Workers send email
4. Retry failed jobs
---
# Stage 6
## Priority Inbox
Use Max Heap.
Priority:
Placement > Result > Event
Recent notifications get higher priority.
Complexity:
Insertion: O(log n)
Top 10 retrieval: O(k log n)