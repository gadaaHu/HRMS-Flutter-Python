import requests

BASE = "http://localhost:8000/api/v1"
results = []

def check(name, ok, info=""):
    status = "PASS" if ok else "FAIL"
    results.append((name, status, info))
    print(f"[{status}] {name}: {info}")

# Health
r = requests.get("http://localhost:8000")
check("Health check", r.status_code == 200, r.json().get("message"))

# Login
r = requests.post(f"{BASE}/login", json={"email": "test@test.com", "password": "test"})
d = r.json()
token = d.get("data", {}).get("token", "")
check("Login", d.get("success"), "token=" + ("YES" if token else "NO"))
H = {"Authorization": "Bearer " + token}

# Get User
r = requests.get(f"{BASE}/get-user", headers=H)
d = r.json()
user_data = d.get("data", [{}])[0]
check("Get User", d.get("success"), "name=" + user_data.get("first_name", "") + " " + user_data.get("last_name", ""))

# Today Attendance
r = requests.get(f"{BASE}/getTodaysAttendance", headers=H)
check("Todays Attendance", r.json().get("success"), str(r.json().get("data")))

# Get Office
r = requests.get(f"{BASE}/get-office")
check("Get Office", r.json().get("success"), str(len(r.json().get("data", []))) + " locations")

# Leave Status
r = requests.get(f"{BASE}/get-leave-status", headers=H)
check("Leave Status", r.json().get("success"), str(r.json().get("data")))

# Get Leaves
r = requests.get(f"{BASE}/get-leave", headers=H)
check("Get Leaves", r.json().get("success"), str(len(r.json().get("data", []))) + " records")

# Apply Leave
r = requests.post(f"{BASE}/apply-leave", json={"userid": "EMP001", "leave_type": "Sick", "start_date": "2026-09-20", "end_date": "2026-09-21", "reason": "Fever"})
check("Apply Leave", r.json().get("success"), r.json().get("message"))

# Get Attendance
r = requests.get(f"{BASE}/get-attendance", headers=H)
check("Get Attendance", r.json().get("success"), str(len(r.json().get("data", []))) + " records")

# Regularization
r = requests.post(f"{BASE}/apply-regularization", json={"userid": "EMP001", "date": "2026-09-10", "intime": "09:30", "outtime": "18:30", "reason": "System issue"})
check("Apply Regularization", r.json().get("success"), r.json().get("message"))

r = requests.get(f"{BASE}/get-regularization", headers=H)
check("Get Regularization", r.json().get("success"), str(len(r.json().get("data", []))) + " records")

# Reimbursement
r = requests.get(f"{BASE}/get-reimbursement", headers=H)
check("Get Reimbursement", r.json().get("success"))

# Resignation
r = requests.get(f"{BASE}/get-resign", headers=H)
check("Get Resignation", r.json().get("success"))

# Holidays
r = requests.get(f"{BASE}/get-holidays")
check("Get Holidays", r.json().get("success"), str(len(r.json().get("data", []))) + " holidays")

# Notifications
r = requests.get(f"{BASE}/get-user-notification", headers=H)
check("Get Notifications", r.json().get("success"))

# Working Days
r = requests.get(f"{BASE}/getWorkingDays", headers=H)
check("Working Days", r.json().get("success"), str(r.json().get("data")))

print()
passed = sum(1 for _, s, _ in results if s == "PASS")
print(f"Result: {passed}/{len(results)} tests passed")
