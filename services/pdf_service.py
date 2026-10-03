import io
import re
import logging
from pypdf import PdfReader

logger = logging.getLogger(__name__)

def extract_text_from_pdf(pdf_stream_or_bytes):
    """
    Extracts plain text from a PDF file stream or bytes buffer.
    """
    try:
        if isinstance(pdf_stream_or_bytes, bytes):
            reader = PdfReader(io.BytesIO(pdf_stream_or_bytes))
        else:
            reader = PdfReader(pdf_stream_or_bytes)
        
        full_text = []
        for idx, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                full_text.append(text)
        return "\n\n".join(full_text)
    except Exception as e:
        logger.error(f"Error reading PDF content: {e}")
        raise ValueError(f"Failed to read PDF file: {str(e)}")


def parse_questions_from_text(raw_text, default_topic="Quantitative", default_difficulty="medium"):
    """
    Parses questions, options (A, B, C, D), answers, and explanations from text.
    Handles standard formats:
    - 1. Question text / Q1. Question text / Question 1: ...
    - A) ... B) ... C) ... D) ... / (A) ... / A. ...
    - Answer: A / Ans: B / Correct Answer: C
    - Explanation: ... / Solution: ...
    """
    if not raw_text or not raw_text.strip():
        return []

    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    cleaned_text = "\n".join(lines)

    # Strategy: Split into question blocks using regex for Question numbering
    # Matches: "1.", "1)", "Q1.", "Q1:", "Question 1:", "Q.1", etc. at line starts or text starts
    pattern = re.compile(
        r'(?:^|\n)\s*(?:Q(?:uestion)?\.?\s*(\d+)[:.]?|(\d+)[\.\)])\s+',
        re.IGNORECASE
    )

    matches = list(pattern.finditer(cleaned_text))
    blocks = []

    if matches:
        for i in range(len(matches)):
            start = matches[i].end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(cleaned_text)
            block = cleaned_text[start:end].strip()
            if block:
                blocks.append(block)
    else:
        # Fallback: Split on double newlines
        blocks = [b.strip() for b in cleaned_text.split('\n\n') if len(b.strip()) > 30]

    parsed_questions = []

    for block in blocks:
        q_item = _parse_single_question_block(block, default_topic, default_difficulty)
        if q_item and len(q_item.get('options', [])) >= 2:
            parsed_questions.append(q_item)

    return parsed_questions


def _parse_single_question_block(block, default_topic="Quantitative", default_difficulty="medium"):
    """
    Parses a single question text block into structured dictionary.
    """
    lines = [l.strip() for l in block.splitlines() if l.strip()]
    if not lines:
        return None

    # Separate metadata (Answer, Explanation, Topic, Difficulty) from the Question & Options
    explanation = ""
    correct_idx = 0
    topic = default_topic
    difficulty = default_difficulty

    # 1. Topic & Difficulty (extract early from the full block)
    topic_match = re.search(r'(?:Topic|Category)\s*[:\-]\s*([A-Za-z\s&,]+?)(?=[|•\n\]\)]|$)', block, re.IGNORECASE)
    if topic_match:
        t_cand = topic_match.group(1).strip()
        if len(t_cand) < 30:
            topic = t_cand
        block = block[:topic_match.start()] + "\n" + block[topic_match.end():]
        block = re.sub(r'^\s*[|•]\s*', '', block, flags=re.MULTILINE)

    diff_match = re.search(r'(?:Difficulty|Level)\s*[:\-]\s*(easy|medium|hard)', block, re.IGNORECASE)
    if diff_match:
        difficulty = diff_match.group(1).lower()
        block = block[:diff_match.start()] + "\n" + block[diff_match.end():]
        block = re.sub(r'^\s*[|•]\s*', '', block, flags=re.MULTILINE)

    # 2. Extract and remove Explanation / Solution
    exp_match = re.search(r'(?:Explanation|Solution|Exp|Reason)\s*[:\-]\s*(.+)', block, re.IGNORECASE | re.DOTALL)
    if exp_match:
        explanation = exp_match.group(1).strip()
        block_cleaned = block[:exp_match.start()].strip()
    else:
        block_cleaned = block

    # 3. Extract and remove Answer: / Ans: / Correct: / Key:
    ans_pattern = re.compile(
        r'(?:Answer|Ans|Correct\s*Answer|Key|Correct\s*Option)\s*[:\-]?\s*(?:Option\s*)?\(?([A-Ea-e1-5])\)?',
        re.IGNORECASE
    )
    ans_match = ans_pattern.search(block_cleaned)
    if ans_match:
        val = ans_match.group(1).upper()
        if val in ('A', '1'): correct_idx = 0
        elif val in ('B', '2'): correct_idx = 1
        elif val in ('C', '3'): correct_idx = 2
        elif val in ('D', '4'): correct_idx = 3
        elif val in ('E', '5'): correct_idx = 4
        block_cleaned = block_cleaned[:ans_match.start()] + "\n" + block_cleaned[ans_match.end():]

    # 4. Extract options A), B), C), D)
    opt_pattern = re.compile(
        r'(?:^|\n|\s+)(?:\(?([A-Ea-e])\)|([A-Ea-e])[\.\:]|\[([A-Ea-e])\])\s+',
        re.MULTILINE
    )
    opt_matches = list(opt_pattern.finditer(block_cleaned))

    options = []
    question_statement = ""

    if len(opt_matches) >= 2:
        question_statement = block_cleaned[:opt_matches[0].start()].strip()
        for idx in range(len(opt_matches)):
            opt_start = opt_matches[idx].end()
            opt_end = opt_matches[idx + 1].start() if idx + 1 < len(opt_matches) else len(block_cleaned)
            opt_text = block_cleaned[opt_start:opt_end].strip()
            # Clean leftover keywords
            opt_text = re.sub(r'^(?:Answer|Ans|Explanation|Solution).*$', '', opt_text, flags=re.IGNORECASE | re.MULTILINE).strip()
            if opt_text:
                options.append(opt_text)
    else:
        # Line-by-line fallback
        q_lines = []
        for l in block_cleaned.splitlines():
            l_str = l.strip()
            if not l_str:
                continue
            m = re.match(r'^[\(\[]?([A-Ea-e])[\)\]\.\:]\s*(.+)$', l_str)
            if m:
                options.append(m.group(2).strip())
            else:
                if not options:
                    q_lines.append(l_str)
        question_statement = " ".join(q_lines).strip()

    # Clean question statement
    question_statement = re.sub(r'^(?:Q(?:uestion)?\.?\s*\d+[:.]?|\d+[\.\)])\s*', '', question_statement, flags=re.IGNORECASE).strip()
    question_statement = re.sub(r'[\s|•\-–—]+$', '', question_statement).strip()
    question_statement = re.sub(r'\s+', ' ', question_statement).strip()
    options = [re.sub(r'\s+', ' ', opt).strip() for opt in options if opt.strip()]
    if explanation:
        explanation = re.sub(r'\s+', ' ', explanation).strip()

    if not question_statement or len(options) < 2:
        return None

    # Determine category
    category = "Quantitative"
    top_clean = (topic or "").strip()
    known_cats = ["Quantitative", "Logical Reasoning", "Verbal Ability", "Data Interpretation"]
    matched_cat = next((kc for kc in known_cats if top_clean.lower() == kc.lower()), None)
    if matched_cat:
        category = matched_cat
    else:
        q_lower = (question_statement + " " + topic).lower()
        if any(k in q_lower for k in ['blood relation', 'seating', 'syllogism', 'coding', 'decoding', 'direction', 'clock', 'calendar', 'puzzle', 'series', 'analogy', 'logic']):
            category = "Logical Reasoning"
        elif any(k in q_lower for k in ['grammar', 'passage', 'comprehension', 'vocabulary', 'synonym', 'antonym', 'sentence', 'idiom', 'preposition', 'verbal', 'error', 'antonym']):
            category = "Verbal Ability"
        elif any(k in q_lower for k in ['table', 'bar graph', 'pie chart', 'caselet', 'data interpretation', 'line graph', 'chart']):
            category = "Data Interpretation"
        elif any(k in q_lower for k in ['ratio', 'percentage', 'speed', 'distance', 'time', 'work', 'profit', 'loss', 'simple interest', 'compound interest', 'probability', 'algebra', 'arithmetic', 'number', 'train', 'boat']):
            category = "Quantitative"

    # Ensure answer_index is valid
    if correct_idx >= len(options):
        correct_idx = 0

    return {
        'question': question_statement,
        'options': options,
        'answer_index': correct_idx,
        'topic': topic or category,
        'category': category,
        'difficulty': difficulty,
        'explanation': explanation,
        'hint_l1': f"Identify the foundational concept governing this problem in {topic or category}.",
        'hint_l2': "Set up the algebraic relationships and methodically eliminate inconsistent choices.",
        'hint_l3': explanation or "Follow the systematic method to solve step-by-step."
    }


def parse_questions_from_pdf(file_stream_or_bytes, default_topic="Quantitative", default_difficulty="medium"):
    """
    Reads PDF and returns a list of formatted question documents ready for database ingestion.
    """
    raw_text = extract_text_from_pdf(file_stream_or_bytes)
    return parse_questions_from_text(raw_text, default_topic, default_difficulty)
