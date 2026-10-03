import os
import requests
import json
import logging
from config import Config

logger = logging.getLogger(__name__)

AI_PROVIDER = Config.AI_PROVIDER
AI_API_KEY = Config.AI_API_KEY
AI_MODEL = Config.AI_MODEL


def _build_hint_prompt(question_text, topic="", level=1):
    level_instructions = {
        1: "Provide Level 1 – Basic Hint: A simple hint that guides the user toward the correct approach and formula without revealing the solution or option choice.",
        2: "Provide Level 2 – Detailed Hint: A more detailed explanation of the question and the exact mathematical/logical approach required to solve it step-by-step.",
        3: "Provide Level 3 – Advanced Hint / Solution: Display the complete solution with a proper step-by-step detailed explanation and final answer."
    }

    inst = level_instructions.get(level, level_instructions[1])

    prompt = (
        f"You are an expert aptitude tutor on AptiForge. The student is practicing a {topic or 'general'} aptitude question.\n\n"
        f"Question:\n\"{question_text}\"\n\n"
        f"Goal: {inst}\n\n"
        "Guidelines:\n"
        "1. Write clear, pedagogical, concise explanations.\n"
        "2. For Level 1 and Level 2, guide their thinking without prematurely giving away the answer.\n"
        "3. For Level 3, provide a full, structured step-by-step derivation and state the correct option.\n"
    )
    return prompt


def call_cloud_ai_api(prompt):
    """
    Call Groq, OpenRouter, OpenAI, or local Ollama API based on configuration.
    """
    if AI_PROVIDER != 'ollama' and not AI_API_KEY:
        return None

    try:
        if AI_PROVIDER == 'ollama':
            host = getattr(Config, 'OLLAMA_HOST', 'http://localhost:11434').rstrip('/')
            url = f"{host}/v1/chat/completions"
            payload = {
                "model": AI_MODEL or "llama3.2",
                "messages": [
                    {"role": "system", "content": "You are a concise, helpful aptitude tutor providing progressive hints."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 220,
                "temperature": 0.5
            }
            try:
                resp = requests.post(url, json=payload, timeout=12)
                if resp.status_code == 200:
                    data = resp.json()
                    return data['choices'][0]['message']['content'].strip()
            except Exception:
                pass
            
            # Direct Ollama native endpoint fallback (/api/generate)
            url_native = f"{host}/api/generate"
            payload_native = {
                "model": AI_MODEL or "llama3.2",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.5,
                    "num_predict": 220
                }
            }
            resp_native = requests.post(url_native, json=payload_native, timeout=12)
            if resp_native.status_code == 200:
                data = resp_native.json()
                return data.get('response', '').strip()
            else:
                logger.warning(f"Ollama API error HTTP {resp_native.status_code}: {resp_native.text}")

        elif AI_PROVIDER == 'groq':
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": AI_MODEL or "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": "You are a concise, helpful aptitude tutor providing progressive hints."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 220,
                "temperature": 0.5
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                logger.warning(f"Groq API error HTTP {resp.status_code}: {resp.text}")

        elif AI_PROVIDER == 'openrouter':
            url = "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": AI_MODEL or "meta-llama/llama-3-70b-instruct",
                "messages": [
                    {"role": "system", "content": "You are a concise aptitude tutor providing progressive hints."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 220,
                "temperature": 0.5
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                return data['choices'][0]['message']['content'].strip()

        elif AI_PROVIDER == 'openai':
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {AI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": AI_MODEL or "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "You are a concise aptitude tutor providing progressive hints."},
                    {"role": "user", "content": prompt}
                ],
                "max_tokens": 220,
                "temperature": 0.5
            }
            resp = requests.post(url, headers=headers, json=payload, timeout=8)
            if resp.status_code == 200:
                data = resp.json()
                return data['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"AI API exception ({AI_PROVIDER}): {e}")

    return None


def get_offline_fallback_hint(question_doc, level=1):
    """
    Structured 3-level offline fallback hint generator.
    """
    topic = question_doc.get('topic', 'Quantitative') if isinstance(question_doc, dict) else ''
    category = question_doc.get('category', topic) if isinstance(question_doc, dict) else ''
    combined_topic = f"{category} {topic}".lower()

    if 'quantitative' in combined_topic or 'profit' in combined_topic or 'speed' in combined_topic or 'work' in combined_topic or 'number' in combined_topic:
        if level == 1:
            return "💡 **Level 1 – Basic Hint**\nIdentify the known variables and the core formula needed (e.g., Speed = Distance / Time, Work Done = Rate × Time, or Profit% = (SP - CP)/CP × 100). Avoid calculating immediately; list what is given."
        elif level == 2:
            return "🔍 **Level 2 – Detailed Hint**\nSet up the algebraic equation with the given values. Express all unknown quantities in terms of a single variable, and equalize the ratios or unit rates before simplifying."
        else:
            expl = question_doc.get('explanation', '') if isinstance(question_doc, dict) else ''
            ans = question_doc.get('correct_answer', '') if isinstance(question_doc, dict) else ''
            base = "🎓 **Level 3 – Advanced Hint / Solution**\n"
            if expl:
                base += f"Step-by-step solution: {expl}"
            else:
                base += "Solve the equation by cross-multiplying and isolating the unknown variable to obtain the exact value."
            if ans:
                base += f"\n\nCorrect Answer: {ans}"
            return base

    elif 'logical' in combined_topic or 'reasoning' in combined_topic or 'syllogism' in combined_topic or 'relation' in combined_topic:
        if level == 1:
            return "💡 **Level 1 – Basic Hint**\nLook for the directional or logical constraint that fixes at least one element with 100% certainty. Do not guess; find the anchor fact."
        elif level == 2:
            return "🔍 **Level 2 – Detailed Hint**\nDraft a quick schematic or positional chart (e.g. linear seating line or Venn diagram for syllogisms). Place the fixed elements first, then test conditional constraints."
        else:
            expl = question_doc.get('explanation', '') if isinstance(question_doc, dict) else ''
            ans = question_doc.get('correct_answer', '') if isinstance(question_doc, dict) else ''
            base = "🎓 **Level 3 – Advanced Hint / Solution**\n"
            if expl:
                base += f"Step-by-step deduction: {expl}"
            else:
                base += "Eliminate all conflicting permutations until only one valid arrangement remains."
            if ans:
                base += f"\n\nCorrect Answer: {ans}"
            return base

    elif 'verbal' in combined_topic or 'english' in combined_topic or 'comprehension' in combined_topic:
        if level == 1:
            return "💡 **Level 1 – Basic Hint**\nIdentify the grammatical role of the target phrase (subject-verb agreement, modifier placement, or parallel structure) or the author's primary assertion."
        elif level == 2:
            return "🔍 **Level 2 – Detailed Hint**\nInspect each option against grammatical rules: check tense consistency and whether pronouns clearly refer to their intended antecedent."
        else:
            expl = question_doc.get('explanation', '') if isinstance(question_doc, dict) else ''
            ans = question_doc.get('correct_answer', '') if isinstance(question_doc, dict) else ''
            base = "🎓 **Level 3 – Advanced Hint / Solution**\n"
            if expl:
                base += f"Detailed explanation: {expl}"
            else:
                base += "The correct choice conforms to standard written English and eliminates dangling modifiers."
            if ans:
                base += f"\n\nCorrect Answer: {ans}"
            return base

    else:
        if level == 1:
            return "💡 **Level 1 – Basic Hint**\nCarefully read the question prompt and isolate the specific data points required from the tables or problem statement."
        elif level == 2:
            return "🔍 **Level 2 – Detailed Hint**\nBreak down the calculation into simple ratios or percentage changes before performing full arithmetic."
        else:
            expl = question_doc.get('explanation', '') if isinstance(question_doc, dict) else ''
            ans = question_doc.get('correct_answer', '') if isinstance(question_doc, dict) else ''
            base = "🎓 **Level 3 – Advanced Hint / Solution**\n"
            if expl:
                base += f"Step-by-step solution: {expl}"
            else:
                base += "Compute the exact proportion and match with the closest option choice."
            if ans:
                base += f"\n\nCorrect Answer: {ans}"
            return base


def get_hint_for_question(question_doc, level=1):
    """
    Main entry point for progressive hints:
    - Level 1 – Basic Hint: A simple hint that guides the user toward the correct approach without revealing too much.
    - Level 2 – Detailed Hint: A more detailed explanation of the question and the approach required to solve it.
    - Level 3 – Advanced Hint / Solution: Display the complete solution with a proper step-by-step and detailed explanation.
    """
    if isinstance(question_doc, dict):
        if level == 1 and question_doc.get('hint_l1'):
            return question_doc.get('hint_l1')
        elif level == 2 and question_doc.get('hint_l2'):
            return question_doc.get('hint_l2')
        elif level == 3 and question_doc.get('explanation'):
            return question_doc.get('explanation')

    # If question_doc lacks the curated hints, attempt cloud AI call
    text = question_doc.get('question', '') if isinstance(question_doc, dict) else str(question_doc)
    topic = question_doc.get('topic', 'General') if isinstance(question_doc, dict) else 'General'

    prompt = _build_hint_prompt(text, topic, level)
    ai_hint = call_cloud_ai_api(prompt)
    if ai_hint:
        prefixes = {
            1: "💡 **Level 1 – Basic Hint**\n\n",
            2: "🔍 **Level 2 – Detailed Hint**\n\n",
            3: "🎓 **Level 3 – Advanced Solution**\n\n"
        }
        return f"{prefixes.get(level, '')}{ai_hint}"

    # Fallback to intelligent rule-based hint
    return get_offline_fallback_hint(question_doc, level)
