import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from database import models, db

def verify_all():
    app = create_app()
    with app.app_context():
        total_q = models.count_questions('all')
        print(f"Total questions in DB: {total_q}")
        assert total_q >= 200, f"Expected >= 200 questions, found {total_q}"

        categories = ['Quantitative', 'Logical Reasoning', 'Verbal Ability', 'Data Interpretation']
        for cat in categories:
            cnt = models.count_questions(cat)
            print(f"  Category '{cat}': {cnt} questions")
            assert cnt >= 50, f"Expected >= 50 questions for '{cat}', found {cnt}"

            # Test random 20 sampling
            sample20 = models.get_random_questions(cat, count=20)
            assert len(sample20) == 20, f"Expected 20 sampled questions for '{cat}', got {len(sample20)}"
            for q in sample20:
                assert len(q.get('options', [])) == 4, f"Question options length != 4: {q.get('_id')}"
                assert 0 <= q.get('answer_index') <= 3, f"Invalid answer index: {q.get('answer_index')}"
                assert q.get('difficulty') == 'hard', f"Difficulty not hard: {q.get('difficulty')}"
                assert len(q.get('explanation', '').strip()) > 0, f"Empty explanation on {q.get('_id')}"

        print("[PASSED] All 4 categories have 50+ high difficulty, valid questions.")

        # Re-seed & verify exams
        models.seed_placement_mock_exams()
        exams = models.list_exams()
        print(f"Total exams configured: {len(exams)}")
        assert len(exams) >= 5, f"Expected at least 5 exams, got {len(exams)}"
        for ex in exams:
            assert ex.get('duration_minutes') == 20, f"Exam {ex.get('name')} duration is {ex.get('duration_minutes')}, expected 20"
            assert ex.get('question_count') == 20, f"Exam {ex.get('name')} question count is {ex.get('question_count')}, expected 20"

        print("[PASSED] All mock exams have duration = 20 minutes and 20 questions.")

        # Test Flask test client API endpoints
        with app.test_client() as client:
            for cat in categories:
                res = client.get(f'/api/questions?topic={cat}&random=true&limit=20')
                assert res.status_code == 200, f"Failed status {res.status_code} for {cat}"
                data = res.get_json()
                assert data['ok'] is True
                assert len(data['questions']) == 20
                print(f"API /api/questions for {cat} returned 20 random questions successfully.")

            # Test /api/exams
            ex_res = client.get('/api/exams')
            assert ex_res.status_code == 200
            ex_data = ex_res.get_json()
            assert ex_data['ok'] is True
            first_exam = ex_data['exams'][0]
            print(f"Verified exam: '{first_exam['name']}' (Duration: {first_exam['duration_minutes']} mins, Count: {first_exam['question_count']})")

    print("\nALL VERIFICATION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    verify_all()
