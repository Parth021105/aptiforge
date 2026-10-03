from app import create_app
from database.db import get_db

app = create_app()
with app.app_context():
    db = get_db()
    if db is None:
        print("Database connection failed.")
        exit(1)

    # 1. Delete all student and faculty accounts
    del_res = db.users.delete_many({'role': {'$in': ['student', 'faculty']}})
    print(f"Removed {del_res.deleted_count} student & faculty accounts.")

    # 2. Clear stale exam sessions
    sess_res = db.exam_sessions.delete_many({})
    print(f"Cleared {sess_res.deleted_count} test sessions.")

    # 3. List remaining admin accounts
    admins = list(db.users.find({}, {'password': 0}))
    print(f"\nRemaining active accounts ({len(admins)}):")
    for a in admins:
        name = a.get('name', 'Admin')
        email = a.get('email')
        role = a.get('role')
        print(f"  - {name} | {email} | [{role}]")
