from flask import Flask, jsonify
import requests
import heapq
from logging_middleware.logger import Log
app = Flask(__name__)
BASE_URL = "http://4.224.186.213/evaluation-service"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJjaGFyYW4yYWpqdWNoYXJhbkBnbWFpbC5jb20iLCJleHAiOjE3Nzg5MzExNzcsImlhdCI6MTc3ODkzMDI3NywiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjMxYmFhOTNiLWM4YzktNDVmZi1hNjRlLTlmOTMyNzhiNTFkMiIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImNoYXJhbiBiaGFyYWRod2FqIGMiLCJzdWIiOiIyMmY3ZGZjNi03YzlmLTQzMTYtYWUwOC03NDg2OGM2MDBhOTYifSwiZW1haWwiOiJjaGFyYW4yYWpqdWNoYXJhbkBnbWFpbC5jb20iLCJuYW1lIjoiY2hhcmFuIGJoYXJhZGh3YWogYyIsInJvbGxObyI6IjIybWljMDE3NyIsImFjY2Vzc0NvZGUiOiJTZkZ1V2ciLCJjbGllbnRJRCI6IjIyZjdkZmM2LTdjOWYtNDMxNi1hZTA4LTc0ODY4YzYwMGE5NiIsImNsaWVudFNlY3JldCI6IndEdWJSem1kck5HQmdnYm4ifQ.hic_eMWWK9mI74ofvKEkZALCjnHqqXD1ruO7cry_58c"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}
def calculate_priority(notification):
    priority_map = {
        "Placement": 3,
        "Result": 2,
        "Event": 1
    }
    return priority_map.get(notification["Type"], 0)
@app.route('/top-notifications', methods=['GET'])
def top_notifications():
    try:
        Log("backend", "info", "route", "Fetching notifications")
        response = requests.get(
            f"{BASE_URL}/notifications",
            headers=headers
        )
        notifications = response.json()["notifications"]
        heap = []
        for notification in notifications:
            priority = calculate_priority(notification)
            heapq.heappush(heap, (
                -priority,
                notification["Timestamp"],
                notification
            ))
        top_10 = []
        for _ in range(min(10, len(heap))):
            top_10.append(heapq.heappop(heap)[2])
        Log("backend", "info", "service", "Top notifications generated")
        return jsonify(top_10), 200
    except Exception as e:
        Log("backend", "error", "handler", str(e))
        return jsonify({
            "error": str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True, port=5001)