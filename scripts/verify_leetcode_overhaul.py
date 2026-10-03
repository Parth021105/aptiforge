import requests
import sys

# Force UTF-8 encoding for Windows stdout
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:5000"

def test_all():
    print("=== STARTING APTIFORGE LEETCODE OVERHAUL VERIFICATION ===")
    session = requests.Session()

    # 1. Test Student Login & Boundary
    print("\n--- 1. Testing Student Authentication & Boundaries ---")
    login_res = session.post(f"{BASE_URL}/api/login", json={
        "email": "student@aptiforge.com",
        "password": "password123"
    })
    assert login_res.status_code == 200, f"Student login failed: {login_res.text}"
    login_data = login_res.json()
    print(f"Student Login Response: ok={login_data.get('ok')}, role={login_data.get('role')}, redirect={login_data.get('redirect')}")
    assert login_data.get('role') == 'student'
    assert login_data.get('redirect') == '/dashboard'

    # Student accessing /dashboard
    dash_res = session.get(f"{BASE_URL}/dashboard")
    assert dash_res.status_code == 200
    assert "Student Dashboard" in dash_res.text or "Welcome back" in dash_res.text
    print("[PASS] Student Dashboard renders correctly.")

    # Student trying to access /admin -> must be rejected (403 or forbidden)
    admin_attempt = session.get(f"{BASE_URL}/admin")
    assert admin_attempt.status_code in (403, 302), f"Student was not blocked from /admin: {admin_attempt.status_code}"
    print(f"[PASS] Student access to /admin properly blocked: HTTP {admin_attempt.status_code}")

    # 2. Test Admin Login & Dedicated Workspace
    print("\n--- 2. Testing Admin Authentication & Command Center ---")
    admin_session = requests.Session()
    admin_login_res = admin_session.post(f"{BASE_URL}/api/login", json={
        "email": "admin@aptiforge.com",
        "password": "admin123"
    })
    assert admin_login_res.status_code == 200, f"Admin login failed: {admin_login_res.text}"
    admin_data = admin_login_res.json()
    print(f"Admin Login Response: ok={admin_data.get('ok')}, role={admin_data.get('role')}, redirect={admin_data.get('redirect')}")
    assert admin_data.get('role') == 'admin'
    assert admin_data.get('redirect') == '/admin'

    # Admin accessing /dashboard -> should redirect to /admin
    admin_dash_res = admin_session.get(f"{BASE_URL}/dashboard", allow_redirects=False)
    assert admin_dash_res.status_code in (302, 301), f"Admin was not redirected from /dashboard: {admin_dash_res.status_code}"
    print(f"[PASS] Admin navigating to /dashboard is strictly redirected to /admin (HTTP {admin_dash_res.status_code})")

    # Admin accessing /admin
    admin_page_res = admin_session.get(f"{BASE_URL}/admin")
    assert admin_page_res.status_code == 200
    assert "System Command Center" in admin_page_res.text
    assert "ADMIN PRIVILEGES" in admin_page_res.text
    assert "Question Repository" in admin_page_res.text
    print("[PASS] Admin Command Center rendered with full privilege panels and KPIs.")

    # 3. Test Admin Stats API
    stats_res = admin_session.get(f"{BASE_URL}/api/admin/stats")
    assert stats_res.status_code == 200
    stats = stats_res.json().get('stats', {})
    print(f"[PASS] Live Admin KPIs: Students={stats.get('total_students')}, Questions={stats.get('total_questions')}, Exams={stats.get('total_exams')}, Submissions={stats.get('total_attempts')}")
    assert stats.get('total_questions', 0) >= 200

    # 4. Test Multi-Level Progressive Hints
    print("\n--- 3. Testing 3-Level Progressive Hints System ---")
    q_res = session.get(f"{BASE_URL}/api/questions?random=true&limit=5")
    assert q_res.status_code == 200
    q_data = q_res.json()
    assert len(q_data.get('questions', [])) > 0
    sample_q = q_data['questions'][0]
    qid = sample_q['_id']
    print(f"Inspecting Question: [{sample_q.get('topic')}] {sample_q.get('question')[:60]}...")

    for lvl in [1, 2, 3]:
      hint_res = session.post(f"{BASE_URL}/api/get-hint", json={"question_id": qid, "level": lvl})
      assert hint_res.status_code == 200
      h_text = hint_res.json().get('hint', '')
      assert len(h_text) > 20, f"Hint level {lvl} is too short!"
      print(f"[PASS] Level {lvl} Hint length: {len(h_text)} chars")
      print(f"   Preview: {h_text[:90].strip()}...")

    # 5. Test Question Inspection API
    print("\n--- 4. Testing Question Inspection Detail API ---")
    inspect_res = admin_session.get(f"{BASE_URL}/api/questions/{qid}")
    assert inspect_res.status_code == 200
    q_detail = inspect_res.json().get('question', {})
    assert 'hint_l1' in q_detail and 'hint_l2' in q_detail and 'explanation' in q_detail
    print(f"[PASS] Question {qid} contains hint_l1, hint_l2, and explanation.")

    # 6. Test LeetCode Practice Page HTML Elements
    print("\n--- 5. Testing LeetCode Workspace UI Elements ---")
    practice_res = session.get(f"{BASE_URL}/practice")
    assert practice_res.status_code == 200
    html = practice_res.text
    assert "lc-workspace" in html
    assert "hint-accordion" in html
    assert "acc-hint-1" in html
    assert "acc-hint-2" in html
    assert "acc-hint-3" in html
    assert "lc-console" in html
    print("[PASS] Practice page contains LeetCode workspace, collapsible hint accordions, and verdict console.")

    print("\n=== ALL VERIFICATION TESTS PASSED SUCCESSFULLY! ===")

if __name__ == '__main__':
    test_all()
