import requests, json, time, random, string

BASE = "https://supercareer-backend-1.onrender.com"
uid = ''.join(random.choices(string.ascii_lowercase, k=6))
EMAIL = f"test_{uid}@example.com"
PASS = "TestPass123!"
refresh_token = ""

results = []

def test(name, method, path, expected, **kwargs):
    url = f"{BASE}{path}"
    try:
        r = getattr(requests, method)(url, timeout=40, **kwargs)
        ok = r.status_code == expected
        status = "PASS" if ok else "FAIL"
        try: body = r.json()
        except: body = r.text[:120]
        results.append((status, r.status_code, name, body))
        print(f"{status} [{r.status_code}] {name}")
        if not ok or isinstance(body, dict):
            print(f"     {json.dumps(body, ensure_ascii=False)[:200]}" if isinstance(body, dict) else f"     {body[:100]}")
        return r
    except Exception as e:
        results.append(("FAIL", "ERR", name, str(e)))
        print(f"FAIL [ERR] {name}: {e}")
        return None

# ── Auth ──────────────────────────────────────────────────────────────────────
r = test("Register", "post", "/api/register/", 201, json={
    "email": EMAIL, "password": PASS, "full_name": "Test User", "role": "job_seeker"
})
access = r.json()["tokens"]["access"] if r else ""
refresh_token = r.json()["tokens"]["refresh"] if r else ""
h = {"Authorization": f"Bearer {access}"}

test("Login", "post", "/api/login/", 200, json={"email": EMAIL, "password": PASS})
test("Token Refresh - no token (400)", "post", "/api/token/refresh/", 400, json={})

# ── Profile ───────────────────────────────────────────────────────────────────
test("Get Profile", "get", "/api/profile/", 200, headers=h)
test("Update Profile", "patch", "/api/profile/", 200, headers=h, json={
    "bio": "Python Developer", "specialization": "Backend"
})
test("Change Password", "post", "/api/change-password/", 200, headers=h, json={
    "old_password": PASS, "new_password": "NewPass456!", "confirm_password": "NewPass456!"
})
test("Dashboard Stats", "get", "/api/accounts/dashboard-stats/", 200, headers=h)

# ── Password Reset ────────────────────────────────────────────────────────────
test("Forgot Password (real email)", "post", "/api/forgot-password/", 200, json={"email": EMAIL})
test("Verify OTP - wrong code (400)", "post", "/api/verify-otp/", 400, json={"email": EMAIL, "otp": "0000"})
test("Reset Password - unverified (401)", "post", "/api/reset-password/", 401, json={
    "email": EMAIL, "otp": "0000", "new_password": "NewPass789!", "confirm_new_password": "NewPass789!"
})

# ── Google Auth ───────────────────────────────────────────────────────────────
test("Google Login - invalid token (400)", "post", "/api/auth/google/login/", 400, json={"token": "fake_google_token"})
test("Google Register - invalid token (400)", "post", "/api/auth/google/register/", 400, json={"token": "fake_google_token"})

# ── Opportunities ─────────────────────────────────────────────────────────────
test("List Jobs", "get", "/api/opportunities/jobs/", 200, headers=h)
test("List Projects", "get", "/api/opportunities/projects/", 200, headers=h)
test("Refresh Projects (no scraper = 500)", "post", "/api/opportunities/refresh/", 500, headers=h)

# ── Matching ──────────────────────────────────────────────────────────────────
test("AI Matching", "get", "/api/matching/", 200, headers=h)

# ── Documents ─────────────────────────────────────────────────────────────────
test("Proposal History", "get", "/api/documents/proposals/", 200, headers=h)

# ── Notifications ─────────────────────────────────────────────────────────────
test("List Notifications", "get", "/api/notifications/", 200, headers=h)

# ── Docs / Admin ──────────────────────────────────────────────────────────────
test("Swagger UI", "get", "/api/docs/", 200)
test("Admin Stats - no perm (403)", "get", "/api/admin-tools/stats/", 403, headers=h)
test("Logout", "post", "/api/logout/", 200, headers=h, json={"refresh": refresh_token})

# ── Summary ───────────────────────────────────────────────────────────────────
passed = sum(1 for r in results if r[0] == "PASS")
print(f"\n{'='*60}")
print(f"TOTAL: {len(results)} | PASSED: {passed} | FAILED: {len(results)-passed}")
print("="*60)
for status, code, name, _ in results:
    print(f"  {status} [{code}] {name}")
