import requests, json, time

BASE = "https://supercareer-backend-1.onrender.com"
EMAIL = f"bilal_final_test_{int(time.time())}@example.com"
PASS = "TestPass123!"

def print_res(name, r):
    print(f"\n--- {name} [{r.status_code}] ---")
    try:
        print(json.dumps(r.json(), indent=2, ensure_ascii=False))
    except:
        print(r.text[:200])

# 1. Register
r_reg = requests.post(f"{BASE}/api/register/", json={
    "email": EMAIL,
    "password": PASS,
    "full_name": "Bilal Live Tester",
    "role": "job_seeker"
})
print_res("Register", r_reg)
access = r_reg.json()['tokens']['access']

headers = {"Authorization": f"Bearer {access}"}

# 2. Update Profile
r_prof = requests.patch(f"{BASE}/api/profile/", headers=headers, json={
    "bio": "Expert Python developer with 5 years of experience in Django and React.",
    "specialization": "Full Stack Developer",
    "location": "Cairo, Egypt"
})
print_res("Update Profile", r_prof)

# 3. Get Jobs (to get an ID for matching/proposal)
r_jobs = requests.get(f"{BASE}/api/opportunities/jobs/", headers=headers)
print_res("List Jobs", r_jobs)
job_id = r_jobs.json()[0]['id'] if r_jobs.json() else None

# 4. AI Matching
r_match = requests.get(f"{BASE}/api/matching/", headers=headers)
print_res("AI Matching (Mock Mode)", r_match)

# 5. Create Proposal
if job_id:
    r_prop = requests.post(f"{BASE}/api/documents/cv/create/", headers=headers, json={
        "job": job_id,
        "ats_score": 85.5,
        "feedback": "Great match for the role!"
    })
    print_res("Create Proposal/CV Record", r_prop)

# 6. Dashboard Stats
r_dash = requests.get(f"{BASE}/api/accounts/dashboard-stats/", headers=headers)
print_res("Dashboard Stats", r_dash)
