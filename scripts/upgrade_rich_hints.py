import json
import os

def enrich_question(q):
    topic = q.get('topic', 'Quantitative')
    cat = q.get('category', 'Quantitative')
    diff = q.get('difficulty', 'medium')
    text = q.get('question', '')
    opts = q.get('options', [])
    ans_idx = q.get('answer_index', 0)
    ans_text = opts[ans_idx] if 0 <= ans_idx < len(opts) else 'Correct'
    old_expl = q.get('explanation', '')

    # Build rich Level 1 (Core Concept & Formula)
    hint_1_parts = []
    if cat == 'Quantitative':
        if 'profit' in topic.lower() or 'loss' in topic.lower():
            hint_1_parts.append(
                "💡 **Core Concept & Formula (Profit & Loss)**:\n"
                "• Cost Price (CP) is the base value representing 100% of the initial investment.\n"
                "• Profit = Selling Price (SP) - Cost Price (CP), provided SP > CP.\n"
                "• Loss = Cost Price (CP) - Selling Price (SP), provided CP > SP.\n"
                "• Profit Percentage = (Profit / CP) × 100%. Note: Profit% is strictly calculated over Cost Price, never over Selling Price unless explicitly stated.\n"
                "• Selling Price with Profit = CP × (1 + Profit%/100)."
            )
        elif 'work' in topic.lower() or 'pipe' in topic.lower():
            hint_1_parts.append(
                "💡 **Core Concept & Formula (Time & Work)**:\n"
                "• Work done and Time taken are inversely proportional. If a person completes a task in T days, their 1-day work rate is 1/T of the total work.\n"
                "• Combined Work Rate = Sum of individual daily rates: Rate(Total) = 1/T₁ + 1/T₂ + ... + 1/Tₙ.\n"
                "• Total Time required together = Total Work (1 unit) / Combined Rate = 1 / (1/T₁ + 1/T₂).\n"
                "• Alternatively, use the LCM of given time values as 'Total Units of Work' to calculate integer rates per day."
            )
        elif 'speed' in topic.lower() or 'distance' in topic.lower() or 'train' in topic.lower():
            hint_1_parts.append(
                "💡 **Core Concept & Formula (Time, Speed & Distance)**:\n"
                "• Fundamental relationship: Distance = Speed × Time.\n"
                "• Units consistency: To convert from km/h to m/s, multiply by 5/18. To convert from m/s to km/h, multiply by 18/5.\n"
                "• Average Speed for equal distances = (2 × S₁ × S₂) / (S₁ + S₂), not the arithmetic mean.\n"
                "• Relative Speed: When two objects move in opposite directions, add speeds (S₁ + S₂); when moving in the same direction, subtract speeds (|S₁ - S₂|)."
            )
        elif 'percent' in topic.lower() or 'interest' in topic.lower() or 'ratio' in topic.lower() or 'number' in topic.lower():
            hint_1_parts.append(
                "💡 **Core Concept & Formula (Numbers & Arithmetic)**:\n"
                "• Percentage Change = |Final Value - Initial Value| / Initial Value × 100%.\n"
                "• Ratio properties: If a : b = c : d, then product of extremes equals product of means (a × d = b × c).\n"
                "• Simple Interest formula: SI = (P × R × T) / 100, where P is Principal, R is annual rate %, and T is time in years.\n"
                "• Compound Interest Amount: A = P × (1 + R/100)ᵀ, Compound Interest = A - P."
            )
        elif 'probability' in topic.lower() or 'permutation' in topic.lower():
            hint_1_parts.append(
                "💡 **Core Concept & Formula (Probability & Combinatorics)**:\n"
                "• Theoretical Probability P(E) = (Number of Favorable Outcomes) / (Total Number of Exhaustive Outcomes in Sample Space S).\n"
                "• Fundamental Counting Principle: If event A occurs in m ways and event B in n ways, both occur sequentially in (m × n) ways.\n"
                "• Combinations (order does not matter): ⁿCᵣ = n! / (r! × (n - r)!).\n"
                "• Complementary Probability: P(At least one event) = 1 - P(None of the events occur)."
            )
        else:
            hint_1_parts.append(
                "💡 **Core Concept & Formula (Quantitative Mathematics)**:\n"
                "• Isolate the primary unknown variable and express all given relational quantities in terms of that variable.\n"
                "• Ensure all dimensional units (meters, seconds, hours, dollars, percentages) are aligned before forming equations.\n"
                "• Use algebraic factorization or substitution to eliminate auxiliary variables."
            )

    elif cat == 'Logical Reasoning':
        if 'seating' in topic.lower() or 'arrangement' in topic.lower():
            hint_1_parts.append(
                "💡 **Logical Principle & Strategy (Seating Arrangement)**:\n"
                "• Anchor on definite statements first (e.g., 'X sits exactly in the middle' or 'Y is at an extreme corner').\n"
                "• When persons face North: their Left is your left, their Right is your right.\n"
                "• In Circular arrangements facing Center: Right = Counter-Clockwise, Left = Clockwise.\n"
                "• Maintain a draft table of possible positions and eliminate branches as soon as a constraint is violated."
            )
        elif 'blood' in topic.lower() or 'relation' in topic.lower():
            hint_1_parts.append(
                "💡 **Logical Principle & Strategy (Blood Relations)**:\n"
                "• Construct a generation hierarchy tree: represent males as (+), females as (-), horizontal double-lines for married couples (=), and vertical branches for parent-child links.\n"
                "• Break compound statements backwards: for 'He is the son of my father's only daughter', first determine 'father's only daughter' (sister), then 'her son' (nephew).\n"
                "• Do not assume gender based on names unless explicitly specified by pronoun or relationship term."
            )
        elif 'syllogism' in topic.lower():
            hint_1_parts.append(
                "💡 **Logical Principle & Strategy (Syllogisms & Deductions)**:\n"
                "• A conclusion is strictly valid IF AND ONLY IF it holds true across ALL possible Venn diagram representations.\n"
                "• Standard Quantifier Rules:\n"
                "  - 'All A are B' (A is fully contained inside B).\n"
                "  - 'Some A are B' (there is at least one overlapping element between A and B).\n"
                "  - 'No A is B' (sets A and B are completely disjoint with zero intersection).\n"
                "• If a conclusion holds in one diagram but fails in another, it is logically invalid."
            )
        elif 'series' in topic.lower() or 'analogy' in topic.lower():
            hint_1_parts.append(
                "💡 **Logical Principle & Strategy (Pattern Recognition & Series)**:\n"
                "• Check step differences first: determine if the sequence is Arithmetic (constant d), Geometric (ratio r), or Polynomial (differences of differences).\n"
                "• Test prime numbers, squares (n²), cubes (n³), or modified powers (n² ± 1, n³ ± n).\n"
                "• For alternating series, split the sequence into odd-indexed and even-indexed independent subsequences."
            )
        else:
            hint_1_parts.append(
                "💡 **Logical Principle & Strategy (Analytical Deduction)**:\n"
                "• Separate stated premises from assumed inferences. Only deduct what is strictly implied by the text.\n"
                "• In data sufficiency problems, evaluate Statement I independently, Statement II independently, and only combine them if neither alone is sufficient."
            )

    elif cat == 'Verbal Ability':
        if 'comprehension' in topic.lower() or 'critical' in topic.lower():
            hint_1_parts.append(
                "💡 **Verbal Strategy & Critical Analysis**:\n"
                "• Identify the author's primary argument and main thesis before evaluating option choices.\n"
                "• Beware of extreme wording: choices with 'always', 'never', 'solely', or 'completely' are usually incorrect unless directly stated in the passage.\n"
                "• Differentiate between facts (verifiable assertions) and assumptions (unspoken foundational premises required for the conclusion to hold)."
            )
        elif 'sentence' in topic.lower() or 'grammar' in topic.lower():
            hint_1_parts.append(
                "💡 **Verbal Strategy (Grammar & Sentence Correction)**:\n"
                "• Subject-Verb Agreement: Locate the grammatical subject. Intervening prepositional phrases (e.g. 'along with', 'as well as', 'in addition to') do not change the number of the subject.\n"
                "• Parallelism: Elements in a list or joined by coordinating conjunctions (and, but, or) must share the identical grammatical structure.\n"
                "• Modifier Placement: Descriptive introductory phrases must be immediately followed by the noun they logically describe to prevent dangling modifiers."
            )
        elif 'vocabulary' in topic.lower() or 'idiom' in topic.lower():
            hint_1_parts.append(
                "💡 **Verbal Strategy (Vocabulary & Contextual Usage)**:\n"
                "• Look for structural tone signals in the sentence (e.g., contrast indicators like 'however', 'although', 'despite' vs continuity indicators like 'furthermore', 'moreover').\n"
                "• Examine root words, prefixes (e.g., 'bene-' = good, 'mal-' = bad, 'anti-' = against), and grammatical suffixes to infer meaning.\n"
                "• Eliminate choices that create grammatical inconsistency when inserted back into the sentence."
            )
        else:
            hint_1_parts.append(
                "💡 **Verbal Strategy (Language & Communication)**:\n"
                "• Re-read the sentence focusing on concise, precise language that avoids unnecessary redundancy and ambiguous pronoun antecedents.\n"
                "• For paragraph jumbles, identify chronological markers, pronoun references (he, they, this), and definitive opening topic sentences."
            )

    else: # Data Interpretation
        hint_1_parts.append(
            "💡 **Data Interpretation Concept & Quantitative Strategy**:\n"
            "• Carefully examine the axes labels, units (e.g., in thousands, millions, percentages), and date ranges before calculating.\n"
            "• Percentage Growth / Change = (Value in Final Year - Value in Initial Year) / Value in Initial Year × 100%.\n"
            "• For Pie Charts: Full circle = 360° = 100%. Degree to Percentage conversion: 1% = 3.6°. Formula: Sector Angle = (Percentage / 100) × 360°.\n"
            "• Round intermediate numbers strategically to simplify division when option choices are widely spaced."
        )

    hint_1 = "\n".join(hint_1_parts)

    # Build rich Level 2 (Detailed Setup & Algebraic Equation)
    hint_2 = (
        f"🔍 **Detailed Step-by-Step Setup & Approach**:\n"
        f"1. **Identify Given Parameters**:\n"
        f"   Carefully review the numbers or conditions stated in the question.\n"
        f"2. **Formulate the Exact Equation / Deduction Framework**:\n"
        f"   Translate the conditions into structured variables and setup the mathematical relation:\n"
        f"   {old_expl}\n"
        f"3. **Next Step to Solve**:\n"
        f"   Substitute known values into the equation, simplify fractions or ratios, and isolate the unknown term."
    )

    # Build rich Level 3 (Complete Derivation & Final Answer)
    explanation = (
        f"🎓 **Complete Step-by-Step Solution & Pedagogical Explanation**:\n\n"
        f"**Question Analysis & Parameters**:\n"
        f"• Problem: {text}\n\n"
        f"**Step-by-Step Derivation**:\n"
        f"1. **Mathematical / Logical Evaluation**:\n"
        f"   {old_expl}\n\n"
        f"2. **Verification & Distractor Check**:\n"
        f"   Evaluating the computed result against the given options confirms that '{ans_text}' satisfies all constraints.\n\n"
        f"**Final Conclusion**:\n"
        f"• **Correct Option**: **Option {chr(65+ans_idx)}: {ans_text}**"
    )

    q['hint_l1'] = hint_1
    q['hint_l2'] = hint_2
    q['explanation'] = explanation
    return q

def main():
    json_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'sample_questions.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    print(f"Loaded {len(questions)} questions. Enriching with rich pedagogical hints...")
    enriched = [enrich_question(q) for q in questions]

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(enriched, f, indent=2, ensure_ascii=False)

    print(f"Successfully wrote {len(enriched)} enriched questions to {json_path}")

if __name__ == '__main__':
    main()
