import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_sample_faculty_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=45,
        leftMargin=45,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0f172a'),
        alignment=1, # Center
        spaceAfter=4,
        fontName='Helvetica-Bold'
    )
    
    sub_style = ParagraphStyle(
        'SubTitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        alignment=1,
        spaceAfter=15
    )

    badge_style = ParagraphStyle(
        'BadgeStyle',
        parent=styles['Normal'],
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#0284c7'),
        fontName='Helvetica-Bold',
        spaceBefore=8,
        spaceAfter=2
    )

    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=2,
        spaceAfter=5,
        fontName='Helvetica-Bold'
    )

    opt_style = ParagraphStyle(
        'OptionStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        leftIndent=15,
        spaceAfter=2
    )

    ans_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['Normal'],
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#059669'),
        fontName='Helvetica-Bold',
        leftIndent=15,
        spaceBefore=3,
        spaceAfter=2
    )

    expl_style = ParagraphStyle(
        'ExplStyle',
        parent=styles['Normal'],
        fontSize=9,
        leading=12.5,
        textColor=colors.HexColor('#64748b'),
        leftIndent=15,
        spaceAfter=10
    )

    story = [
        Paragraph("AptiForge Comprehensive Campus Assessment 2026", title_style),
        Paragraph("Official Faculty Question Paper • Quantitative, Logical Reasoning & Verbal Ability", sub_style),
        HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=10),
        Spacer(1, 5)
    ]

    questions = [
        {
            "num": 1,
            "topic": "Quantitative",
            "diff": "medium",
            "q": "A train running at a speed of 60 km/hr crosses a telephone pole in 9 seconds. What is the length of the train in metres?",
            "opts": ["A) 120 metres", "B) 180 metres", "C) 150 metres", "D) 324 metres"],
            "ans": "Answer: C",
            "expl": "Explanation: Speed in m/s = 60 * (5/18) = 50/3 m/s. Length of train = Speed * Time = (50/3) * 9 = 150 metres."
        },
        {
            "num": 2,
            "topic": "Quantitative",
            "diff": "medium",
            "q": "If A can complete a work in 12 days and B can complete the same work in 24 days, in how many days can they complete the work working together?",
            "opts": ["A) 6 days", "B) 8 days", "C) 10 days", "D) 9 days"],
            "ans": "Answer: B",
            "expl": "Explanation: 1/A + 1/B = 1/12 + 1/24 = 3/24 = 1/8. Together they complete the work in 8 days."
        },
        {
            "num": 3,
            "topic": "Logical Reasoning",
            "diff": "easy",
            "q": "Pointing to a photograph of a boy, Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?",
            "opts": ["A) Brother", "B) Uncle", "C) Father", "D) Grandfather"],
            "ans": "Answer: C",
            "expl": "Explanation: The only son of Suresh's mother is Suresh himself. Therefore, the boy is Suresh's son, making Suresh his father."
        },
        {
            "num": 4,
            "topic": "Logical Reasoning",
            "diff": "medium",
            "q": "Find the odd number out in the series: 3, 5, 11, 14, 17, 21",
            "opts": ["A) 21", "B) 17", "C) 14", "D) 3"],
            "ans": "Answer: C",
            "expl": "Explanation: Every number in the series except 14 is prime and odd, whereas 14 is an even composite number."
        },
        {
            "num": 5,
            "topic": "Quantitative",
            "diff": "easy",
            "q": "A vendor bought toffees at 6 for a rupee. How many for a rupee must he sell to gain 20% profit?",
            "opts": ["A) 3", "B) 4", "C) 5", "D) 6"],
            "ans": "Answer: C",
            "expl": "Explanation: Cost Price of 6 toffees = Re 1. Selling Price of 6 toffees = 120% of 1 = Rs 1.20. For Re 1, number of toffees sold = 6 / 1.20 = 5 toffees."
        },
        {
            "num": 6,
            "topic": "Logical Reasoning",
            "diff": "medium",
            "q": "A man walks 5 km South and then turns to the right. After walking 3 km he turns to the left and walks 5 km. In which direction is he now from his starting point?",
            "opts": ["A) West", "B) South", "C) North-East", "D) South-West"],
            "ans": "Answer: D",
            "expl": "Explanation: The man moves 5 km South, 3 km West (right turn from south), and 5 km South again (left turn from west). Relative to start, he is South-West."
        },
        {
            "num": 7,
            "topic": "Verbal Ability",
            "diff": "easy",
            "q": "Choose the word that is most nearly OPPOSITE in meaning to the word 'FRUGAL':",
            "opts": ["A) Economical", "B) Extravagant", "C) Miserly", "D) Prudent"],
            "ans": "Answer: B",
            "expl": "Explanation: 'Frugal' means sparing or economical with money or food. The opposite is 'Extravagant' (spending recklessly)."
        },
        {
            "num": 8,
            "topic": "Quantitative",
            "diff": "hard",
            "q": "A sum of money invested at compound interest doubles itself in 4 years. In how many years will it amount to 8 times itself at the same rate?",
            "opts": ["A) 8 years", "B) 12 years", "C) 16 years", "D) 24 years"],
            "ans": "Answer: B",
            "expl": "Explanation: Under compound interest, if P becomes 2P in 4 years, it becomes 4P in 8 years, and 8P in 12 years (2^3 = 8, so 3 * 4 = 12 years)."
        },
        {
            "num": 9,
            "topic": "Logical Reasoning",
            "diff": "hard",
            "q": "Statements: (I) All cats are dogs. (II) Some dogs are birds. Conclusions: (1) Some cats are birds. (2) Some birds are dogs.",
            "opts": ["A) Only (1) follows", "B) Only (2) follows", "C) Either (1) or (2) follows", "D) Neither (1) nor (2) follows"],
            "ans": "Answer: B",
            "expl": "Explanation: Since 'Some dogs are birds' converts directly into 'Some birds are dogs', conclusion (2) definitely follows. Conclusion (1) cannot be definitively inferred."
        },
        {
            "num": 10,
            "topic": "Verbal Ability",
            "diff": "medium",
            "q": "Select the correct phrase to complete the sentence: 'Despite facing severe obstacles, the startup managed to _______ and achieved profitability within two years.'",
            "opts": ["A) bite the bullet", "B) throw in the towel", "C) weather the storm", "D) burn bridges"],
            "ans": "Answer: C",
            "expl": "Explanation: The idiom 'weather the storm' means to successfully survive a period of severe difficulty or danger."
        }
    ]

    for item in questions:
        story.append(Paragraph(f"{item['num']}. {item['q']}", q_style))
        meta_line = f"Topic: {item['topic']} | Difficulty: {item['diff'].capitalize()}"
        story.append(Paragraph(meta_line, badge_style))
        for opt in item['opts']:
            story.append(Paragraph(opt, opt_style))
        story.append(Paragraph(item['ans'], ans_style))
        story.append(Paragraph(item['expl'], expl_style))

    doc.build(story)
    print(f"Sample PDF generated successfully at: {output_path}")

if __name__ == '__main__':
    root_dest = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'sample_question_bank.pdf'))
    db_dest = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'sample_faculty_questions.pdf'))
    
    create_sample_faculty_pdf(root_dest)
    create_sample_faculty_pdf(db_dest)
