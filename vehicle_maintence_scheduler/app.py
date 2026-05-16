from flask import Flask, jsonify
import requests
from vehicle_maintence_scheduler.knapsack import solve_knapsack
from logging_middleware.logger import Log
app = Flask(__name__)
BASE_URL = "http://4.224.186.213/evaluation-service"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiJjaGFyYW4yYWpqdWNoYXJhbkBnbWFpbC5jb20iLCJleHAiOjE3Nzg5MzExNzcsImlhdCI6MTc3ODkzMDI3NywiaXNzIjoiQWZmb3JkIE1lZGljYWwgVGVjaG5vbG9naWVzIFByaXZhdGUgTGltaXRlZCIsImp0aSI6IjMxYmFhOTNiLWM4YzktNDVmZi1hNjRlLTlmOTMyNzhiNTFkMiIsImxvY2FsZSI6ImVuLUlOIiwibmFtZSI6ImNoYXJhbiBiaGFyYWRod2FqIGMiLCJzdWIiOiIyMmY3ZGZjNi03YzlmLTQzMTYtYWUwOC03NDg2OGM2MDBhOTYifSwiZW1haWwiOiJjaGFyYW4yYWpqdWNoYXJhbkBnbWFpbC5jb20iLCJuYW1lIjoiY2hhcmFuIGJoYXJhZGh3YWogYyIsInJvbGxObyI6IjIybWljMDE3NyIsImFjY2Vzc0NvZGUiOiJTZkZ1V2ciLCJjbGllbnRJRCI6IjIyZjdkZmM2LTdjOWYtNDMxNi1hZTA4LTc0ODY4YzYwMGE5NiIsImNsaWVudFNlY3JldCI6IndEdWJSem1kck5HQmdnYm4ifQ.hic_eMWWK9mI74ofvKEkZALCjnHqqXD1ruO7cry_58c"
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
@app.route('/')
def home():
    return jsonify({
        "message": "Vehicle Maintenance Scheduler Running"
    }), 200
@app.route('/optimize', methods=['GET'])
def optimize():
    try:
        Log("backend", "info", "route", "Fetching depots")
        depots_response = requests.get(
            f"{BASE_URL}/depots",
            headers=headers
        )
        print("DEPOTS STATUS:", depots_response.status_code)
        print("DEPOTS RESPONSE:", depots_response.text)
        if depots_response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch depots",
                "response": depots_response.text
            }), depots_response.status_code
        depots_json = depots_response.json()
        if "depots" not in depots_json:
            return jsonify({
                "error": "Depots key missing",
                "response": depots_json
            }), 500
        depots = depots_json["depots"]
        Log("backend", "info", "route", "Fetching vehicles")
        vehicles_response = requests.get(
            f"{BASE_URL}/vehicles",
            headers=headers
        )
        print("VEHICLES STATUS:", vehicles_response.status_code)
        print("VEHICLES RESPONSE:", vehicles_response.text)
        if vehicles_response.status_code != 200:
            return jsonify({
                "error": "Failed to fetch vehicles",
                "response": vehicles_response.text
            }), vehicles_response.status_code
        vehicles_json = vehicles_response.json()
        if "vehicles" not in vehicles_json:
            return jsonify({
                "error": "Vehicles key missing",
                "response": vehicles_json
            }), 500
        vehicles = vehicles_json["vehicles"]
        result = []
        for depot in depots:
            capacity = depot.get("MechanicHours", 0)
            selected_tasks, total_impact = solve_knapsack(
                vehicles,
                capacity
            )
            result.append({
                "depot_id": depot.get("ID"),
                "mechanic_hours": capacity,
                "total_impact": total_impact,
                "selected_tasks": selected_tasks
            })
        Log("backend", "info", "service", "Optimization completed")
        return jsonify(result), 200
    except Exception as e:
        Log("backend", "error", "handler", str(e))
        return jsonify({
            "error": str(e)
        }), 500
if __name__ == '__main__':
    app.run(debug=True)