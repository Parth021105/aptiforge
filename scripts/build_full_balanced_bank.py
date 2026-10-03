import os
import json
import sys

# Import questions list from generate_balanced_bank which already has 52 Quantitative questions
from generate_balanced_bank import questions, add_q

# ==========================================
# 2. LOGICAL REASONING (52 Questions: 20 Easy, 20 Medium, 12 Hard)
# ==========================================

# --- 20 Easy Logical Reasoning ---
add_q("Logical Reasoning", "Blood Relations", "easy",
      "Pointing to a photograph of a boy, Suresh said, 'He is the son of the only son of my mother.' How is Suresh related to that boy?",
      ["Brother", "Uncle", "Father", "Grandfather"], 2,
      "The only son of Suresh's mother is Suresh himself. Therefore, the boy is the son of Suresh, so Suresh is his father.",
      "Identify who 'the only son of my mother' is first.",
      "Suresh's mother's only son is Suresh. So the boy is Suresh's son.")

add_q("Logical Reasoning", "Blood Relations", "easy",
      "A is the sister of B. B is the daughter of C. How is A related to C?",
      ["Daughter", "Sister", "Mother", "Niece"], 0,
      "Since B is the daughter of C, and A is the sister of B, A is also the daughter of C.",
      "Consider the direct vertical parent-child link through B.",
      "If B is C's daughter, her sister A must also be C's daughter.")

add_q("Logical Reasoning", "Direction Sense", "easy",
      "A person walks 5 km North, then turns right and walks 4 km. Which direction is he facing now?",
      ["North", "East", "South", "West"], 1,
      "Starting facing North, turning 90 degrees clockwise (right) points towards East.",
      "Imagine the compass rose: turning right from North leads East.",
      "Clockwise 90° from North is East.")

add_q("Logical Reasoning", "Direction Sense", "easy",
      "Rohan starts from his house and walks 20m South, then turns left and walks 15m. In which direction is he from his house?",
      ["North-East", "South-East", "South-West", "North-West"], 1,
      "He moved South (negative Y) and East (positive X). His position relative to start is South-East.",
      "Combine the two orthogonal vectors: South and East.",
      "Position vector is (15m East, 20m South) = South-East.")

add_q("Logical Reasoning", "Code Decoding", "easy",
      "If 'CAT' is coded as 'DBU', how is 'DOG' coded in that same language?",
      ["EPH", "EPI", "FPH", "EOH"], 0,
      "Each letter is shifted by +1: D->E, O->P, G->H. Hence EPH.",
      "Check the forward alphabetical shift for each individual letter.",
      "C+1=D, A+1=B, T+1=U. Apply +1 to D, O, G.")

add_q("Logical Reasoning", "Code Decoding", "easy",
      "In a code language, 'APPLE' is written as 'ELPPA'. How is 'MANGO' written?",
      ["OGNAM", "OGMAN", "OGAMN", "ONMAG"], 0,
      "The letters of the word are written in exact reverse order: M-A-N-G-O becomes O-G-N-A-M.",
      "Observe the order of the letters from end to beginning.",
      "Reverse spelling: O, G, N, A, M.")

add_q("Logical Reasoning", "Series & Analogy", "easy",
      "Find the next number in the sequence: 2, 4, 8, 16, 32, ?",
      ["48", "60", "64", "72"], 2,
      "Each term is multiplied by 2 (powers of 2): 32 * 2 = 64.",
      "Look at the constant ratio between consecutive terms.",
      "Multiply 32 by 2.")

add_q("Logical Reasoning", "Series & Analogy", "easy",
      "Complete the number series: 5, 10, 15, 20, 25, ?",
      ["28", "30", "32", "35"], 1,
      "The series increases by a constant common difference of +5: 25 + 5 = 30.",
      "Identify the constant difference between consecutive terms.",
      "Add 5 to 25.")

add_q("Logical Reasoning", "Series & Analogy", "easy",
      "Book is to Reading as Fork is to:",
      ["Writing", "Eating", "Cooking", "Cutting"], 1,
      "A book is an instrument used for reading; a fork is an instrument used for eating.",
      "Identify the primary functional relationship of the tool.",
      "Book is read; fork is used to eat.")

add_q("Logical Reasoning", "Odd One Out", "easy",
      "Find the odd one out: Apple, Banana, Carrot, Mango.",
      ["Apple", "Banana", "Carrot", "Mango"], 2,
      "Apple, Banana, and Mango are fruits; Carrot is a root vegetable.",
      "Classify by biological/botanical category.",
      "Carrot is a vegetable; the other three are fruits.")

add_q("Logical Reasoning", "Odd One Out", "easy",
      "Find the odd number: 11, 13, 15, 17, 19.",
      ["11", "13", "15", "17"], 2,
      "11, 13, 17, and 19 are all prime numbers, whereas 15 is a composite number (3 * 5).",
      "Check prime vs composite properties.",
      "15 is divisible by 3 and 5; others are prime.")

add_q("Logical Reasoning", "Clocks & Calendar", "easy",
      "If today is Wednesday, what day of the week will it be after 14 days?",
      ["Tuesday", "Wednesday", "Thursday", "Friday"], 1,
      "14 days = exactly 2 weeks (0 odd days). The day remains Wednesday.",
      "Divide the number of days by 7 to determine the remainder.",
      "14 mod 7 = 0 remainder. Day remains the same.")

add_q("Logical Reasoning", "Clocks & Calendar", "easy",
      "How many hours are there between 9:00 AM on Monday and 9:00 AM on Wednesday?",
      ["24 hours", "36 hours", "48 hours", "72 hours"], 2,
      "Monday 9 AM to Tuesday 9 AM = 24h. Tuesday 9 AM to Wednesday 9 AM = 24h. Total = 48 hours.",
      "Count the number of full 24-hour day cycles.",
      "2 full days * 24 hours = 48 hours.")

add_q("Logical Reasoning", "Syllogisms", "easy",
      "Statements: All cats are animals. All animals need water. Conclusion: All cats need water.",
      ["Definitely True", "Definitely False", "Probably True", "Cannot be determined"], 0,
      "By transitive property of universal affirmatives: Cats ⊆ Animals ⊆ Need Water. Definitely true.",
      "Draw two concentric Venn circles: Cats inside Animals, Animals inside Need Water.",
      "Cats are completely enclosed in Need Water.")

add_q("Logical Reasoning", "Syllogisms", "easy",
      "Statements: Some pens are pencils. Some pencils are erasers. Can we conclude: All pens are erasers?",
      ["Yes", "No", "Maybe", "Insufficient data"], 1,
      "Two particular premises ('some') cannot yield a universal affirmative conclusion ('all'). No.",
      "Universal affirmative ('all') requires complete containment, which particular premises cannot establish.",
      "Partial intersections do not establish total containment.")

add_q("Logical Reasoning", "Seating Arrangement", "easy",
      "Five persons A, B, C, D, E are sitting in a row facing north. C is in the middle. How many people sit to the right of C?",
      ["1", "2", "3", "4"], 1,
      "In a 5-person row with indices 1, 2, 3, 4, 5, the middle is position 3. Two persons (4 and 5) sit to the right.",
      "Count positions on either side of the center in a 5-element line.",
      "5 elements: 2 on left, 1 in middle, 2 on right.")

add_q("Logical Reasoning", "Ranking", "easy",
      "In a class of 30 students, Rahul's rank is 10th from the top. What is his rank from the bottom?",
      ["20th", "21st", "22nd", "23rd"], 1,
      "Rank from bottom = Total - Rank from top + 1 = 30 - 10 + 1 = 21st.",
      "Total = (Rank from top) + (Rank from bottom) - 1.",
      "30 - 10 + 1 = 21.")

add_q("Logical Reasoning", "Alphabet Test", "easy",
      "Which letter is 5th to the right of the 10th letter from the left in the English alphabet?",
      ["N", "O", "P", "Q"], 1,
      "10th letter from left = J (10). 5th to the right = 10 + 5 = 15th letter = O.",
      "Add the positions: 10 + 5 = 15.",
      "15th letter in alphabet is O.")

add_q("Logical Reasoning", "Puzzles", "easy",
      "If day before yesterday was Thursday, what day will tomorrow be?",
      ["Saturday", "Sunday", "Monday", "Tuesday"], 1,
      "Day before yesterday = Thursday => Yesterday = Friday => Today = Saturday => Tomorrow = Sunday.",
      "Establish today's day of the week first.",
      "Today is Saturday (two days after Thursday). Tomorrow is Sunday.")

add_q("Logical Reasoning", "Matrix Logic", "easy",
      "In a group of 10 people, 6 like tea and 5 like coffee. If 2 like both, how many like neither?",
      ["1", "2", "3", "4"], 0,
      "n(T U C) = 6 + 5 - 2 = 9. Neither = 10 - 9 = 1 person.",
      "n(T U C) = n(T) + n(C) - n(Both).",
      "6 + 5 - 2 = 9. 10 - 9 = 1.")

# --- 20 Medium Logical Reasoning ---
add_q("Logical Reasoning", "Blood Relations", "medium",
      "Pointing to a photograph, Rahul said, 'She is the daughter of my grandfather's only son.' How is she related to Rahul?",
      ["Mother", "Sister", "Cousin", "Aunt"], 1,
      "Grandfather's only son is Rahul's father. Daughter of Rahul's father is Rahul's sister.",
      "Identify 'my grandfather's only son' first.",
      "Grandfather's only son is Rahul's father. Father's daughter is Rahul's sister.")

add_q("Logical Reasoning", "Code Decoding", "medium",
      "In a certain code language, 'COMPUTER' is written as 'RFUVQNPC'. How is 'MEDICINE' written?",
      ["EOJDJEFM", "EOJDEJFM", "MFEJDJOE", "EOJDJFEM"], 0,
      "Reverse the word and add +1 to each inner letter. MEDICINE reversed is ENICIDEM. Inner letters +1 gives EOJDJEFM.",
      "Notice first and last letter positions, and the shift of internal letters.",
      "Word is reversed then inner letters shifted +1.")

add_q("Logical Reasoning", "Direction Sense", "medium",
      "A man walks 30m South, turns left and walks 40m, turns left again and walks 30m. How far is he from his start point?",
      ["30m", "40m", "50m", "70m"], 1,
      "South and North cancel (30m South then 30m North). Remaining displacement is 40m East.",
      "Track net vertical (North-South) and net horizontal (East-West) movement.",
      "Vertical displacement is 0. Horizontal displacement is 40m.")

add_q("Logical Reasoning", "Syllogisms", "medium",
      "Statements: Some managers are leaders. All leaders are visionaries. Conclusions: 1. Some managers are visionaries. 2. Some visionaries are managers.",
      ["Only 1 follows", "Only 2 follows", "Neither follows", "Both 1 and 2 follow"], 3,
      "Managers that are leaders are visionaries, so Some managers are visionaries (1). By conversion, Some visionaries are managers (2). Both follow.",
      "Check intersection of Managers with the inclusive circle of Visionaries.",
      "Both conclusions are symmetrical deductions from the Venn diagram.")

add_q("Logical Reasoning", "Seating Arrangement", "medium",
      "Six friends P, Q, R, S, T, U sit in a circle facing the center. R is between P and Q. U is to the immediate left of P. Who is right of Q?",
      ["R", "S", "T", "U"], 0,
      "Arranging in circle: Going counter-clockwise from P gives R, then Q. Hence R is to immediate right of Q.",
      "Place P, R, Q consecutively facing center.",
      "R sits directly between P and Q, so to Q's right is R.")

add_q("Logical Reasoning", "Clocks & Calendar", "medium",
      "What is the angle between the hands of a clock at 5:20?",
      ["40°", "45°", "50°", "55°"], 0,
      "Angle = |30*H - 5.5*M| = |30*5 - 5.5*20| = |150 - 110| = 40°.",
      "Apply the clock angle formula |30H - 5.5M|.",
      "|150 - 110| = 40°.")

add_q("Logical Reasoning", "Clocks & Calendar", "medium",
      "How many leap years are there in a standard period of 100 consecutive years?",
      ["24", "25", "26", "28"], 0,
      "100 / 4 = 25, but the century year (e.g. 1900, 2100) is only a leap year if divisible by 400. Thus 25 - 1 = 24 leap years.",
      "Remember that century years require divisibility by 400.",
      "25 multiples of 4 minus the non-400 century year = 24.")

add_q("Logical Reasoning", "Series & Analogy", "medium",
      "Find the missing term: 4, 9, 25, 49, 121, ?",
      ["144", "169", "196", "225"], 1,
      "The terms are squares of consecutive prime numbers: 2^2, 3^2, 5^2, 7^2, 11^2, 13^2 = 169.",
      "Identify the sequence of base numbers whose squares are listed.",
      "Bases are primes: 2, 3, 5, 7, 11, next is 13. 13^2 = 169.")

add_q("Logical Reasoning", "Series & Analogy", "medium",
      "In a certain sequence: 7, 14, 42, 168, ?, what is the next number?",
      ["504", "672", "840", "1008"], 2,
      "Multipliers increase: *2, *3, *4, *5. 168 * 5 = 840.",
      "Determine the multiplier applied to each successive step.",
      "7*2=14, 14*3=42, 42*4=168, 168*5 = 840.")

add_q("Logical Reasoning", "Critical Reasoning", "medium",
      "Statement: 'The company decided to recruit only candidates with certifications.' Assumption I: Certified candidates are more skilled. Assumption II: Non-certified candidates cannot learn.",
      ["Only I is implicit", "Only II is implicit", "Both are implicit", "Neither is implicit"], 0,
      "The management assumes certification correlates with skill (I), but does not assume non-certified cannot learn (II). Only I is implicit.",
      "Evaluate which assumption is necessary to justify the policy.",
      "Assumption I directly supports hiring preference; Assumption II is an extreme generalization.")

add_q("Logical Reasoning", "Data Sufficiency", "medium",
      "What is the value of x? Statement I: 2x + 3 = 11. Statement II: x^2 = 16.",
      ["I alone is sufficient", "II alone is sufficient", "Both together needed", "Neither is sufficient"], 0,
      "From I: 2x = 8 => x = 4 (unique value). From II: x can be +4 or -4 (not unique). Hence I alone is sufficient.",
      "A statement is sufficient only if it yields a single unique answer.",
      "Statement I gives x = 4 uniquely.")

add_q("Logical Reasoning", "Puzzles", "medium",
      "Four cars A, B, C, D are in a race. A finished before B but after C. D finished after B. Who won the race?",
      ["A", "B", "C", "D"], 2,
      "Order: C finished before A, A before B, B before D. Order: C > A > B > D. C won.",
      "Construct the finish order from earliest to latest.",
      "C > A > B > D. C is first.")

add_q("Logical Reasoning", "Puzzles", "medium",
      "In an apartment of 5 floors (1 to 5), Anita lives on an odd floor above floor 2. Bina lives immediately below Anita. Which floor does Bina live on?",
      ["Floor 1", "Floor 2", "Floor 3", "Floor 4"], 1,
      "Odd floors above 2 are 3 and 5. If Anita is on 3, Bina is on 2. If Anita on 5, Bina on 4. Wait: If Anita is on 3, Bina on 2.",
      "Test possible odd floors above 2.",
      "Floor 3 gives floor 2 below.")

add_q("Logical Reasoning", "Ranking", "medium",
      "In a queue of 45 people, Ramesh is 18th from the front and Suresh is 12th from the back. How many people are between them?",
      ["13", "14", "15", "16"], 2,
      "Total occupied = 18 + 12 = 30. People in between = 45 - 30 = 15 people.",
      "Subtract the sum of ranks from total when there is no overlap.",
      "45 - (18 + 12) = 45 - 30 = 15.")

add_q("Logical Reasoning", "Ranking", "medium",
      "A is taller than B but shorter than C. D is taller than E but shorter than B. Who is the tallest?",
      ["A", "B", "C", "D"], 2,
      "C > A > B and B > D > E. Combined: C > A > B > D > E. C is tallest.",
      "Chain the inequality relations.",
      "C is taller than A, who is taller than all others.")

add_q("Logical Reasoning", "Code Decoding", "medium",
      "If 'STRONG' is coded as 'TVTQPI', what is the pattern?",
      ["+1, +1, +1...", "+1, +2, +1, +2...", "+1, +2, +3...", "+2, +2, +2..."], 1,
      "S(+1)->T, T(+2)->V, R(+1)->S... wait: R(+2)->T, O(+1)->P, N(+2)->P, G(+2)->I. Pattern is alternating +1 and +2.",
      "Calculate the difference between original and coded letters.",
      "S(19)->T(20) [+1], T(20)->V(22) [+2], etc.")

add_q("Logical Reasoning", "Direction Sense", "medium",
      "A girl facing South-East turns 90° clockwise, then 180° counter-clockwise. Which direction is she facing now?",
      ["North-East", "South-West", "North-West", "South"], 0,
      "Net rotation = -90° + 180° = +90° counter-clockwise. South-East + 90° CCW = North-East.",
      "Compute the net angular shift.",
      "90° clockwise followed by 180° counter-clockwise is net 90° counter-clockwise. SE to NE.")

add_q("Logical Reasoning", "Blood Relations", "medium",
      "If 'A + B' means A is father of B; 'A - B' means A is sister of B. What does 'P + Q - R' mean?",
      ["P is uncle of R", "P is father of R", "P is brother of R", "P is grandfather of R"], 1,
      "P is father of Q. Q is sister of R. Therefore P is also the father of R.",
      "Q and R are siblings with the same father P.",
      "P is the father of both Q and R.")

add_q("Logical Reasoning", "Syllogisms", "medium",
      "Statements: No paper is plastic. All plastic is toxic. Conclusion: Some toxic things are not paper.",
      ["Definitely True", "Definitely False", "Doubtful", "Cannot be determined"], 0,
      "Plastics are toxic, and no plastic is paper. Hence the toxic things that are plastic cannot be paper. Definitely True.",
      "Consider the subset of toxic entities that are plastic.",
      "Plastic items are toxic and cannot be paper.")

add_q("Logical Reasoning", "Matrix Logic", "medium",
      "Three boxes are labeled Red, Blue, and Mixed. All three labels are known to be incorrect. You pick one ball from the 'Mixed' box and it is Red. What is in the box labeled 'Blue'?",
      ["Red", "Blue", "Mixed", "Empty"], 2,
      "Since all labels are false, 'Mixed' cannot be mixed; since it has a Red ball, it must be 'Red'. 'Blue' box cannot be Blue and cannot be Red, so it must be 'Mixed'.",
      "Start with the box labeled 'Mixed' because its true identity is immediately resolved.",
      "Box labeled Mixed is Red. Box labeled Blue cannot be Blue or Red, so it is Mixed.")

# --- 12 Hard Logical Reasoning ---
add_q("Logical Reasoning", "Blood Relations", "hard",
      "If 'A + B' means A is brother of B; 'A - B' means A is sister of B; 'A * B' means A is father of B. Which shows 'M is uncle of N'?",
      ["M + K * N", "M - K * N", "M * K + N", "M + K - N"], 0,
      "M + K means M is brother of K. K * N means K is father of N. Brother of father is uncle. So M is uncle of N.",
      "Look for an expression where M is the brother of N's father.",
      "M + K (brother) and K * N (father) makes M uncle of N.")

add_q("Logical Reasoning", "Syllogisms", "hard",
      "Statements: Only a few engineers are managers. All managers are leaders. No leader is a poet. Conclusions: 1. Some engineers are definitely not poets. 2. All engineers being leaders is a possibility.",
      ["Only 1 follows", "Only 2 follows", "Both follow", "Neither follows"], 2,
      "Engineers who are managers are leaders and cannot be poets, so some engineers are not poets (1). Since only a few engineers are managers, all engineers could still be leaders without all being managers (2). Both follow.",
      "Analyze the 'only a few' constraint carefully against universal possibility.",
      "Conclusion 1 is a direct deduction; Conclusion 2 does not violate 'only a few managers'.")

add_q("Logical Reasoning", "Seating Arrangement", "hard",
      "8 executives A-H sit in a circle. Four face center and four face outwards. A sits 3rd right of B who faces center. C sits 2nd left of A. Who sits opposite B?",
      ["E", "F", "G", "H"], 1,
      "Tracing orientations and circular coordinates reveals F sits directly opposite B.",
      "Fix B facing inward at position 0, then position A at 3.",
      "Analyze alternate facing constraints to identify the opposite node.")

add_q("Logical Reasoning", "Critical Reasoning", "hard",
      "City X added bicycle lanes and emissions dropped 15%. Mayor claims bike lanes caused the reduction. Which most weakens the claim?",
      ["A massive steel mill in City X shut down during the same period.", "Bike sales rose 5%.", "Traffic police issued more fines.", "Public transit added 2 routes."], 0,
      "The shutdown of a heavy steel mill offers a massive confounding variable that accounts for the emission drop.",
      "Look for an alternative cause that accounts for the observed outcome.",
      "The industrial shutdown accounts for the emissions drop independent of bike lanes.")

add_q("Logical Reasoning", "Clocks & Calendar", "hard",
      "An accurate clock shows 8 o'clock in the morning. Through how many degrees will the hour hand rotate when it shows 2 o'clock in the afternoon?",
      ["144°", "150°", "168°", "180°"], 3,
      "From 8 AM to 2 PM is 6 hours. Hour hand moves 30° per hour. 6 * 30° = 180°.",
      "Hour hand rotation rate is 360° / 12 = 30° per hour.",
      "6 hours * 30° = 180°.")

add_q("Logical Reasoning", "Puzzles", "hard",
      "Seven boxes J, K, L, M, N, O, P are placed in a stack. Only 2 boxes between K and L. O is immediately above P. Three boxes between J and O. Which box is at bottom?",
      ["J", "M", "P", "N"], 2,
      "Evaluating vertical stack constraints places P at the lowest position (bottom).",
      "Chain the vertical distance constraints between J, O, and P.",
      "P is fixed at the base of the valid permutation.")

add_q("Logical Reasoning", "Input-Output", "hard",
      "A machine sorts words alphabetically in reverse order from left to right. Input: 'zen cat dog lion'. What is Step 1?",
      ["zen cat dog lion", "zen lion dog cat", "zen lion cat dog", "lion zen cat dog"], 0,
      "'zen' is already the highest alphabetical word, so it remains in position 1 in Step 1.",
      "Machine targets the alphabetically highest word first.",
      "'zen' is already at the first position.")

add_q("Logical Reasoning", "Data Sufficiency", "hard",
      "Who is the oldest among P, Q, and R? Statement I: P is older than Q. Statement II: R is not the oldest.",
      ["I alone sufficient", "II alone sufficient", "Both together sufficient", "Neither sufficient"], 2,
      "From I: P > Q. From II: R is not oldest, so either P or Q is oldest. Since P > Q, P must be the oldest. Both together are sufficient.",
      "Combine the inequality P > Q with the elimination of R.",
      "Since R is not oldest and P > Q, P must be the oldest.")

add_q("Logical Reasoning", "Code Decoding", "hard",
      "In a matrix coding system, if 'BRISK' is coded as '24, 18, 09, 19, 11' based on letter coordinates, how is 'CALM' coded?",
      ["03, 01, 12, 13", "03, 02, 12, 14", "04, 01, 12, 13", "03, 01, 11, 13"], 0,
      "Direct two-digit alphabetical position: C=03, A=01, L=12, M=13.",
      "Observe that each coordinate maps directly to the standard A=1..Z=26 index with leading zeroes.",
      "C=03, A=01, L=12, M=13.")

add_q("Logical Reasoning", "Series & Analogy", "hard",
      "Find the missing number in the series: 3, 10, 29, 66, 127, ?",
      ["216", "218", "222", "225"], 1,
      "The pattern is n^3 + 2: 1^3+2=3, 2^3+2=10, 3^3+2=29, 4^3+2=66, 5^3+2=127, 6^3+2 = 216 + 2 = 218.",
      "Compare each number to perfect cubes (1, 8, 27, 64, 125, 216).",
      "Each number is n^3 + 2. 6^3 + 2 = 218.")

add_q("Logical Reasoning", "Direction Sense", "hard",
      "One morning after sunrise, Suresh was facing a pole. The shadow of the pole fell exactly to his right. Which direction was Suresh facing?",
      ["East", "West", "North", "South"], 3,
      "Sun is in the East in morning, so shadows point West. If West is to his right, Suresh must be facing South.",
      "Morning shadows always point West.",
      "If right arm points West, facing direction is South.")

add_q("Logical Reasoning", "Critical Reasoning", "hard",
      "Statement: 'Should all nuclear power plants be phased out immediately?' Argument I: Yes, nuclear disasters cause irreversible contamination. Argument II: No, it provides zero-emission baseload power.",
      ["Only I is strong", "Only II is strong", "Both I and II are strong", "Neither is strong"], 2,
      "Both arguments address crucial national safety and clean energy sustainability issues with valid premises. Both are strong.",
      "Assess whether each argument is substantive and directly addresses national policy consequences.",
      "Both represent fundamental, valid real-world policy considerations.")

print(f"Total Logical Reasoning: {len([q for q in questions if q['category'] == 'Logical Reasoning'])}")

# ==========================================
# 3. VERBAL ABILITY (52 Questions: 20 Easy, 20 Medium, 12 Hard)
# ==========================================

# --- 20 Easy Verbal Ability ---
add_q("Verbal Ability", "Vocabulary", "easy",
      "Choose the word that is most nearly SYNONYMOUS with 'CANDID':",
      ["Deceptive", "Frank", "Shy", "Arrogant"], 1,
      "'Candid' means truthful, straightforward, and frank.",
      "Think of a 'candid photo'—unposed, natural, and honest.",
      "Frank means open and sincere.")

add_q("Verbal Ability", "Vocabulary", "easy",
      "Choose the word that is most nearly OPPOSITE in meaning to 'ANCIENT':",
      ["Historic", "Modern", "Antique", "Aged"], 1,
      "'Ancient' refers to times long past; its antonym is 'Modern'.",
      "Opposite of belonging to the distant past.",
      "Modern means relating to the present or recent times.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Identify the correct spelling:",
      ["Accomodate", "Accommodate", "Acommodate", "Accommode"], 1,
      "The correct spelling has double 'c' and double 'm': 'Accommodate'.",
      "Remember: It accommodates two 'c's and two 'm's.",
      "A-C-C-O-M-M-O-D-A-T-E.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Choose the correct sentence:",
      ["She don't like coffee.", "She doesn't likes coffee.", "She doesn't like coffee.", "She do not like coffee."], 2,
      "Third-person singular 'She' takes auxiliary 'does not' followed by bare infinitive 'like'.",
      "Third-person singular requires 'does', and main verb stays in base form.",
      "'She doesn't like' is grammatically correct.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Fill in the blank: 'He has been living in London ______ 2018.'",
      ["for", "since", "from", "by"], 1,
      "'Since' is used for a specific starting point in time in the past.",
      "Use 'since' for a fixed point in time, and 'for' for a duration.",
      "2018 is a specific point in time, so use 'since'.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Choose the correct pronoun: 'Either John or David forgot ______ keys.'",
      ["their", "his", "them", "him"], 1,
      "Singular antecedents joined by 'or' take a singular pronoun ('his').",
      "When two singular nouns are joined by 'or', the pronoun remains singular.",
      "Both John and David are singular males, so use 'his'.")

add_q("Verbal Ability", "Idioms & Phrases", "easy",
      "What does the idiom 'Piece of cake' mean?",
      ["Delicious dessert", "Very easy task", "Difficult challenge", "Expensive item"], 1,
      "'Piece of cake' colloquially signifies an effortless or simple task.",
      "Refers to something that requires little to no effort.",
      "Means very easy.")

add_q("Verbal Ability", "Idioms & Phrases", "easy",
      "What is the meaning of 'Once in a blue moon'?",
      ["Very frequently", "Very rarely", "Every month", "At nighttime"], 1,
      "'Once in a blue moon' means an event that occurs very infrequently or rarely.",
      "A blue moon is an uncommon astronomical occurrence.",
      "Indicates something that happens very rarely.")

add_q("Verbal Ability", "Vocabulary", "easy",
      "Choose the synonym for 'GENEROUS':",
      ["Stingy", "Benevolent", "Greedy", "Hostile"], 1,
      "'Benevolent' means well-meaning and kindly; generous in giving.",
      "Look for a word that implies kindness and willingness to share.",
      "Benevolent means generous and charitable.")

add_q("Verbal Ability", "Vocabulary", "easy",
      "Choose the antonym of 'OPTIMISTIC':",
      ["Hopeful", "Pessimistic", "Cheerful", "Confident"], 1,
      "'Optimistic' means positive and expecting the best; its antonym is 'Pessimistic'.",
      "Opposite of expecting favorable outcomes.",
      "Pessimistic means expecting the worst.")

add_q("Verbal Ability", "Cloze Test", "easy",
      "The teacher asked the students to pay ______ to the lecture.",
      ["attendance", "attention", "intention", "attraction"], 1,
      "The idiomatic collocation is 'to pay attention'.",
      "Standard English verb-noun pair for listening carefully.",
      "'Pay attention' is the standard phrase.")

add_q("Verbal Ability", "Cloze Test", "easy",
      "She was commended for her ______ honesty during the audit.",
      ["impeccable", "flawed", "dubious", "mediocre"], 0,
      "'Impeccable' means flawless or of highest standard.",
      "Look for an unambiguously positive adjective praising honesty.",
      "Impeccable means faultless.")

add_q("Verbal Ability", "Reading Comprehension", "easy",
      "Passage: 'Regular physical exercise strengthens the cardiovascular system and releases endorphins, which improve mood.' What is a primary benefit of exercise mentioned?",
      ["It induces fatigue", "It releases endorphins that elevate mood", "It cures all diseases", "It replaces sleep"], 1,
      "The passage explicitly states exercise 'releases endorphins, which improve mood.'",
      "Direct textual retrieval from the second clause.",
      "Exercise releases endorphins that enhance mood.")

add_q("Verbal Ability", "Reading Comprehension", "easy",
      "Passage: 'Solar energy is a renewable power source that emits zero greenhouse gases during operation.' Why is solar energy environmentally beneficial?",
      ["It is expensive", "It emits zero greenhouse gases during operation", "It operates at night", "It requires coal"], 1,
      "Text directly highlights that it emits zero greenhouse gases.",
      "Scan for the stated environmental attribute.",
      "Zero operational emissions.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Select the word with correct spelling:",
      ["Receive", "Recieve", "Receeve", "Receve"], 0,
      "The rule is 'i before e except after c': R-E-C-E-I-V-E.",
      "Remember 'i before e except after c'.",
      "Follows 'c', so 'ei': Receive.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Choose the correct preposition: 'He is proficient ______ mathematics.'",
      ["at", "in", "with", "on"], 1,
      "One is said to be 'proficient in' a subject or skill.",
      "The standard preposition paired with 'proficient' is 'in'.",
      "Proficient in mathematics.")

add_q("Verbal Ability", "Para Jumbles", "easy",
      "Arrange into order: 1. He woke up early. 2. He brushed his teeth. 3. He had breakfast. 4. He caught the bus.",
      ["1-2-3-4", "2-1-3-4", "4-3-2-1", "1-3-2-4"], 0,
      "Chronological sequence of a morning routine: Wake up -> Brush -> Breakfast -> Catch bus.",
      "Follow natural chronological morning events.",
      "1, 2, 3, 4 is the logical chronological flow.")

add_q("Verbal Ability", "Vocabulary", "easy",
      "What is the meaning of 'RELUCTANT'?",
      ["Eager", "Unwilling or hesitant", "Enthusiastic", "Careless"], 1,
      "'Reluctant' means unwilling and hesitant.",
      "Opposite of willing or enthusiastic.",
      "Unwilling or disinclined.")

add_q("Verbal Ability", "Sentence Correction", "easy",
      "Fill in the blank: 'Neither of the answers ______ correct.'",
      ["is", "are", "were", "have been"], 0,
      "'Neither' is grammatically singular and takes the singular verb 'is'.",
      "Subject 'Neither' governs a singular verb.",
      "Use singular 'is'.")

add_q("Verbal Ability", "Idioms & Phrases", "easy",
      "What does 'Call it a day' mean?",
      ["Start working", "Stop working on something", "Celebrate a birthday", "Plan a schedule"], 1,
      "'Call it a day' means to decide to stop working for the rest of the day.",
      "Indicates concluding current activity.",
      "Stop working for the day.")

# --- 20 Medium Verbal Ability ---
add_q("Verbal Ability", "Sentence Correction", "medium",
      "Choose the grammatically correct sentence:",
      ["Neither of the managers were able to submit their reports.", "Neither of the managers was able to submit his report.", "Neither of the managers were able to submit his report.", "Neither of the managers was able to submit their report."], 1,
      "'Neither' is singular requiring singular verb 'was' and pronoun referent 'his'.",
      "'Neither' governs singular agreement throughout.",
      "'was able to submit his report' is grammatically precise.")

add_q("Verbal Ability", "Sentence Correction", "medium",
      "Select the sentence that maintains proper parallelism:",
      ["She enjoys hiking, to swim, and reading novels.", "She enjoys to hike, swimming, and reading novels.", "She enjoys hiking, swimming, and reading novels.", "She enjoys hiking, swimming, and to read novels."], 2,
      "All three actions must share the gerund form: hiking, swimming, and reading.",
      "Ensure all items in the series share identical grammatical form.",
      "Gerunds: hiking, swimming, reading.")

add_q("Verbal Ability", "Sentence Correction", "medium",
      "Select the correct sentence:",
      ["Between you and I, this merger will be disastrous.", "Between you and me, this merger will be disastrous.", "Between you and myself, this merger will be disastrous.", "Between you and me, this merger would had been disastrous."], 1,
      "'Between' is a preposition requiring objective pronouns ('me', not 'I').",
      "Prepositions govern objective case pronouns.",
      "'Between you and me' is correct.")

add_q("Verbal Ability", "Para Jumbles", "medium",
      "Arrange: P: Digital payments expanded rapidly. Q: Consequently, cyber security became vital. R: In recent years, smartphones enabled this shift. S: However, vulnerabilities also emerged.",
      ["R-P-S-Q", "P-R-Q-S", "R-S-P-Q", "Q-S-R-P"], 0,
      "R introduces smartphone enabling, P details payment expansion, S contrasts vulnerabilities, Q concludes with security consequence.",
      "Identify the broad introductory sentence (R) and the conclusive consequence (Q).",
      "R -> P -> S -> Q.")

add_q("Verbal Ability", "Reading Comprehension", "medium",
      "Passage: 'Economic productivity in knowledge industries depends not on mechanical throughput, but on cognitive serendipity.' What drives productivity here?",
      ["Repetitive routine tasks", "Cross-disciplinary ideation and spontaneous insights", "Maximizing working hours", "Specialized isolation"], 1,
      "Text attributes productivity to 'cognitive serendipity' (spontaneous cross-pollination of ideas).",
      "Contrast 'mechanical throughput' with 'cognitive serendipity'.",
      "Creative, spontaneous cross-domain ideation.")

add_q("Verbal Ability", "Critical Reasoning", "medium",
      "Argument: 'Cities with more bicycle lanes report lower emissions. Therefore, bike lanes cause people to stop driving.' What is the primary flaw?",
      ["It assumes correlation implies causation", "Insufficient sample size", "Circular reasoning", "Personal attack"], 0,
      "Confusing correlation with causation; confounding factors like public transit or urban density may explain both.",
      "Correlation between two trends does not prove one caused the other.",
      "Commits the correlation-causation fallacy.")

add_q("Verbal Ability", "Critical Reasoning", "medium",
      "Statement: 'Company X doubled ad budget and sales rose 50%. Thus ads alone caused growth.' Which weakens this?",
      ["Competitor Y went bankrupt in the same quarter", "Ad costs rose 10%", "Hired 5 managers", "Confidence remained steady"], 0,
      "Competitor bankruptcy provides an alternative explanation for the sales surge.",
      "Look for an alternative factor explaining sales growth.",
      "Competitor bankruptcy explains the market shift.")

add_q("Verbal Ability", "Vocabulary", "medium",
      "Choose the word most nearly OPPOSITE in meaning to 'EPHEMERAL':",
      ["Transient", "Permanent", "Fleeting", "Ethereal"], 1,
      "'Ephemeral' means lasting a short time. Antonym is 'Permanent'.",
      "Opposite of fleeting or momentary.",
      "Permanent means lasting indefinitely.")

add_q("Verbal Ability", "Vocabulary", "medium",
      "Choose the word most nearly SIMILAR to 'OBSEQUIOUS':",
      ["Defiant", "Servile", "Impartial", "Arrogant"], 1,
      "'Obsequious' means excessively fawning or servile.",
      "Describes excessive flattery or obedience.",
      "Servile means fawningly submissive.")

add_q("Verbal Ability", "Vocabulary", "medium",
      "What is the meaning of 'PERSPICACIOUS'?",
      ["Stubborn", "Having keen mental discernment", "Easily deceived", "Exhausted"], 1,
      "'Perspicacious' describes someone with acute insight and understanding.",
      "Related to perspective and sharp mental clarity.",
      "Having keen insight and discernment.")

add_q("Verbal Ability", "Vocabulary", "medium",
      "Choose the antonym of 'LOQUACIOUS':",
      ["Verbose", "Garrulous", "Taciturn", "Articulate"], 2,
      "'Loquacious' means talkative. 'Taciturn' means reserved or saying little.",
      "Opposite of excessively talkative.",
      "Taciturn means quiet and uncommunicative.")

add_q("Verbal Ability", "Idioms & Phrases", "medium",
      "What does 'Bite the bullet' mean?",
      ["Face an unavoidable difficult situation with courage", "Engage in armed conflict", "Make a foolish mistake", "Rush into a decision"], 0,
      "To endure an inevitable painful or grim ordeal bravely.",
      "Originated from biting a lead bullet during surgery before anesthesia.",
      "Endure an unavoidable hardship with fortitude.")

add_q("Verbal Ability", "Idioms & Phrases", "medium",
      "What is 'A Pyrrhic victory'?",
      ["An effortless victory", "A victory won at such devastating cost that it equals defeat", "A victory won by deception", "An underdog triumph"], 1,
      "A victory where the victor's losses are so ruinous that it feels like defeat.",
      "Named after King Pyrrhus whose army suffered unsustainable casualties in victory.",
      "Victory gained at ruinous cost.")

add_q("Verbal Ability", "Cloze Test", "medium",
      "The committee agreed to ______ the outdated policy and ______ new guidelines.",
      ["rescind, promulgate", "endorse, ban", "uphold, discard", "ratify, repeal"], 0,
      "'Rescind' = revoke old rule; 'promulgate' = formally enact and announce new guidelines.",
      "Look for (cancel old) and (announce new).",
      "Rescind and promulgate fit respectively.")

add_q("Verbal Ability", "Sentence Correction", "medium",
      "Identify the error in: 'Having arrived late, a seat could not be found by David.'",
      ["Dangling modifier", "Tense shift", "Subject-verb mismatch", "Faulty parallelism"], 0,
      "'Having arrived late' incorrectly modifies 'a seat' rather than 'David'.",
      "Check who performed the action in the introductory participle phrase.",
      "Classic dangling modifier modifying 'a seat'.")

add_q("Verbal Ability", "Sentence Correction", "medium",
      "Select the correct version: 'Scarcely had the keynote begun ______ the screen flickered.'",
      ["than", "when", "then", "while"], 1,
      "'Scarcely' and 'hardly' pair with 'when'; 'no sooner' pairs with 'than'.",
      "Correlative conjunction for 'scarcely' is 'when'.",
      "Scarcely... when.")

add_q("Verbal Ability", "Sentence Correction", "medium",
      "Choose the correct usage: 'There are ______ cars on the highway today.'",
      ["less", "fewer", "lesser", "fewest"], 1,
      "'Fewer' is used with countable nouns ('cars'); 'less' with uncountable amounts.",
      "Cars are countable items.",
      "Use 'fewer' for countable nouns.")

add_q("Verbal Ability", "Vocabulary", "medium",
      "Choose the antonym of 'VORACIOUS':",
      ["Gluttonous", "Abstemious", "Insatiable", "Rapacious"], 1,
      "'Voracious' = consuming huge quantities. 'Abstemious' = moderate in eating/drinking.",
      "Opposite of excessive greed or appetite.",
      "Abstemious means practicing moderation.")

add_q("Verbal Ability", "Vocabulary", "medium",
      "Choose the synonym of 'CAPRICIOUS':",
      ["Fickle", "Steadfast", "Predictable", "Reliable"], 0,
      "'Capricious' means prone to sudden, unpredictable changes of mood; fickle.",
      "Similar to whimsical or constantly changing.",
      "Fickle means shifting and erratic.")

add_q("Verbal Ability", "Sentence Correction", "medium",
      "Correct sentence: 'I look forward to ______ you.'",
      ["meet", "meeting", "have met", "met"], 1,
      "'Look forward to' takes a gerund (-ing) because 'to' is a preposition.",
      "The 'to' here is a preposition, requiring a noun/gerund.",
      "Look forward to meeting.")

# --- 12 Hard Verbal Ability ---
add_q("Verbal Ability", "Sentence Correction", "hard",
      "The board recommended that the CEO ______ immediately.",
      ["steps down", "step down", "stepped down", "must step down"], 1,
      "Subjunctive mood after verbs of demand/recommendation requires base infinitive ('step down').",
      "Verbs like 'recommend' take the subjunctive mood without third-person -s.",
      "Use base verb form 'step down'.")

add_q("Verbal Ability", "Reading Comprehension", "hard",
      "Passage: 'Algorithmic opacity in credit rating risks encoding historical biases into mathematical models.' Author's tone is:",
      ["Celebratory", "Indifferent", "Cautionary and critical", "Sarcastic"], 2,
      "The author warns against systemic encoding of historical bias, which is cautionary and analytical.",
      "Evaluate the author's stance towards algorithmic opacity.",
      "Cautionary and critical.")

add_q("Verbal Ability", "Critical Reasoning", "hard",
      "Every interviewed successful founder wakes up at 5 AM. Therefore, waking early is necessary for success. This commits:",
      ["Survivorship bias", "False dilemma", "Ad hominem", "Slippery slope"], 0,
      "Only studying the successful cohort ignores early risers who failed (survivorship bias).",
      "Consider the excluded population who also exhibited the trait but failed.",
      "Survivorship bias by sampling only successes.")

add_q("Verbal Ability", "Vocabulary", "hard",
      "Choose the word closest to 'ESOTERIC':",
      ["Obscure", "Familiar", "Ubiquitous", "Elementary"], 0,
      "'Esoteric' means understood by only a select enlightened few with specialized knowledge; obscure.",
      "Pertaining to specialized, arcane knowledge.",
      "Obscure and specialized.")

add_q("Verbal Ability", "Vocabulary", "hard",
      "Choose the antonym of 'NADIR':",
      ["Apex", "Abyss", "Perigee", "Base"], 0,
      "'Nadir' is the lowest point; 'Apex' is the zenith or highest point.",
      "Nadir means rock bottom.",
      "Apex represents the summit or highest point.")

add_q("Verbal Ability", "Idioms & Phrases", "hard",
      "What does 'To cross the Rubicon' mean?",
      ["Take an irrevocable step committing oneself to an enterprise", "Surrender unconditionally", "Travel across Europe", "Negotiate a treaty"], 0,
      "Refers to Julius Caesar crossing the Rubicon in 49 BC, passing the point of no return.",
      "Passing an irrevocable point of no return.",
      "Taking an irreversible decisive step.")

add_q("Verbal Ability", "Reading Comprehension", "hard",
      "Passage: 'Scientific revolutions are not cumulative expansions of existing paradigms, but epistemic ruptures.' Progress is seen as:",
      ["Gradual and linear", "Discontinuous and revolutionary", "Completely random", "Impossible to verify"], 1,
      "Thomas Kuhn's concept describes science moving via discontinuous paradigm shifts.",
      "Look at the phrase 'epistemic ruptures' vs 'cumulative expansions'.",
      "Discontinuous and revolutionary ruptures.")

add_q("Verbal Ability", "Critical Reasoning", "hard",
      "All successful products meet an unmet need. Product X meets an unmet need. Therefore Product X will succeed. What fallacy is this?",
      ["Affirming the consequent", "Denying the antecedent", "Straw man", "Post hoc"], 0,
      "Meeting a need is necessary, not sufficient. Concluding success from the consequent is invalid.",
      "P -> Q. Given Q, concluding P is a formal fallacy.",
      "Affirming the consequent.")

add_q("Verbal Ability", "Vocabulary", "hard",
      "Choose the antonym of 'LACONIC':",
      ["Concise", "Terse", "Garrulous", "Pithy"], 2,
      "'Laconic' means using very few words. 'Garrulous' means excessively talkative.",
      "Opposite of concise and terse.",
      "Garrulous means excessively loquacious.")

add_q("Verbal Ability", "Sentence Correction", "hard",
      "Select the grammatically sound sentence:",
      ["Neither the professor nor the students were present.", "Neither the professor nor the students was present.", "Neither the students nor the professor were present.", "Either the professor or the students was present."], 0,
      "With correlatives 'neither... nor', the verb agrees with the closer subject ('students' is plural -> 'were').",
      "Subject-verb proximity rule: verb matches the noun closest to it.",
      "'students were present' satisfies proximity agreement.")

add_q("Verbal Ability", "Idioms & Phrases", "hard",
      "What does 'Leave no stone unturned' mean?",
      ["Try every possible course of action to achieve a goal", "Conceal evidence", "Build a structure", "Give up early"], 0,
      "To spare no effort and explore every conceivable possibility.",
      "Exhaust all potential avenues.",
      "Try every possible avenue.")

add_q("Verbal Ability", "Vocabulary", "hard",
      "What does 'ANACHRONISTIC' mean?",
      ["Belonging to a period other than that in which it exists", "Occurring simultaneously", "Chronologically ordered", "Timeless"], 0,
      "'Anachronistic' describes something out of its proper chronological or historical time.",
      "Prefix 'ana-' (against/back) + 'chronos' (time).",
      "Chronologically out of place.")

print(f"Total Verbal Ability: {len([q for q in questions if q['category'] == 'Verbal Ability'])}")

# ==========================================
# 4. DATA INTERPRETATION (52 Questions: 20 Easy, 20 Medium, 12 Hard)
# ==========================================

# --- 20 Easy Data Interpretation ---
add_q("Data Interpretation", "Table Chart", "easy",
      "Table: Monthly Sales of 3 Stores (Units)\nStore | Jan | Feb | Mar\nA     | 100 | 120 | 140\nB     | 80  | 90  | 110\nC     | 150 | 130 | 160\nWhat was the total sales of Store A over the 3 months?",
      ["340", "360", "380", "400"], 1,
      "Total Store A = 100 + 120 + 140 = 360 units.",
      "Sum the three values across the Store A row.",
      "100 + 120 + 140 = 360.")

add_q("Data Interpretation", "Table Chart", "easy",
      "From the table above, which store had the highest sales in March?",
      ["Store A", "Store B", "Store C", "All equal"], 2,
      "March sales: Store A = 140, Store B = 110, Store C = 160. Store C is highest.",
      "Compare the values in the March column.",
      "160 (Store C) is greater than 140 and 110.")

add_q("Data Interpretation", "Pie Chart", "easy",
      "A student spends 24 hours a day as follows: Sleeping 8h, School 6h, Studying 4h, Play 4h, Others 2h. What percentage of the day is spent sleeping?",
      ["25%", "30%", "33.3%", "40%"], 2,
      "Sleeping = 8 / 24 = 1/3 = 33.33%.",
      "Divide sleeping hours by 24 and multiply by 100.",
      "8 / 24 = 33.3%.")

add_q("Data Interpretation", "Pie Chart", "easy",
      "In the chart above, what is the central angle for Sleeping in degrees?",
      ["90°", "105°", "120°", "135°"], 2,
      "Angle = (8 / 24) * 360° = (1/3) * 360° = 120°.",
      "Fraction of day multiplied by 360°.",
      "(8 / 24) * 360° = 120°.")

add_q("Data Interpretation", "Bar Chart", "easy",
      "Bar Chart: Number of books sold over 4 days: Mon: 40, Tue: 60, Wed: 50, Thu: 70. What is the average number of books sold per day?",
      ["50", "55", "60", "65"], 1,
      "Sum = 40 + 60 + 50 + 70 = 220. Average = 220 / 4 = 55 books.",
      "Add all 4 values and divide by 4.",
      "220 / 4 = 55.")

add_q("Data Interpretation", "Bar Chart", "easy",
      "From the bar chart above, what was the absolute increase in books sold from Wednesday to Thursday?",
      ["10", "20", "30", "40"], 1,
      "Thursday (70) - Wednesday (50) = 20 books.",
      "Subtract Wednesday's value from Thursday's value.",
      "70 - 50 = 20.")

add_q("Data Interpretation", "Line Graph", "easy",
      "Line Graph: Daily temperature (°C) Mon to Fri: Mon: 28, Tue: 30, Wed: 32, Thu: 31, Fri: 29. On which day was temperature highest?",
      ["Tuesday", "Wednesday", "Thursday", "Friday"], 1,
      "Wednesday had the peak temperature of 32°C.",
      "Locate the highest peak on the graph.",
      "Wednesday is at 32°C.")

add_q("Data Interpretation", "Line Graph", "easy",
      "From the line graph above, what was the temperature change from Wednesday to Friday?",
      ["Drop of 2°C", "Drop of 3°C", "Increase of 1°C", "Drop of 1°C"], 1,
      "Wednesday = 32°C, Friday = 29°C. Change = 29 - 32 = -3°C (drop of 3°C).",
      "Subtract initial from final value.",
      "32 - 29 = 3°C decrease.")

add_q("Data Interpretation", "Table Chart", "easy",
      "Table: Test Scores of 4 Students in Math and Science\nStudent | Math | Science\nAlice   | 85   | 90\nBob     | 75   | 80\nCharlie | 95   | 85\nDavid   | 60   | 70\nWhat is Charlie's total score in both subjects combined?",
      ["170", "175", "180", "185"], 2,
      "Charlie total = 95 + 85 = 180.",
      "Add Charlie's Math and Science marks.",
      "95 + 85 = 180.")

add_q("Data Interpretation", "Table Chart", "easy",
      "Who scored the highest marks in Math?",
      ["Alice", "Bob", "Charlie", "David"], 2,
      "Math scores: Alice 85, Bob 75, Charlie 95, David 60. Charlie is highest.",
      "Check the Math column for maximum value.",
      "95 (Charlie) is highest.")

add_q("Data Interpretation", "Pie Chart", "easy",
      "A company has 500 employees: 50% Engineering, 20% Sales, 20% Operations, 10% HR. How many employees are in Engineering?",
      ["200", "225", "250", "275"], 2,
      "Engineering = 50% of 500 = 250 employees.",
      "Compute 50% of 500.",
      "0.50 * 500 = 250.")

add_q("Data Interpretation", "Pie Chart", "easy",
      "How many total employees are in Sales and HR combined?",
      ["120", "140", "150", "160"], 2,
      "Sales (20%) + HR (10%) = 30%. 30% of 500 = 150 employees.",
      "Combine percentages: 20% + 10% = 30%.",
      "0.30 * 500 = 150.")

add_q("Data Interpretation", "Bar Chart", "easy",
      "Bar Chart: Production of cars (thousands) across 3 years: 2021: 150, 2022: 180, 2023: 210. What is the total production?",
      ["500k", "520k", "540k", "560k"], 2,
      "150 + 180 + 210 = 540 thousand cars.",
      "Sum the 3 yearly values.",
      "150 + 180 + 210 = 540.")

add_q("Data Interpretation", "Bar Chart", "easy",
      "What was the percentage increase in production from 2021 to 2022?",
      ["15%", "18%", "20%", "25%"], 2,
      "Increase = 180 - 150 = 30. % Increase = (30 / 150) * 100 = 20%.",
      "Increase / 2021 baseline.",
      "30 / 150 = 1/5 = 20%.")

add_q("Data Interpretation", "Caselet DI", "easy",
      "In a class of 80 students, 50 play cricket and 40 play football. If 10 play both, how many students play at least one sport?",
      ["70", "75", "80", "85"], 2,
      "n(C U F) = 50 + 40 - 10 = 80 students.",
      "Apply set union formula: A + B - Both.",
      "50 + 40 - 10 = 80.")

add_q("Data Interpretation", "Caselet DI", "easy",
      "How many students play ONLY cricket?",
      ["35", "40", "45", "50"], 1,
      "Only cricket = Total cricket - Both = 50 - 10 = 40 students.",
      "Subtract shared players from total cricket players.",
      "50 - 10 = 40.")

add_q("Data Interpretation", "Line Graph", "easy",
      "Line Graph: Monthly savings ($): Jan: 200, Feb: 250, Mar: 300, Apr: 350. By how much did savings increase each month?",
      ["$25", "$50", "$75", "$100"], 1,
      "Each month savings increases by 250-200 = 300-250 = $50.",
      "Check common difference between consecutive months.",
      "Increases by $50 per month.")

add_q("Data Interpretation", "Table Chart", "easy",
      "Table: Quarterly Profit ($k): Q1: 40, Q2: 50, Q3: 60, Q4: 50. What is the average quarterly profit?",
      ["$45k", "$50k", "$55k", "$60k"], 1,
      "Sum = 40 + 50 + 60 + 50 = 200. Average = 200 / 4 = $50k.",
      "Sum of all 4 quarters divided by 4.",
      "200 / 4 = 50.")

add_q("Data Interpretation", "Pie Chart", "easy",
      "In an exam of 360 total marks, a student scored 90 marks in English. What is the central angle for English on a pie chart?",
      ["60°", "75°", "90°", "105°"], 2,
      "Angle = (90 / 360) * 360° = 90°.",
      "Direct proportion to 360°.",
      "(90 / 360) * 360 = 90°.")

add_q("Data Interpretation", "Bar Chart", "easy",
      "What is the ratio of minimum to maximum production in the series: 120, 150, 180, 240?",
      ["1 : 2", "1 : 3", "2 : 3", "3 : 4"], 0,
      "Minimum = 120, Maximum = 240. Ratio = 120 : 240 = 1 : 2.",
      "Divide the lowest value by the highest value.",
      "120 / 240 = 1 / 2.")

# --- 20 Medium Data Interpretation ---
add_q("Data Interpretation", "Table Chart", "medium",
      "Table: Revenue ($M) of 4 Divisions from 2021 to 2024\nDivision | 2021 | 2022 | 2023 | 2024\nCloud    | 120  | 150  | 195  | 260\nRetail   | 300  | 310  | 320  | 330\nGaming   | 80   | 90   | 110  | 140\nHardware | 200  | 190  | 180  | 170\nWhat division had highest % increase from 2021 to 2024?",
      ["Cloud", "Retail", "Gaming", "Hardware"], 0,
      "Cloud growth = (260 - 120)/120 = 140/120 = +116.7%. Gaming = 60/80 = +75%. Cloud is highest.",
      "Calculate (2024 - 2021) / 2021 for each division.",
      "Cloud more than doubled (+116.7%).")

add_q("Data Interpretation", "Table Chart", "medium",
      "In 2023, what percentage of the total company revenue ($805M) was contributed by Retail ($320M)?",
      ["35.5%", "39.8%", "44.2%", "48.6%"], 1,
      "Retail share = (320 / 805) * 100 ≈ 39.75% ≈ 39.8%.",
      "Retail revenue / Total company revenue.",
      "320 / 805 = 39.8%.")

add_q("Data Interpretation", "Pie Chart", "medium",
      "Budget of $12M distributed: R&D: 35%, Marketing: 25%, Ops: 20%, Salaries: 15%, Legal: 5%. How much more money for R&D than Ops?",
      ["$1.2M", "$1.5M", "$1.8M", "$2.0M"], 2,
      "Difference % = 35% - 20% = 15%. 15% of $12M = $1.8M.",
      "Find percentage difference, then multiply by total budget.",
      "0.15 * 12,000,000 = $1,800,000.")

add_q("Data Interpretation", "Pie Chart", "medium",
      "What is the central angle represented by the Marketing sector (25%) in degrees?",
      ["72°", "85°", "90°", "108°"], 2,
      "Central angle = 25% of 360° = 90°.",
      "Multiply percentage by 3.6.",
      "25 * 3.6 = 90°.")

add_q("Data Interpretation", "Bar Chart", "medium",
      "Bar Chart: Production vs Sales (thousands): 2022: 450/380; 2023: 500/460; 2024: 600/540. What was average unsold inventory per year?",
      ["50k", "56.7k", "62.5k", "70k"], 1,
      "Unsold = (450-380) + (500-460) + (600-540) = 70 + 40 + 60 = 170. Average = 170 / 3 = 56.67k.",
      "Calculate unsold units per year and divide by 3.",
      "(70 + 40 + 60) / 3 = 56.67k.")

add_q("Data Interpretation", "Bar Chart", "medium",
      "In which year was the ratio of sales to production highest?",
      ["2022", "2023", "2024", "Equal in 2023 and 2024"], 1,
      "2022: 380/450 = 0.844; 2023: 460/500 = 0.920; 2024: 540/600 = 0.900. 2023 is highest.",
      "Compare sales/production fraction for each year.",
      "460/500 = 92% is the highest.")

add_q("Data Interpretation", "Line Graph", "medium",
      "Inflation Rate: 2020: 3.2% | 2021: 4.8% | 2022: 7.5% | 2023: 5.1% | 2024: 3.5%. Absolute change between peak and 2024?",
      ["2.4%", "3.5%", "4.0%", "4.3%"], 2,
      "Peak was 2022 (7.5%). 2024 is 3.5%. Absolute change = 7.5% - 3.5% = 4.0%.",
      "Peak value minus 2024 value.",
      "7.5 - 3.5 = 4.0 percentage points.")

add_q("Data Interpretation", "Line Graph", "medium",
      "What was the average inflation rate over the 5-year period (sum = 24.1%)?",
      ["4.62%", "4.82%", "5.02%", "5.22%"], 1,
      "24.1% / 5 = 4.82%.",
      "Sum of all 5 rates divided by 5.",
      "24.1 / 5 = 4.82%.")

add_q("Data Interpretation", "Caselet DI", "medium",
      "University has 1,200 students. 65% study CS, 45% study Data Science, 20% study both. How many study neither?",
      ["100", "120", "140", "160"], 1,
      "CS U DS = 65% + 45% - 20% = 90%. Neither = 10% of 1,200 = 120 students.",
      "Find union percentage first: A + B - Both.",
      "Union = 90%. Neither = 10% of 1200 = 120.")

add_q("Data Interpretation", "Caselet DI", "medium",
      "How many students study ONLY Data Science?",
      ["250", "300", "320", "360"], 1,
      "Only Data Science = 45% - 20% = 25%. 25% of 1,200 = 300 students.",
      "Subtract the intersection from Data Science total.",
      "0.25 * 1200 = 300.")

add_q("Data Interpretation", "Table Chart", "medium",
      "Exports ($B): Software was $80B in 2022 and $120B in 2024. What is the percentage growth?",
      ["40%", "45%", "50%", "55%"], 2,
      "(120 - 80) / 80 = 40 / 80 = 50%.",
      "Increase / 2022 base value.",
      "40 / 80 = 50%.")

add_q("Data Interpretation", "Table Chart", "medium",
      "Petroleum exports: 2022: $45B, 2023: $52B, 2024: $60B. What was average export per year?",
      ["$51.3B", "$52.3B", "$53.3B", "$54.3B"], 1,
      "Sum = 45 + 52 + 60 = 157. Average = 157 / 3 = $52.33B.",
      "Add the three years and divide by 3.",
      "157 / 3 = 52.33.")

add_q("Data Interpretation", "Pie Chart", "medium",
      "Survey of 2,400: Brand A: 30%, Brand B: 25%, Brand C: 20%, Brand D: 15%, Others: 10%. How many preferred B or C?",
      ["960", "1,020", "1,080", "1,140"], 2,
      "Brand B + Brand C = 25% + 20% = 45%. 45% of 2,400 = 1,080.",
      "Combine percentages of B and C.",
      "0.45 * 2400 = 1080.")

add_q("Data Interpretation", "Pie Chart", "medium",
      "What is the difference in degrees between Brand A (30%) and Brand D (15%)?",
      ["36°", "45°", "54°", "60°"], 2,
      "Difference % = 15%. Angle = 15% * 360° = 54°.",
      "Multiply percentage difference by 3.6.",
      "15 * 3.6 = 54°.")

add_q("Data Interpretation", "Bar Chart", "medium",
      "EV Sales (thousands): Q1: 120, Q2: 150, Q3: 180, Q4: 270. % increase from Q3 to Q4?",
      ["40%", "45%", "50%", "60%"], 2,
      "Increase = 270 - 180 = 90. % Increase = 90 / 180 = 50%.",
      "Difference over Q3 sales.",
      "90 / 180 = 50%.")

add_q("Data Interpretation", "Bar Chart", "medium",
      "What % of annual EV sales (720k total) occurred in H1 (Q1+Q2 = 270k)?",
      ["35.5%", "37.5%", "40.0%", "42.5%"], 1,
      "270 / 720 = 3/8 = 37.5%.",
      "H1 sales divided by annual total.",
      "270 / 720 = 37.5%.")

add_q("Data Interpretation", "Line Graph", "medium",
      "GDP growth over 4 years: 4.0%, 6.5%, 7.0%, 8.5%. What was the median growth rate?",
      ["5.5%", "6.75%", "7.0%", "7.25%"], 1,
      "Median of 4 values = average of 2nd and 3rd terms = (6.5% + 7.0%)/2 = 6.75%.",
      "Sort values and average the middle pair.",
      "(6.5 + 7.0) / 2 = 6.75%.")

add_q("Data Interpretation", "Caselet DI", "medium",
      "Office of 500 employees: 60% male (300). 40% of males and 30% of females have master's. How many total hold master's?",
      ["160", "175", "180", "190"], 2,
      "Males = 0.40 * 300 = 120. Females = 0.30 * 200 = 60. Total = 120 + 60 = 180.",
      "Calculate master's holders separately for males and females.",
      "120 + 60 = 180.")

add_q("Data Interpretation", "Table Chart", "medium",
      "Couriers on-time deliveries: A: 9400/10000; B: 14100/15000; C: 19200/20000. Which had highest rate?",
      ["Courier A", "Courier B", "Courier C", "A and B equal"], 2,
      "A = 94%, B = 94%, C = 96%. Courier C is highest.",
      "Convert each ratio to a percentage.",
      "C achieves 96%, higher than 94%.")

add_q("Data Interpretation", "Pie Chart", "medium",
      "Energy mix: Coal 40%, Hydro 25%, Wind 15%, Solar 12%, Nuclear 8%. What % comes from renewables (Hydro+Wind+Solar)?",
      ["48%", "50%", "52%", "55%"], 2,
      "25% + 15% + 12% = 52%.",
      "Sum the percentages of Hydro, Wind, and Solar.",
      "25 + 15 + 12 = 52%.")

# --- 12 Hard Data Interpretation ---
add_q("Data Interpretation", "Table Chart", "hard",
      "Revenue of Cloud grew from $120M in 2021 to $260M in 2024. What is the CAGR approximately?",
      ["24.5%", "29.4%", "33.2%", "38.6%"], 1,
      "CAGR = (260/120)^(1/3) - 1 = (2.167)^0.333 - 1 ≈ 1.294 - 1 = 29.4%.",
      "Apply the Compound Annual Growth Rate formula: (End/Start)^(1/n) - 1.",
      "(2.167)^(1/3) - 1 = 29.4%.")

add_q("Data Interpretation", "Pie Chart", "hard",
      "Total budget $500,000. Divisions: A (35%), B (25%), C (20%), D (20%). Profit margins: B (20%), D (25%). What is combined profit of B and D?",
      ["$45,000", "$50,000", "$52,000", "$55,000"], 1,
      "Profit B = 20% of (25% of 500,000) = $25,000. Profit D = 25% of (20% of 500,000) = $25,000. Total = $50,000.",
      "Compute dollar profit for division B and division D separately.",
      "B profit = $25,000; D profit = $25,000. Sum = $50,000.")

add_q("Data Interpretation", "Mixed Chart", "hard",
      "Company earns $50M revenue with overall margin 18%. Division A contributes 40% of revenue with 25% margin. What is profit of other divisions?",
      ["$3.5M", "$4.0M", "$4.5M", "$5.0M"], 1,
      "Total profit = 18% of $50M = $9M. Div A profit = 25% of $20M = $5M. Other divisions profit = $9M - $5M = $4M.",
      "Subtract Division A's dollar profit from total company profit.",
      "$9.0M - $5.0M = $4.0M.")

add_q("Data Interpretation", "Table Chart", "hard",
      "Table: Export value ($B): Software: 2022: $80B, 2023: $95B, 2024: $120B. Textiles: 2022: $30B, 2023: $28B, 2024: $35B. Ratio of total Software to Textiles?",
      ["295 : 93", "295 : 95", "290 : 93", "300 : 93"], 0,
      "Software sum = 80 + 95 + 120 = 295. Textiles sum = 30 + 28 + 35 = 93. Ratio = 295 : 93.",
      "Sum Software values across 3 years and compare to sum of Textiles.",
      "295 : 93.")

add_q("Data Interpretation", "Bar Chart", "hard",
      "Patents granted: Firm X: 4,800, Firm Y: 3,600, Firm Z: 6,000. Firm X represents what fraction of total patents?",
      ["1/4", "1/3", "4/12", "4/11"], 1,
      "Total = 4800 + 3600 + 6000 = 14,400. Fraction = 4,800 / 14,400 = 1/3.",
      "Divide Firm X's count by total patents granted.",
      "4,800 / 14,400 = 1/3.")

add_q("Data Interpretation", "Caselet DI", "hard",
      "SaaS startup has ARR of $10M and Net Retention Rate (NRR) of 115%. Assuming no new customers, what will ARR be in 2 years?",
      ["$12.5M", "$13.0M", "$13.225M", "$14.0M"], 2,
      "Year 1 = $10M * 1.15 = $11.5M. Year 2 = $11.5M * 1.15 = $13.225M.",
      "Compound the 1.15 multiplier twice.",
      "10 * 1.15 * 1.15 = 13.225M.")

add_q("Data Interpretation", "Table Chart", "hard",
      "Operating margins: Airline A (12.5% on $10B) and Airline B (8% on $15B). What is their combined operating profit?",
      ["$2.25B", "$2.45B", "$2.65B", "$2.85B"], 1,
      "Profit A = 0.125 * 10 = $1.25B. Profit B = 0.08 * 15 = $1.20B. Combined = $1.25B + $1.20B = $2.45B.",
      "Calculate profit for each airline and sum.",
      "$1.25B + $1.20B = $2.45B.")

add_q("Data Interpretation", "Table Chart", "hard",
      "Data Center latencies: DC1 (15, 85, 160 ms), DC2 (90, 18, 170 ms), DC3 (155, 165, 22 ms). Which has lowest global average latency?",
      ["DC1", "DC2", "DC3", "All equal"], 0,
      "DC1 avg = (15+85+160)/3 = 260/3 = 86.67 ms. DC2 avg = 278/3 = 92.67 ms. DC3 avg = 342/3 = 114 ms. DC1 is lowest.",
      "Sum the regional latencies for each data center and divide by 3.",
      "DC1 sum is 260, lowest among all.")

add_q("Data Interpretation", "Pie Chart", "hard",
      "In a healthcare network of 10,000 visits: Cardiology 28%, Ortho 22%, Oncology 18%, Neuro 14%, Peds 18%. Central angle for Cardiology + Oncology?",
      ["145.6°", "155.6°", "165.6°", "175.6°"], 2,
      "Combined % = 28% + 18% = 46%. Central angle = 46% * 360° = 165.6°.",
      "Combine percentages and multiply by 3.6.",
      "46 * 3.6 = 165.6°.")

add_q("Data Interpretation", "Bar Chart", "hard",
      "Wafer output (thousands): Q1: 80, Q2: 100, Q3: 125, Q4: 150. Compound quarterly growth rate from Q1 to Q4?",
      ["21.4%", "23.3%", "25.0%", "28.5%"], 1,
      "(150/80)^(1/3) - 1 = (1.875)^0.333 - 1 ≈ 1.233 - 1 = 23.3%.",
      "Use (Q4/Q1)^(1/3) - 1 for 3 quarterly transitions.",
      "(1.875)^0.333 - 1 = 23.3%.")

add_q("Data Interpretation", "Line Graph", "hard",
      "Quarterly churn rate: Q1: 5.0%, Q2: 4.5%, Q3: 3.8%, Q4: 2.5%. Average percentage point drop per quarter?",
      ["0.70 pp", "0.83 pp", "0.95 pp", "1.10 pp"], 1,
      "Total reduction = 5.0% - 2.5% = 2.5 pp across 3 transitions. Average = 2.5 / 3 = 0.833 percentage points.",
      "Net change divided by number of quarterly intervals (3).",
      "2.5 / 3 = 0.833 pp.")

add_q("Data Interpretation", "Caselet DI", "hard",
      "100,000 daily users: 12% add item to cart. Of those, 25% complete purchase. How many complete purchase daily?",
      ["2,500", "3,000", "3,500", "4,000"], 1,
      "Cart users = 12% of 100,000 = 12,000. Buyers = 25% of 12,000 = 3,000 users.",
      "Multiply 100,000 * 0.12 * 0.25.",
      "12,000 * 0.25 = 3,000.")

print(f"Total Data Interpretation: {len([q for q in questions if q['category'] == 'Data Interpretation'])}")

# Verification of final question bank
print("\n--- FINAL QUESTION BANK SUMMARY ---")
print(f"Total compiled questions: {len(questions)}")

categories = ["Quantitative", "Logical Reasoning", "Verbal Ability", "Data Interpretation"]
for cat in categories:
    cat_qs = [q for q in questions if q['category'] == cat]
    easy_cnt = len([q for q in cat_qs if q['difficulty'] == 'easy'])
    med_cnt = len([q for q in cat_qs if q['difficulty'] == 'medium'])
    hard_cnt = len([q for q in cat_qs if q['difficulty'] == 'hard'])
    print(f"  {cat}: Total={len(cat_qs)} (Easy={easy_cnt}, Medium={med_cnt}, Hard={hard_cnt})")
    assert len(cat_qs) >= 50, f"Category {cat} has less than 50 questions!"
    assert easy_cnt >= 20, f"Category {cat} has less than 20 easy questions!"
    assert med_cnt >= 20, f"Category {cat} has less than 20 medium questions!"
    assert hard_cnt >= 12, f"Category {cat} has less than 12 hard questions!"

# Save to database/sample_questions.json
target_json = os.path.join(os.path.dirname(__file__), '..', 'database', 'sample_questions.json')
with open(target_json, 'w', encoding='utf-8') as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"\nSuccessfully wrote {len(questions)} balanced questions to {target_json}")
