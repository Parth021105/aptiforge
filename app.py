from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from config import Config
from database.db import mongo, init_db
from database import models
from services.ai_service import get_hint_for_question
import os
import json

def create_app():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app = Flask(
        __name__,
        static_folder=os.path.join(basedir, 'static'),
        template_folder=os.path.join(basedir, 'templates')
    )
    app.config.from_object(Config)
    init_db(app)

    # Auto-seed sample questions if question collection is empty or outdated
    with app.app_context():
        try:
            if models.count_questions('all') < 50:
                sample_path = os.path.join(os.path.dirname(__file__), 'database', 'sample_questions.json')
                if os.path.exists(sample_path):
                    with open(sample_path, 'r', encoding='utf-8') as f:
                        q_data = json.load(f)
                    db = models.get_db()
                    if db is not None:
                        db.questions.delete_many({})
                    models.insert_questions(q_data)
                    models.seed_placement_mock_exams()
                    app.logger.info("Auto-seeded comprehensive question bank (200+ questions).")
        except Exception as e:
            app.logger.warning(f"Auto-seed check skipped: {e}")

    # Authentication decorators
    def login_required(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*a, **kw):
            uid = session.get('user_id')
            if not uid:
                return redirect(url_for('login_page'))
            user = models.get_user_by_id(uid)
            if not user:
                session.clear()
                return redirect(url_for('login_page'))
            session['role'] = user.get('role', 'student')
            session['user_name'] = user.get('name', 'User')
            session['user_email'] = user.get('email', '')
            return fn(*a, **kw)
        return wrapper

    def admin_required(fn):
        from functools import wraps
        @wraps(fn)
        def wrapper(*a, **kw):
            uid = session.get('user_id')
            if not uid:
                return redirect(url_for('login_page'))
            user = models.get_user_by_id(uid)
            if not user or user.get('role') not in ('admin', 'faculty'):
                return render_template('login.html', error="Faculty or Admin privileges required. Access denied."), 403
            session['role'] = user.get('role', 'faculty')
            session['user_name'] = user.get('name', 'Faculty/Admin')
            return fn(*a, **kw)
        return wrapper

    # --- HTML Page Routes ---
    @app.route('/')
    def home():
        if session.get('user_id'):
            return redirect(url_for('dashboard'))
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        if session.get('user_id'):
            return redirect(url_for('dashboard'))
        return render_template('login.html')

    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('login_page'))

    @app.route('/dashboard')
    @login_required
    def dashboard():
        role = session.get('role', 'student')
        user_id = session.get('user_id')
        user = models.get_user_by_id(user_id)

        # Strictly redirect admin and faculty away from student dashboard to Admin/Faculty Command Center
        if role in ('admin', 'faculty'):
            return redirect(url_for('admin_page'))
        
        analytics = models.analytics_summary_for_user(user_id)
        return render_template('dashboard_student.html', user=user, analytics=analytics)

    @app.route('/practice')
    @login_required
    def practice_page():
        return render_template('practice.html')

    @app.route('/exam')
    @login_required
    def exam_page():
        return render_template('exam.html')

    @app.route('/analytics')
    @login_required
    def analytics_page():
        return render_template('analytics.html')

    @app.route('/admin')
    @login_required
    @admin_required
    def admin_page():
        admin_stats = models.admin_analytics_summary()
        return render_template('admin.html', admin_stats=admin_stats)

    # --- API Endpoints ---
    @app.route('/api/register', methods=['POST'])
    def api_register():
        data = request.get_json() or {}
        name = data.get('name', '')
        email = data.get('email', '')
        password = data.get('password', '')
        role = data.get('role', 'student')

        if not email or not password:
            return jsonify({'ok': False, 'error': 'Email and password required'}), 400

        existing = models.find_user_by_email(email)
        if existing:
            return jsonify({'ok': False, 'error': 'User with this email already exists'}), 400

        res = models.create_user(name, email, password, role=role)
        if not res:
            return jsonify({'ok': False, 'error': 'Database error creating user'}), 500

        return jsonify({'ok': True, 'user_id': str(res.inserted_id)})

    @app.route('/api/login', methods=['POST'])
    def api_login():
        data = request.get_json() or {}
        email = data.get('email', '')
        password = data.get('password', '')

        # Auto-create demo admin if requested and not present
        if email.lower() == 'admin@aptiforge.com' and not models.find_user_by_email(email):
            models.create_user('Prof. Rajesh Kumar', 'admin@aptiforge.com', 'admin123', role='admin')

        # Auto-create demo faculty if requested and not present
        if email.lower() == 'faculty@aptiforge.com' and not models.find_user_by_email(email):
            models.create_user('Prof. Sharma (Faculty)', 'faculty@aptiforge.com', 'faculty123', role='faculty')

        # Auto-create demo student if requested and not present
        if email.lower() == 'student@aptiforge.com' and not models.find_user_by_email(email):
            models.create_user('Aarav Sharma', 'student@aptiforge.com', 'password123', role='student')

        user = models.find_user_by_email(email)
        if not user:
            return jsonify({'ok': False, 'error': 'Invalid credentials'}), 401

        from werkzeug.security import check_password_hash
        stored_hash = user.get('password', '')
        password_valid = False
        try:
            password_valid = check_password_hash(stored_hash, password)
        except Exception:
            password_valid = (stored_hash == password)

        if not password_valid:
            return jsonify({'ok': False, 'error': 'Invalid credentials'}), 401

        session['user_id'] = str(user['_id'])
        session['role'] = user.get('role', 'student')
        session['user_name'] = user.get('name', 'User')
        session['user_email'] = user.get('email', '')

        redirect_url = '/admin' if session['role'] in ('admin', 'faculty') else '/dashboard'

        return jsonify({
            'ok': True,
            'role': session['role'],
            'redirect': redirect_url
        })

    @app.route('/api/questions', methods=['GET'])
    def api_list_questions():
        topic = request.args.get('topic', 'all')
        difficulty = request.args.get('difficulty', 'all')
        search = request.args.get('search')
        random_flag = request.args.get('random', 'false').lower() in ('true', '1', 'yes')
        limit = int(request.args.get('limit', 20 if random_flag else 250))
        target_topic = None if topic.lower() == 'all' else topic

        if random_flag:
            if difficulty.lower() == 'mixed':
                questions = models.get_test_questions(category_or_topic=target_topic, difficulty='mixed', count=limit)
            elif difficulty.lower() in ('easy', 'medium', 'hard'):
                questions = models.get_test_questions(category_or_topic=target_topic, difficulty=difficulty.lower(), count=limit)
            else:
                questions = models.get_test_questions(category_or_topic=target_topic, difficulty='mixed', count=limit)
        else:
            questions = models.list_questions(topic=topic, difficulty=difficulty, search=search, limit=limit, random_sample=False)

        return jsonify({'ok': True, 'questions': questions, 'count': len(questions)})

    @app.route('/api/questions/<qid>', methods=['GET'])
    def api_get_question_detail(qid):
        question = models.get_question(qid)
        if not question:
            return jsonify({'ok': False, 'error': 'Question not found'}), 404
        return jsonify({'ok': True, 'question': question})

    @app.route('/api/verify-answer', methods=['POST'])
    def api_verify_answer():
        data = request.get_json() or {}
        qid = data.get('question_id')
        selected = data.get('selected_index')

        if qid is None or selected is None:
            return jsonify({'ok': False, 'error': 'Missing question_id or selected_index'}), 400

        user_id = session.get('user_id')
        is_correct, correct_index, explanation = models.verify_answer(qid, int(selected), user_id=user_id)
        return jsonify({
            'ok': True,
            'is_correct': is_correct,
            'correct_index': correct_index,
            'explanation': explanation
        })

    @app.route('/api/get-hint', methods=['POST'])
    def api_get_hint():
        data = request.get_json() or {}
        qid = data.get('question_id')
        level = int(data.get('level', 1))

        if not qid:
            return jsonify({'ok': False, 'error': 'Missing question_id'}), 400

        question = models.get_question(qid)
        if not question:
            return jsonify({'ok': False, 'error': 'Question not found'}), 404

        hint = get_hint_for_question(question, level=level)
        return jsonify({'ok': True, 'hint': hint, 'level': level})

    @app.route('/api/upload-questions', methods=['POST'])
    def api_upload_questions():
        if session.get('role') not in ('admin', 'faculty'):
            return jsonify({'ok': False, 'error': 'Forbidden: Faculty or Admin access required'}), 403

        file = request.files.get('file')
        topic = request.form.get('topic') or 'Quantitative'
        difficulty = request.form.get('difficulty') or 'medium'
        questions = []

        if file:
            filename = file.filename.lower()
            content = file.read()
            try:
                if filename.endswith('.pdf'):
                    from services.pdf_service import parse_questions_from_pdf
                    questions = parse_questions_from_pdf(content, default_topic=topic, default_difficulty=difficulty)
                    if not questions:
                        return jsonify({'ok': False, 'error': 'No questions could be extracted from this PDF. Please verify standard question formatting (e.g. 1. Question, A) ... B) ... Answer: C).'}), 400
                elif filename.endswith('.json'):
                    questions = json.loads(content.decode('utf-8'))
                elif filename.endswith('.csv'):
                    import csv, io
                    text = io.StringIO(content.decode('utf-8'))
                    reader = csv.DictReader(text)
                    for row in reader:
                        opts = row.get('options', '')
                        options = [o.strip() for o in opts.split('|')] if opts else []
                        q = {
                            'question': row.get('question'),
                            'options': options,
                            'answer_index': int(row.get('answer_index') or 0),
                            'topic': row.get('topic') or topic,
                            'difficulty': row.get('difficulty') or difficulty,
                            'explanation': row.get('explanation') or ''
                        }
                        questions.append(q)
                else:
                    return jsonify({'ok': False, 'error': 'Unsupported file format. Please upload .pdf, .json, or .csv'}), 400
            except Exception as e:
                return jsonify({'ok': False, 'error': f"Parsing error: {str(e)}"}), 400
        else:
            body = request.get_json() or {}
            if isinstance(body, list):
                questions = body
            else:
                questions = body.get('questions', [])

        inserted = models.insert_questions(questions)
        return jsonify({'ok': True, 'inserted': inserted, 'count': len(questions)})

    @app.route('/api/admin/questions/<qid>', methods=['DELETE'])
    def api_delete_question(qid):
        if session.get('role') not in ('admin', 'faculty'):
            return jsonify({'ok': False, 'error': 'Forbidden: Faculty or Admin access required'}), 403
        success = models.delete_question(qid)
        return jsonify({'ok': success})

    @app.route('/api/create-exam', methods=['POST'])
    def api_create_exam():
        if session.get('role') not in ('admin', 'faculty'):
            return jsonify({'ok': False, 'error': 'Forbidden: Faculty or Admin access required'}), 403

        body = request.get_json() or {}
        name = body.get('name')
        qids = body.get('question_ids', [])
        duration = body.get('duration_minutes', 30)
        enable_hints = body.get('enable_hints', True)

        if not name or not qids:
            return jsonify({'ok': False, 'error': 'Missing exam title or question list'}), 400

        eid = models.insert_exam(name, qids, duration, enable_hints, created_by=session.get('user_id'))
        return jsonify({'ok': True, 'exam_id': eid})

    @app.route('/api/create-demo-exam', methods=['POST'])
    def api_create_demo_exam():
        count = models.seed_placement_mock_exams()
        return jsonify({'ok': True, 'count': count})

    @app.route('/api/exams', methods=['GET'])
    def api_list_exams():
        exams = models.list_exams()
        # Auto-seed 12 placement mock exams if fewer than 3 exist
        if len(exams) < 3:
            models.seed_placement_mock_exams()
            exams = models.list_exams()
        return jsonify({'ok': True, 'exams': exams})

    @app.route('/api/get-exam/<exam_id>', methods=['GET'])
    def api_get_exam(exam_id):
        session_id = request.args.get('session_id')
        ex = models.get_exam(exam_id, session_id=session_id)
        if not ex:
            return jsonify({'ok': False, 'error': 'Exam not found'}), 404
        return jsonify({'ok': True, 'exam': ex})

    @app.route('/api/start-exam', methods=['POST'])
    def api_start_exam():
        body = request.get_json() or {}
        exam_id = body.get('exam_id')
        difficulty = body.get('difficulty', 'mixed')
        user_id = session.get('user_id')
        if not user_id:
            student = models.find_user_by_email('student@aptiforge.com')
            if not student:
                models.create_user('Aarav Sharma', 'student@aptiforge.com', 'password123', role='student')
                student = models.find_user_by_email('student@aptiforge.com')
            if student:
                user_id = str(student['_id'])
                session['user_id'] = user_id
                session['role'] = 'student'
                session['user_name'] = student.get('name', 'Student')

        if not user_id or not exam_id:
            return jsonify({'ok': False, 'error': 'Missing user or exam ID'}), 400
        sid = models.create_exam_session(user_id, exam_id, difficulty=difficulty)
        if not sid:
            return jsonify({'ok': False, 'error': 'Could not initialize exam session in database'}), 500
        ex = models.get_exam(exam_id, session_id=sid)
        if not ex:
            return jsonify({'ok': False, 'error': 'Could not load exam questions'}), 404
        return jsonify({'ok': True, 'session_id': sid, 'exam': ex, 'difficulty': difficulty})

    @app.route('/api/submit-exam', methods=['POST'])
    def api_submit_exam():
        body = request.get_json() or {}
        session_id = body.get('session_id')
        answers = body.get('answers', {})
        time_spent = body.get('time_taken_seconds', 0)

        if not session_id or not isinstance(answers, dict):
            return jsonify({'ok': False, 'error': 'Invalid session or submission format'}), 400

        result = models.submit_exam_and_score(session_id, answers, time_taken_seconds=time_spent)
        if not result:
            return jsonify({'ok': False, 'error': 'Unable to score exam submission'}), 500

        return jsonify({'ok': True, 'result': result})

    @app.route('/api/student/analytics', methods=['GET'])
    def api_student_analytics():
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'ok': False, 'error': 'Unauthorized'}), 401
        res = models.analytics_summary_for_user(user_id)
        return jsonify({'ok': True, 'summary': res})

    @app.route('/api/admin/stats', methods=['GET'])
    def api_admin_stats():
        if session.get('role') not in ('admin', 'faculty'):
            return jsonify({'ok': False, 'error': 'Forbidden: Faculty or Admin access required'}), 403
        stats = models.admin_analytics_summary()
        return jsonify({'ok': True, 'stats': stats})

    @app.route('/api/admin/results', methods=['GET'])
    def api_admin_results():
        if session.get('role') not in ('admin', 'faculty'):
            return jsonify({'ok': False, 'error': 'Forbidden: Faculty or Admin access required'}), 403
        results = models.get_all_results()
        return jsonify({'ok': True, 'results': results})

    @app.route('/api/seed-sample', methods=['POST'])
    def api_seed_sample():
        sample_path = os.path.join(os.path.dirname(__file__), 'database', 'sample_questions.json')
        try:
            with open(sample_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            db = models.get_db()
            if db is not None:
                db.questions.delete_many({})
            inserted = models.insert_questions(data)
            models.seed_placement_mock_exams()
            return jsonify({'ok': True, 'inserted': inserted})
        except Exception as e:
            return jsonify({'ok': False, 'error': str(e)}), 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
