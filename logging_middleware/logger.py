import requests
BASE_URL = "http://4.224.186.213/evaluation-service"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJjaGFyYW4yYWpqdWNoYXJhbkBnbWFpbC5jb20iLCJleHAiOjE3Nzg5Mjk5MDYsImlhdCI6MTc3ODkyOTAwNiwiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjFhYWUwZjkzLTk1YjMtNGYyZS1iMDE5LTI3MDY5NzE5OTY1ZiIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImNoYXJhbiBiaGFyYWRod2FqIGMiLCJzdWIiOiIyMmY3ZGZjNi03YzlmLTQzMTYtYWUwOC03NDg2OGM2MDBhOTYifSwiZW1haWwiOiJjaGFyYW4yYWpqdWNoYXJhbkBnbWFpbC5jb20iLCJuYW1lIjoiY2hhcmFuIGJoYXJhZGh3YWogYyIsInJvbGxObyI6IjIybWljMDE3NyIsImFjY2Vzc0NvZGUiOiJTZkZ1V2ciLCJjbGllbnRJRCI6IjIyZjdkZmM2LTdjOWYtNDMxNi1hZTA4LTc0ODY4YzYwMGE5NiIsImNsaWVudFNlY3JldCI6IndEdWJSem1kck5HQmdnYm4ifQ.CV6ocSiqNUnz6emDQPC4CNKtn53vV4G_Wdx-VEh0Oe8"
def Log(stack, level, package, message):
    url = f"{BASE_URL}/logs"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(response.status_code)
        print(response.text)
    except Exception as e:
        print("Logging Error:", str(e))