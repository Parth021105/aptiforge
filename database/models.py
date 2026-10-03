from .db import get_db
from bson.objectid import ObjectId
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(name, email, password, role='student'):
    db = get_db()
    if db is None:
        return None
    hashed = generate_password_hash(password)
    user_doc = {
        'name': name or email.split('@')[0],
        'email': email.lower().strip(),
        'password': hashed,
        'role': role,
        'created_at': datetime.utcnow()
    }
    return db.users.insert_one(user_doc)


def find_user_by_email(email):
    db = get_db()
    if db is None or not email:
        return None
    return db.users.find_one({'email': email.lower().strip()})


def get_user_by_id(user_id):
    db = get_db()
    if db is None:
        return None
    try:
        _id = ObjectId(user_id)
    except Exception:
        return None
    u = db.users.find_one({'_id': _id})
    if not u:
        return None
    u['_id'] = str(u['_id'])
    u.pop('password', None)
    return u


def get_all_users():
    db = get_db()
    if db is None:
        return []
    users = list(db.users.find({}, {'password': 0}).sort('created_at', -1))
    for u in users:
        u['_id'] = str(u['_id'])
    return users


def insert_questions(questions):
    db = get_db()
    if db is None or not questions:
        return 0
    docs = []
    for q in questions:
        q_text = q.get('question') or q.get('question_text')
        if not q_text:
            continue
        options = q.get('options') or q.get('choices') or []
        answer_index = int(q.get('answer_index', 0))
        topic = q.get('topic') or 'General'
        category = q.get('category') or topic
        difficulty = (q.get('difficulty') or 'hard').lower()
        explanation = q.get('explanation') or ''

        docs.append({
            'question': q_text,
            'options': options,
            'answer_index': answer_index,
            'topic': topic.strip(),
            'category': category.strip(),
            'difficulty': difficulty,
            'explanation': explanation,
            'hint_l1': q.get('hint_l1') or '',
            'hint_l2': q.get('hint_l2') or '',
            'created_at': datetime.utcnow()
        })

    if not docs:
        return 0
    res = db.questions.insert_many(docs)
    return len(res.inserted_ids)


def get_question(qid):
    db = get_db()
    if db is None:
        return None
    try:
        _id = ObjectId(qid)
    except Exception:
        return None
    q = db.questions.find_one({'_id': _id})
    if q:
        q['_id'] = str(q['_id'])
    return q


def list_questions(topic=None, difficulty=None, search=None, limit=100, skip=0, random_sample=False):
    db = get_db()
    if db is None:
        return []
    query = {}
    if topic and topic.lower() != 'all':
        query['$or'] = [
            {'topic': {'$regex': f"^{topic}$", '$options': 'i'}},
            {'category': {'$regex': f"^{topic}$", '$options': 'i'}}
        ]
    if difficulty and difficulty.lower() != 'all':
        query['difficulty'] = difficulty.lower()
    if search:
        query['question'] = {'$regex': search, '$options': 'i'}

    if random_sample:
        import random
        try:
            pipeline = []
            if query:
                pipeline.append({'$match': query})
            pipeline.append({'$sample': {'size': limit}})
            docs = list(db.questions.aggregate(pipeline))
            if docs and len(docs) > 0:
                for q in docs:
                    q['_id'] = str(q['_id'])
                return docs
        except Exception:
            pass

    cursor = db.questions.find(query).skip(skip).limit(limit if not random_sample else max(limit, 100))
    questions = []
    for q in cursor:
        q['_id'] = str(q['_id'])
        questions.append(q)
    if random_sample and questions:
        import random
        random.shuffle(questions)
        questions = questions[:limit]
    return questions


def get_test_questions(category_or_topic=None, difficulty='mixed', count=20):
    """
    Selects 20 questions based on difficulty mode:
    - 'mixed': Exactly 8 Easy + 8 Medium + 4 Hard in that sequence.
    - 'easy': 20 random Easy questions.
    - 'medium': 20 random Medium questions.
    - 'hard': 20 random Hard questions (or all available Hard supplemented with Medium).
    """
    diff = (difficulty or 'mixed').lower()
    if diff == 'mixed':
        easy_qs = list_questions(topic=category_or_topic, difficulty='easy', limit=8, random_sample=True)
        med_qs = list_questions(topic=category_or_topic, difficulty='medium', limit=8, random_sample=True)
        hard_qs = list_questions(topic=category_or_topic, difficulty='hard', limit=4, random_sample=True)

        # Fallback padding if pool in specific topic has fewer
        if len(easy_qs) < 8:
            fill_easy = list_questions(topic=category_or_topic, difficulty='easy', limit=8 - len(easy_qs), random_sample=True)
            easy_qs.extend(fill_easy)
        if len(med_qs) < 8:
            fill_med = list_questions(topic=category_or_topic, difficulty='medium', limit=8 - len(med_qs), random_sample=True)
            med_qs.extend(fill_med)
        if len(hard_qs) < 4:
            fill_hard = list_questions(topic=category_or_topic, difficulty='hard', limit=4 - len(hard_qs), random_sample=True)
            hard_qs.extend(fill_hard)

        combined = easy_qs[:8] + med_qs[:8] + hard_qs[:4]
        if len(combined) < 20:
            existing_ids = set(q['_id'] for q in combined)
            pool = list_questions(topic=category_or_topic, limit=25, random_sample=True)
            for q in pool:
                if q['_id'] not in existing_ids and len(combined) < 20:
                    combined.append(q)
                    existing_ids.add(q['_id'])
        return combined[:20]

    elif diff in ('easy', 'medium'):
        qs = list_questions(topic=category_or_topic, difficulty=diff, limit=count, random_sample=True)
        if len(qs) < count:
            existing_ids = set(q['_id'] for q in qs)
            pool = list_questions(topic=category_or_topic, limit=count, random_sample=True)
            for q in pool:
                if q['_id'] not in existing_ids and len(qs) < count:
                    qs.append(q)
                    existing_ids.add(q['_id'])
        return qs[:count]

    elif diff == 'hard':
        hard_qs = list_questions(topic=category_or_topic, difficulty='hard', limit=count, random_sample=True)
        if len(hard_qs) < count:
            existing_ids = set(q['_id'] for q in hard_qs)
            med_qs = list_questions(topic=category_or_topic, difficulty='medium', limit=count - len(hard_qs), random_sample=True)
            for q in med_qs:
                if q['_id'] not in existing_ids and len(hard_qs) < count:
                    hard_qs.append(q)
                    existing_ids.add(q['_id'])
        return hard_qs[:count]

    else:
        return list_questions(topic=category_or_topic, difficulty=diff, limit=count, random_sample=True)


def get_random_questions(category_or_topic=None, count=20, difficulty=None):
    """
    Returns a random sample of `count` questions matching the category or topic.
    """
    return get_test_questions(category_or_topic=category_or_topic, difficulty=difficulty or 'mixed', count=count)


def count_questions(topic=None):
    db = get_db()
    if db is None:
        return 0
    query = {}
    if topic and topic.lower() != 'all':
        query['$or'] = [
            {'topic': {'$regex': f"^{topic}$", '$options': 'i'}},
            {'category': {'$regex': f"^{topic}$", '$options': 'i'}}
        ]
    return db.questions.count_documents(query)


def get_topics():
    db = get_db()
    default_topics = ['Quantitative', 'Logical Reasoning', 'Verbal Ability', 'Data Interpretation']
    if db is None:
        return default_topics
    distinct_topics = db.questions.distinct('topic')
    distinct_categories = db.questions.distinct('category')
    combined = list(set([t for t in distinct_topics if t] + [c for c in distinct_categories if c] + default_topics))
    return sorted(combined)


def update_question(qid, data):
    db = get_db()
    if db is None:
        return False
    try:
        _id = ObjectId(qid)
    except Exception:
        return False
    update_doc = {}
    if 'question' in data:
        update_doc['question'] = data['question']
    if 'options' in data:
        update_doc['options'] = data['options']
    if 'answer_index' in data:
        update_doc['answer_index'] = int(data['answer_index'])
    if 'topic' in data:
        update_doc['topic'] = data['topic']
    if 'difficulty' in data:
        update_doc['difficulty'] = data['difficulty']
    if 'explanation' in data:
        update_doc['explanation'] = data['explanation']

    res = db.questions.update_one({'_id': _id}, {'$set': update_doc})
    return res.modified_count > 0


def delete_question(qid):
    db = get_db()
    if db is None:
        return False
    try:
        _id = ObjectId(qid)
    except Exception:
        return False
    res = db.questions.delete_one({'_id': _id})
    return res.deleted_count > 0


def verify_answer(qid, selected_index, user_id=None):
    q = get_question(qid)
    if not q:
        return False, None, "Question not found"
    correct_index = int(q.get('answer_index', 0))
    is_correct = (selected_index == correct_index)
    explanation = q.get('explanation', '')

    # Log practice attempt if user_id is provided
    if user_id:
        db = get_db()
        if db is not None:
            db.practice_attempts.insert_one({
                'user_id': user_id,
                'question_id': qid,
                'topic': q.get('topic', 'General'),
                'difficulty': q.get('difficulty', 'medium'),
                'selected_index': selected_index,
                'correct_index': correct_index,
                'is_correct': is_correct,
                'created_at': datetime.utcnow()
            })

    return is_correct, correct_index, explanation


def insert_exam(name, question_ids, duration_minutes=20, enable_hints=True, created_by=None, category=None, topic=None):
    db = get_db()
    if db is None:
        return None
    qids = []
    for q in question_ids:
        try:
            qids.append(ObjectId(q))
        except Exception:
            continue
    doc = {
        'name': name,
        'question_ids': qids,
        'duration_minutes': 20,
        'enable_hints': bool(enable_hints),
        'created_by': created_by,
        'category': category or 'All',
        'topic': topic or category or 'General',
        'created_at': datetime.utcnow()
    }
    res = db.exams.insert_one(doc)
    return str(res.inserted_id)


def list_exams():
    db = get_db()
    if db is None:
        return []
    exams = list(db.exams.find().sort('created_at', -1))
    for ex in exams:
        ex['_id'] = str(ex['_id'])
        ex['duration_minutes'] = 20  # Standardize all test timers to 20 minutes
        ex['question_count'] = len(ex.get('question_ids', [])) or 20
        ex['question_ids'] = [str(q) for q in ex.get('question_ids', [])]
        ex['category'] = ex.get('category') or 'All'
        ex['topic'] = ex.get('topic') or ex['category']
    return exams


def seed_placement_mock_exams():
    """
    Auto-generates industry/placement mock exams with 20-minute timers and dynamic 20-question selection.
    """
    db = get_db()
    if db is None:
        return 0

    # Refresh existing mock exams to apply 20-minute timer and 20-question randomized pool
    try:
        db.exams.delete_many({})
    except Exception:
        pass

    mock_definitions = [
        {"name": "Quantitative Aptitude Industry Mock Test", "category": "Quantitative", "topic": "Quantitative", "duration": 20, "hints": True},
        {"name": "Logical Reasoning Industry Mock Test", "category": "Logical Reasoning", "topic": "Logical Reasoning", "duration": 20, "hints": True},
        {"name": "Verbal Ability Industry Mock Test", "category": "Verbal Ability", "topic": "Verbal Ability", "duration": 20, "hints": True},
        {"name": "Data Interpretation Industry Mock Test", "category": "Data Interpretation", "topic": "Data Interpretation", "duration": 20, "hints": True},
        {"name": "Full-Length Placement Comprehensive Exam", "category": "All", "topic": "All", "duration": 20, "hints": True},
        {"name": "Profit & Loss & Commercial Math Test", "category": "Quantitative", "topic": "Profit & Loss", "duration": 20, "hints": True},
        {"name": "Time & Work Efficiency Test", "category": "Quantitative", "topic": "Time & Work", "duration": 20, "hints": True},
        {"name": "Time, Speed & Distance Test", "category": "Quantitative", "topic": "Time, Speed & Distance", "duration": 20, "hints": True},
        {"name": "Numbers & Modular Arithmetic Test", "category": "Quantitative", "topic": "Numbers", "duration": 20, "hints": True},
        {"name": "Probability & Combinatorics Test", "category": "Quantitative", "topic": "Probability", "duration": 20, "hints": True},
        {"name": "Syllogisms & Deductive Logic Test", "category": "Logical Reasoning", "topic": "Syllogisms", "duration": 20, "hints": True},
        {"name": "Blood Relations Puzzle Test", "category": "Logical Reasoning", "topic": "Blood Relations", "duration": 20, "hints": True},
        {"name": "Seating Arrangement Special Test", "category": "Logical Reasoning", "topic": "Seating Arrangement", "duration": 20, "hints": True},
        {"name": "Code Decoding Logic Test", "category": "Logical Reasoning", "topic": "Code Decoding", "duration": 20, "hints": True},
        {"name": "Clocks & Calendar Mastery Test", "category": "Logical Reasoning", "topic": "Clocks", "duration": 20, "hints": True},
        {"name": "Reading Comprehension & Logic Test", "category": "Verbal Ability", "topic": "Reading Comprehension", "duration": 20, "hints": True},
        {"name": "Sentence Correction & Grammar Test", "category": "Verbal Ability", "topic": "Sentence Correction", "duration": 20, "hints": True},
        {"name": "Table Charts & Bar Graphs DI Test", "category": "Data Interpretation", "topic": "Table Chart", "duration": 20, "hints": True},
        {"name": "Pie Charts & Caselet DI Test", "category": "Data Interpretation", "topic": "Pie Chart", "duration": 20, "hints": True}
    ]

    count_created = 0
    for mock in mock_definitions:
        target = mock["topic"] if mock["topic"] != "All" else None
        sampled = get_random_questions(category_or_topic=target, count=20)
        if len(sampled) < 20 and mock.get("category") and mock["category"] != "All":
            sampled_ids = set(q['_id'] for q in sampled)
            extra = get_random_questions(category_or_topic=mock["category"], count=20)
            for q in extra:
                if q['_id'] not in sampled_ids and len(sampled) < 20:
                    sampled.append(q)
                    sampled_ids.add(q['_id'])

        qids = [ObjectId(q['_id']) for q in sampled]
        insert_exam(
            name=mock["name"],
            question_ids=qids,
            duration_minutes=20,
            enable_hints=mock["hints"],
            category=mock["category"],
            topic=mock["topic"]
        )
        count_created += 1

    return count_created


def get_exam(exam_id, session_id=None):
    db = get_db()
    if db is None:
        return None
    try:
        _id = ObjectId(exam_id)
    except Exception:
        return None
    ex = db.exams.find_one({'_id': _id})
    if not ex:
        return None

    questions = []
    question_ids_to_load = []

    if session_id:
        try:
            sess = db.exam_sessions.find_one({'_id': ObjectId(session_id)})
            if sess and sess.get('question_ids'):
                question_ids_to_load = sess.get('question_ids')
        except Exception:
            pass

    if not question_ids_to_load:
        question_ids_to_load = ex.get('question_ids', [])

    for qid in question_ids_to_load:
        q = db.questions.find_one({'_id': qid})
        if q:
            q['_id'] = str(q['_id'])
            questions.append(q)

    # If fewer than 20 questions, augment with random questions from the category pool
    if len(questions) < 20:
        target = ex.get('category') or ex.get('topic')
        if target and target.lower() == 'all':
            target = None
        extra = get_random_questions(category_or_topic=target, count=20)
        existing_ids = set(q['_id'] for q in questions)
        for q in extra:
            if q['_id'] not in existing_ids and len(questions) < 20:
                questions.append(q)
                existing_ids.add(q['_id'])

    ex['duration_minutes'] = 20  # Standardize to 20 minutes for every test
    ex['question_ids'] = [str(x['_id']) if isinstance(x, dict) else str(x) for x in questions]
    ex['questions'] = questions[:20]
    ex['question_count'] = len(ex['questions'])
    ex['_id'] = str(ex['_id'])
    return ex


def delete_exam(exam_id):
    db = get_db()
    if db is None:
        return False
    try:
        _id = ObjectId(exam_id)
    except Exception:
        return False
    res = db.exams.delete_one({'_id': _id})
    return res.deleted_count > 0


def create_exam_session(user_id, exam_id, difficulty='mixed'):
    db = get_db()
    if db is None:
        return None
    try:
        eid = ObjectId(exam_id)
    except Exception:
        return None
    ex = db.exams.find_one({'_id': eid})
    if not ex:
        return None

    # Dynamically select 20 random questions from this category / topic pool!
    target = ex.get('category') or ex.get('topic')
    if target and target.lower() == 'all':
        target = None
    sampled = get_test_questions(category_or_topic=target, difficulty=difficulty, count=20)
    session_qids = [ObjectId(q['_id']) for q in sampled]
    if not session_qids:
        session_qids = ex.get('question_ids', [])[:20]

    session_doc = {
        'user_id': user_id,
        'exam_id': str(eid),
        'difficulty': difficulty or 'mixed',
        'question_ids': session_qids,
        'started_at': datetime.utcnow(),
        'completed': False
    }
    res = db.exam_sessions.insert_one(session_doc)
    return str(res.inserted_id)


def submit_exam_and_score(session_id, answers, time_taken_seconds=0):
    db = get_db()
    if db is None:
        return None
    try:
        sid = ObjectId(session_id)
    except Exception:
        return None
    sess = db.exam_sessions.find_one({'_id': sid})
    if not sess:
        return None
    exam = get_exam(sess['exam_id'], session_id=str(sid))
    if not exam:
        return None

    total = len(exam['questions'])
    correct_count = 0
    per_question = []

    for q in exam['questions']:
        qid = q['_id']
        selected = answers.get(qid)
        correct_index = int(q.get('answer_index', 0))
        is_correct = (selected is not None and int(selected) == correct_index)
        if is_correct:
            correct_count += 1
        per_question.append({
            'question_id': qid,
            'question_text': q.get('question'),
            'selected': selected,
            'correct_index': correct_index,
            'is_correct': is_correct,
            'topic': q.get('topic', 'General'),
            'category': q.get('category', 'General'),
            'explanation': q.get('explanation', '')
        })

    percentage = round((correct_count / total * 100), 1) if total > 0 else 0

    result_doc = {
        'user_id': sess['user_id'],
        'exam_id': sess['exam_id'],
        'exam_name': exam.get('name', 'Mock Exam'),
        'score': percentage,
        'correct_count': correct_count,
        'total_questions': total,
        'time_taken_seconds': time_taken_seconds,
        'details': per_question,
        'created_at': datetime.utcnow()
    }
    res = db.results.insert_one(result_doc)
    db.exam_sessions.update_one({'_id': sid}, {'$set': {'completed': True, 'submitted_at': datetime.utcnow()}})

    result_doc['_id'] = str(res.inserted_id)
    return result_doc


def get_user_results(user_id):
    db = get_db()
    if db is None:
        return []
    docs = list(db.results.find({'user_id': user_id}).sort('created_at', -1).limit(50))
    for d in docs:
        d['_id'] = str(d['_id'])
    return docs


def get_all_results():
    db = get_db()
    if db is None:
        return []
    docs = list(db.results.find().sort('created_at', -1).limit(100))
    for d in docs:
        d['_id'] = str(d['_id'])
        user = get_user_by_id(d.get('user_id'))
        d['user_name'] = user.get('name') if user else 'Student'
        d['user_email'] = user.get('email') if user else ''
    return docs


def analytics_summary_for_user(user_id):
    db = get_db()
    if db is None:
        return {
            'total_exams': 0,
            'avg_score': 0,
            'total_practice': 0,
            'practice_accuracy': 0,
            'topic_stats': [],
            'weak_topics': []
        }

    # Exam results summary
    results = list(db.results.find({'user_id': user_id}))
    total_exams = len(results)
    avg_score = round(sum(r.get('score', 0) for r in results) / total_exams, 1) if total_exams > 0 else 0

    # Practice attempts summary
    practice_attempts = list(db.practice_attempts.find({'user_id': user_id}))
    total_practice = len(practice_attempts)
    practice_correct = sum(1 for p in practice_attempts if p.get('is_correct'))
    practice_accuracy = round((practice_correct / total_practice * 100), 1) if total_practice > 0 else 0

    # Topic-wise accuracy combining practice & exams
    topic_data = {}

    for p in practice_attempts:
        t = p.get('topic') or 'Quantitative'
        if t not in topic_data:
            topic_data[t] = {'total': 0, 'correct': 0}
        topic_data[t]['total'] += 1
        if p.get('is_correct'):
            topic_data[t]['correct'] += 1

    for r in results:
        for q in r.get('details', []):
            t = q.get('topic') or 'Quantitative'
            if t not in topic_data:
                topic_data[t] = {'total': 0, 'correct': 0}
            topic_data[t]['total'] += 1
            if q.get('is_correct'):
                topic_data[t]['correct'] += 1

    topic_stats = []
    weak_topics = []

    for topic, counts in topic_data.items():
        tot = counts['total']
        cor = counts['correct']
        acc = round((cor / tot * 100), 1) if tot > 0 else 0
        stat = {'topic': topic, 'total': tot, 'correct': cor, 'accuracy': acc}
        topic_stats.append(stat)
        if acc < 65 and tot >= 2:
            weak_topics.append(stat)

    topic_stats.sort(key=lambda x: x['accuracy'])

    return {
        'total_exams': total_exams,
        'avg_score': avg_score,
        'total_practice': total_practice,
        'practice_accuracy': practice_accuracy,
        'topic_stats': topic_stats,
        'weak_topics': weak_topics,
        'recent_exams': get_user_results(user_id)[:5]
    }


def admin_analytics_summary():
    db = get_db()
    if db is None:
        return {'total_students': 0, 'total_questions': 0, 'total_exams': 0, 'total_attempts': 0}
    total_students = db.users.count_documents({'role': 'student'})
    total_questions = db.questions.count_documents({})
    total_exams = db.exams.count_documents({})
    total_attempts = db.results.count_documents({})
    return {
        'total_students': total_students,
        'total_questions': total_questions,
        'total_exams': total_exams,
        'total_attempts': total_attempts
    }
